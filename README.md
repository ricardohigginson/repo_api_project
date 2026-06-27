# 🌍 European Data Analyst Job Market — End-to-End Pipeline

An end-to-end data pipeline that extracts, scrapes, cleans, and analyses Data Analyst job postings across 10 European countries from the Adzuna job search engine, enriched with World Bank macroeconomic indicators. Built as a capstone project for the Ironhack Data Analytics Bootcamp to map the real state of the Data Analyst job market across Europe.

A summary of the findings can be found in the ppt here: https://docs.google.com/presentation/d/1sKGe9iyxqKputSVpMaVgsdR3MR7kh61N/edit?usp=share_link&ouid=101510910436796838770&rtpof=true&sd=true 

---

## 📁 Project Structure

```
project_api/
│
├── adzuna_config.py               # Shared config: paths, countries, query settings
├── .env                           # API credentials (not committed — see setup)
│
├── 2_adzuna_extract.py            # Step 1 — Pull jobs from Adzuna API → data/raw_jobs.csv
├── 3_adzuna_scrape.py             # Step 2 — Scrape full descriptions via Selenium → data/scraped_jobs.csv
├── 4_adzuna_export.py             # Step 3 — Clean & export → data/final_jobs.xlsx
├── 5_adzuna_rescrape.py           # Step 4 — Fix /land/ redirect URLs → data/final_jobs_fixed.xlsx
│
├── Adzuna API + Webscrap.ipynb    # Notebook runner: executes steps 1–4 in sequence
├── Import from Worldbank.ipynb    # Fetches macroeconomic indicators → world_bank_data.csv
├── jobs_clieaning_task.ipynb      # Cleaning & feature extraction → jobs_clean.csv
├── job_analysis.ipynb             # EDA and visualisations (6 research questions)
│
└── data/
    ├── raw_jobs.csv               # Output of step 1 (API extract)
    ├── scraped_jobs.csv           # Output of step 2 (Selenium scrape)
    ├── final_jobs.xlsx            # Output of step 3 (export)
    └── final_jobs_fixed.xlsx      # Output of step 4 (/land/ rescrape)
```

> ⚠️ **Path convention — read this before running anything.**
> - Scripts `2–5` and `adzuna_config.py` all use `data/` as a relative path. They must be run from the **project root** (`project_api/`).
> - `Import from Worldbank.ipynb` saves `world_bank_data.csv` directly to the **project root** (no `data/` subfolder).
> - `jobs_clieaning_task.ipynb` reads `final_jobs_fixed.xlsx` from the **project root** and saves `jobs_clean.csv` to the **project root**.
> - `job_analysis.ipynb` reads both `jobs_clean.csv` and `world_bank_data.csv` from the **project root**.
>
> In short: the `data/` folder is only for the raw/scraped/exported files produced by the `.py` scripts. All notebooks read and write from the project root.

---

## ⚙️ Pipeline Overview

```
Adzuna API
    ↓  2_adzuna_extract.py
data/raw_jobs.csv
    ↓  3_adzuna_scrape.py
data/scraped_jobs.csv
    ↓  4_adzuna_export.py
data/final_jobs.xlsx
    ↓  5_adzuna_rescrape.py
data/final_jobs_fixed.xlsx  ──────────────────────────────────────┐
                                                                   ↓
World Bank API → Import from Worldbank.ipynb → world_bank_data.csv
                                                                   ↓
                          jobs_clieaning_task.ipynb reads final_jobs_fixed.xlsx
                                                                   ↓
                                                          jobs_clean.csv
                                                                   ↓
                                             job_analysis.ipynb (+ world_bank_data.csv)
```

---

## 🚀 Quick Start

### 1. Clone and set up the environment

```bash
git clone <your-repo-url>
cd project_api
pip install -r requirements.txt
```

### 2. Create your `.env` file

```
app_id=YOUR_ADZUNA_APP_ID
app_key=YOUR_ADZUNA_APP_KEY
```

