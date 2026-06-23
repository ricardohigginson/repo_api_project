# ============================================================
# STEP 2 — EXTRACT
# Pull job listings from the Adzuna API for all configured
# European countries, page by page, and save raw results to CSV.
#
# What this script does:
# 1. Loads API credentials from the .env file
# 2. Loops through each country in the config
# 3. Requests multiple pages of job results from Adzuna
# 4. Stores the results in a list of dictionaries
# 5. Converts that list into a pandas DataFrame
# 6. Removes duplicate jobs
# 7. Saves the final raw dataset to CSV
#
# ============================================================


# ---------------------------
# Imports
# ---------------------------

import sys
print("DEBUG: script started", flush=True)
# sys is used here so we can stop the script with sys.exit()
# if something important goes wrong, such as missing API keys.

import os
print("DEBUG: os imported", flush=True)
# os is used for:
# - reading environment variables from the .env file
# - creating folders if they do not already exist

import time
print("DEBUG: time imported", flush=True)
# time is used to pause briefly between API requests
# so we do not hit the API too aggressively.

import requests
print("DEBUG: requests imported", flush=True)
# requests is the library used to make HTTP requests to the Adzuna API.

import pandas as pd
print("DEBUG: pandas imported", flush=True)
# pandas is used to create a DataFrame and export it to CSV.

from dotenv import load_dotenv
print("DEBUG: dotenv imported", flush=True)
# load_dotenv reads the .env file and loads its variables
# into the Python environment so os.getenv() can access them.


# ---------------------------
# Import shared configuration
# ---------------------------

print("DEBUG: importing adzuna_config...", flush=True)

from adzuna_config import (
    EUROPEAN_COUNTRIES,
    SEARCH_QUERY,
    RESULTS_PER_PAGE,
    RAW_OUTPUT_PATH,
)

print("DEBUG: adzuna_config imported", flush=True)

# These values come from your shared config file:
# - EUROPEAN_COUNTRIES: list of country codes to search
# - SEARCH_QUERY: the job title / keyword, for example "data analyst"
# - RESULTS_PER_PAGE: number of jobs to request in each API call
# - RAW_OUTPUT_PATH: output CSV path


# ---------------------------
# Load API credentials
# ---------------------------

print("DEBUG: calling load_dotenv()", flush=True)
load_dotenv()
print("DEBUG: load_dotenv finished", flush=True)

# Read the API credentials from the environment.
# These must exist in your .env file.
app_id = os.getenv("app_id")
app_key = os.getenv("app_key")

# Print whether the keys were found.
# This is useful for debugging, but does not expose the actual secret values.
print(f"DEBUG: app_id found? {'yes' if app_id else 'no'}", flush=True)
print(f"DEBUG: app_key found? {'yes' if app_key else 'no'}", flush=True)

# Stop the script immediately if either key is missing.
if not app_id or not app_key:
    print("ERROR: Missing app_id or app_key in .env", flush=True)
    sys.exit(1)


# ---------------------------
# Storage for all jobs
# ---------------------------

# We will collect every job from every country and every page in this list.
# Each item in the list will be one dictionary representing one job.
all_jobs = []


# ---------------------------
# Loop through countries
# ---------------------------

for country in EUROPEAN_COUNTRIES:
    print(f"\nDEBUG: starting country {country}", flush=True)

    # Start from page 1 for each country.
    page = 1

    # Keep requesting pages until the API returns no results
    # or until an error happens.
    while True:

        # Build the API endpoint for the current country and page.
        # Adzuna uses page numbers directly in the URL path.
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

        # Parameters sent with the request.
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": SEARCH_QUERY,
            "results_per_page": RESULTS_PER_PAGE,
            "content-type": "application/json"
        }

        print(f"DEBUG: requesting {country} page {page}", flush=True)

        try:
            # Send request to the Adzuna API.
            # timeout=30 means the request will fail if it takes too long.
            response = requests.get(url, params=params, timeout=30)

            print(f"DEBUG: status code = {response.status_code}", flush=True)

            # If the API does not return success, print the error and stop this country.
            if response.status_code != 200:
                print(f"ERROR: request failed for {country} page {page}", flush=True)
                print(response.text[:500], flush=True)
                break

            # Convert the JSON response into a Python dictionary.
            data = response.json()

            # Get the list of jobs from the "results" field.
            # If "results" does not exist, use an empty list instead.
            results = data.get("results", [])

            print(f"DEBUG: jobs returned = {len(results)}", flush=True)

            # If the API returns no jobs on this page,
            # we assume there are no more pages for this country.
            if not results:
                print(f"DEBUG: no more results for {country}", flush=True)
                break

            # Loop through each job returned on this page.
            for job in results:
                all_jobs.append({
                    # Unique Adzuna job ID
                    "id": job.get("id"),

                    # Country code from our loop
                    "country": country,

                    # Job title
                    "title": job.get("title"),

                    # Company name is nested inside the "company" dictionary
                    "company": (job.get("company") or {}).get("display_name"),

                    # Location name is nested inside the "location" dictionary
                    "location": (job.get("location") or {}).get("display_name"),

                    # Category is nested inside the "category" dictionary
                    "category": (job.get("category") or {}).get("label"),

                    # Salary fields
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "salary_is_predicted": job.get("salary_is_predicted"),

                    # URL to the original job posting
                    "redirect_url": job.get("redirect_url"),

                    # Job description text returned by the API
                    "description": job.get("description"),

                    # Posting date
                    "created": job.get("created"),

                    # Contract details
                    "contract_time": job.get("contract_time"),
                    "contract_type": job.get("contract_type"),

                    # Optional: save which API page this job came from
                    "page": page
                })

            # Move to the next page after processing the current one.
            page += 1

            # Small pause between requests to be polite with the API.
            time.sleep(0.5)

        except Exception as e:
            # If something unexpected happens, print the error
            # and stop processing this country.
            print(f"ERROR: exception on {country} page {page}: {e}", flush=True)
            break


# ---------------------------
# Final checks and export
# ---------------------------

print(f"\nDEBUG: total raw jobs collected = {len(all_jobs)}", flush=True)

# If no jobs were collected at all, stop the script with an error.
if not all_jobs:
    print("ERROR: No jobs were collected", flush=True)
    sys.exit(1)

# Convert the list of job dictionaries into a pandas DataFrame.
df = pd.DataFrame(all_jobs)

# Remove duplicate jobs using the Adzuna job ID.
# This helps in case the same job appears more than once.
df = df.drop_duplicates(subset="id")

# Make sure the output folder exists.
# For example, if RAW_OUTPUT_PATH is "data/raw_jobs.csv",
# this creates the "data" folder if needed.
os.makedirs(os.path.dirname(RAW_OUTPUT_PATH), exist_ok=True)

# Save the cleaned raw dataset to CSV.
df.to_csv(RAW_OUTPUT_PATH, index=False)

print(f"DEBUG: saved {len(df)} unique jobs to {RAW_OUTPUT_PATH}", flush=True)
print("DEBUG: extract step finished successfully", flush=True)