Get your free credentials at [developer.adzuna.com](https://developer.adzuna.com).

### 3. Create the data folder

```bash
mkdir data
```

### 4. Run the extraction + scraping pipeline

**Option A — via the notebook runner** (recommended):

Open `Adzuna API + Webscrap.ipynb` and run all cells. The first block executes scripts 2, 3, and 4 in order; the second block runs script 5 separately for the `/land/` URL fix.

> The notebook must be **opened from the project root** so that `adzuna_config.py` is importable. Launch Jupyter from there:
> ```bash
> cd project_api
> jupyter notebook
> ```

**Option B — via terminal**, one script at a time:

```bash
python 2_adzuna_extract.py    # Pull jobs from API        → data/raw_jobs.csv
python 3_adzuna_scrape.py     # Scrape full descriptions  → data/scraped_jobs.csv
python 4_adzuna_export.py     # Export clean file         → data/final_jobs.xlsx
python 5_adzuna_rescrape.py   # Fix /land/ URLs           → data/final_jobs_fixed.xlsx
```

### 5. Fetch World Bank macroeconomic data

Open `Import from Worldbank.ipynb` and run all cells.

Output: `world_bank_data.csv` saved to the **project root**.

### 6. Clean and enrich the jobs data

Open `jobs_clieaning_task.ipynb` and run all cells.

Reads: `final_jobs_fixed.xlsx` from the **project root**.  
Output: `jobs_clean.csv` saved to the **project root**.

> Before opening the notebook, **copy `final_jobs_fixed.xlsx` from `data/` to the project root**, or update the read path in Cell 1 to `"data/final_jobs_fixed.xlsx"`. See the path issue note below.

### 7. Analyse

Open `job_analysis.ipynb` and run all cells.

Reads: `jobs_clean.csv` and `world_bank_data.csv` from the **project root**.

---

## 📦 Dependencies

Install all with:

```bash
pip install -r requirements.txt
```

**Core packages:**

| Package | Purpose |
|---|---|
| `requests` | Adzuna API and World Bank API calls |
| `pandas` | Data manipulation throughout the pipeline |
| `openpyxl` | Reading and writing `.xlsx` files |
| `python-dotenv` | Loading `.env` API credentials |
| `selenium` | Headless Firefox scraping |
| `beautifulsoup4` | HTML parsing of scraped pages |
| `webdriver-manager` | Auto-installs geckodriver for Firefox |
| `plotly` | Interactive choropleth maps and charts |
| `geopandas` | Map geometry for choropleth visualisations |
| `geodatasets` | Geometry data used by geopandas |
| `pycountry` | ISO-2 → ISO-3 country code conversion |
| `numpy` | Numerical operations and normalisation |
| `matplotlib` | Base plots (heatmaps, bar charts, line charts) |
| `seaborn` | Statistical charts (heatmaps, stacked bars) |

**Two packages require an explicit install command:**

```bash
pip install geopandas geodatasets
```

**Browser requirement:** Firefox must be installed on your machine. `webdriver-manager` handles `geckodriver` automatically.

---

## 🌐 Countries Covered

| Code | Country |
|---|---|
| `at` | Austria |
| `be` | Belgium |
| `fr` | France |
| `de` | Germany |
| `it` | Italy |
| `nl` | Netherlands |
| `pl` | Poland |
| `es` | Spain |
| `ch` | Switzerland |
| `gb` | United Kingdom |

---

## 🔧 Configuration

All shared settings live in `adzuna_config.py`:

```python
SEARCH_QUERY              = "data analyst"
RESULTS_PER_PAGE          = 50
RAW_OUTPUT_PATH           = "data/raw_jobs.csv"
SCRAPED_OUTPUT_PATH       = "data/scraped_jobs.csv"
FINAL_OUTPUT_PATH         = "data/final_jobs.xlsx"
LAND_RESCRAPE_OUTPUT_PATH = "data/final_jobs_fixed.xlsx"
```

Change `SEARCH_QUERY` to target a different job title. All scripts pick up the updated paths automatically.

---

## 📓 Notebooks

### `Adzuna API + Webscrap.ipynb`
Orchestrates the pipeline by calling scripts 2, 3, and 4 via `subprocess.run()`, then runs script 5 in a separate cell. All `.py` scripts must be in the **same directory** as the notebook for `adzuna_config` imports to resolve.

### `Import from Worldbank.ipynb`
Fetches 2024 macroeconomic data for all 10 countries in a single batched request per indicator. Outputs a wide-format CSV (`world_bank_data.csv`) with one row per country, saved to the **project root**.

Indicators retrieved:

| Column | World Bank Code | Description |
|---|---|---|
| `population` | `SP.POP.TOTL` | Total population |
| `gdp_per_capita` | `NY.GDP.PCAP.CD` | GDP per capita (USD) |
| `inflation_cpi` | `FP.CPI.TOTL.ZG` | Inflation rate (CPI %) |
| `unemployment_rate` | `SL.UEM.TOTL.ZS` | General unemployment (%) |
| `youth_unemployment` | `SL.UEM.1524.NE.ZS` | Youth unemployment (%) |

### `jobs_clieaning_task.ipynb`
Reads `final_jobs_fixed.xlsx` and produces `jobs_clean.csv`. Main transformations:

- **Work mode** extraction (Remote / Hybrid / Onsite / Unspecified) using multilingual keyword dictionaries across EN, IT, DE, FR, NL, PL, ES
- **Seniority level** detection (Intern → Junior → Middle → Senior → Unspecified)
- **Contract type** extraction
- **Skills** extraction (Python, SQL, Excel, Power BI, Tableau, and more)
- City and company name parsing from nested API string fields
- Title cleaning and **job category** assignment (data analyst, data engineer, data scientist, business analyst, financial analyst, and others)
- Salary parsing, **currency detection** (EUR / GBP / PLN), and EUR conversion using fixed exchange rates
- Columns dropped in the clean output: `company`, `location`, `salary_min`, `salary_max`, `country`, `redirect_url`

### `job_analysis.ipynb`
EDA and visualisations filtered to **2026 postings**, further narrowed to the `"data analyst"` job category. Answers 6 research questions:

1. Which countries have the most Data Analyst job postings? *(choropleth map + % share)*
2. Which countries offer the best overall opportunity? *(composite score: salary 35%, market size 20%, GDP 20%, unemployment 15%, inflation 10%)*
3. What skills are most requested, and how do they vary by country? *(top-10 skill frequency table + choropleth of top skill per country)*
4. How is work mode distributed by country? *(heatmap + stacked horizontal bar)*
5. What seniority levels are most requested per country? *(heatmap + stacked horizontal bar)*
6. Which countries publish the most jobs per week? *(weekly trend line chart + average jobs/week bar chart)*

---

## ⚠️ Known Issues & Fixes

### ❗ `ModuleNotFoundError: No module named 'adzuna_config'`

Occurs when the notebook runner calls scripts via `subprocess` and the working directory is not the project root.

**Fix:** Always launch Jupyter from the project root:

```bash
cd project_api
jupyter notebook
```

Or add this at the top of the runner cell:

```python
import os
os.chdir("/absolute/path/to/project_api")
```

---

### ❗ `ModuleNotFoundError: No module named 'selenium'`

The scraper scripts require `selenium` in the **same Python environment** that Jupyter is running from.

**Fix:**

```bash
pip install selenium webdriver-manager
```

Confirm you are installing into the same environment: `which python` in the terminal should match the Jupyter kernel.

---

### ❗ Path mismatch — `jobs_clieaning_task.ipynb` reads from the project root, not `data/`

Cell 1 of the cleaning notebook reads:

```python
jobs_df = pd.read_excel("final_jobs_fixed.xlsx", engine="openpyxl")
```

But `5_adzuna_rescrape.py` saves that file to `data/final_jobs_fixed.xlsx`.

**Fix (pick one):**

Option A — copy the file to the project root before opening the notebook:
```bash
cp data/final_jobs_fixed.xlsx ./final_jobs_fixed.xlsx
```

Option B — update Cell 1 in the notebook to match the actual path:
```python
jobs_df = pd.read_excel("data/final_jobs_fixed.xlsx", engine="openpyxl")
```

---

### ❗ `/land/` URL bot detection

Adzuna redirect URLs containing `/land/` trigger bot detection and return an "Access Denied" page. Script `5_adzuna_rescrape.py` fixes this by reconstructing the equivalent `/details/` URL:

```
https://www.adzuna.it/land/ad/123456?se=...  →  https://www.adzuna.it/details/123456
```

Always run step 5 after step 4. The original `final_jobs.xlsx` is never modified — output goes to `final_jobs_fixed.xlsx`.

---

## 📊 Output Files Summary

| File | Location | Produced by | Description |
|---|---|---|---|
| `raw_jobs.csv` | `data/` | `2_adzuna_extract.py` | Raw API output, ~50 jobs × 10 countries × N pages |
| `scraped_jobs.csv` | `data/` | `3_adzuna_scrape.py` | Same rows + full scraped descriptions |
| `final_jobs.xlsx` | `data/` | `4_adzuna_export.py` | Deduplicated, key columns only |
| `final_jobs_fixed.xlsx` | `data/` | `5_adzuna_rescrape.py` | `/land/` rows re-scraped via `/details/` |
| `world_bank_data.csv` | project root | `Import from Worldbank.ipynb` | 5 macroeconomic indicators, 10 countries, 2024 |
| `jobs_clean.csv` | project root | `jobs_clieaning_task.ipynb` | Fully cleaned and enriched dataset, ready for analysis |

---

## 📜 License

This project was built for educational purposes as part of the Ironhack Data Analytics Bootcamp.
