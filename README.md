# Floripa Real Estate Pressure

End-to-end data pipeline analyzing Florianópolis' real estate transformation
over the past decade. Covers the compounding impact of urban regulatory changes,
COVID-19 remote work migration, and the Airbnb short-term rental explosion.
Built with PySpark, dbt, Delta Lake, and Streamlit.

## The Story

Florianópolis experienced a compounding series of pressures on its housing
market driven by three forces:

- **Urban regulatory changes** — LC 482 (Plano Diretor, 2014) and LC 739
(revision, 2023) reshaped land use and supply-side dynamics.
- **COVID-19 remote work migration** — demand shock from high-income remote
workers relocating to the island from 2020 onward.
- **Airbnb short-term rental explosion** — systematic conversion of long-term
housing stock into tourist accommodation.

This project exists to surface and quantify this story through data.

## Key Inflection Points

| Year | Event | Type |
|------|-------|------|
| 2014 | LC 482 — Plano Diretor original | Regulatory |
| 2020 | COVID-19 pandemic | Demand shock |
| 2021 | SELIC at historic lows | Financial |
| 2022 | Censo IBGE 2022 | Demographic |
| 2023 | LC 739 — Plano Diretor revision | Regulatory |

## Architecture
```
Raw Sources → Bronze (Delta) → Silver (Delta) → Gold (Delta) → Streamlit
                ↑                    ↑
        PySpark notebooks        dbt Core
        Databricks Workflows     Local CLI
```

### Stack

- **Compute & Storage** — Databricks Community Edition + Delta Lake
- **Ingestion** — PySpark notebooks, scheduled via Databricks Workflows
- **Transformation** — dbt Core with dbt-databricks adapter, run locally via CLI
- **Serving** — Streamlit Community Cloud
- **Version Control** — GitHub (this repo)

### Medallion Layers

- **Bronze** — raw data as-is, append or overwrite per source
- **Silver** — cleaned, typed, tested, one model per source
- **Gold** — analytical marts consumed directly by Streamlit

## Data Sources

| Source | Description | Access |
|--------|-------------|--------|
| Inside Airbnb | Florianópolis listing snapshots | CSV download |
| BCB API | SELIC and IPCA time series | REST API |
| FIPE/ZAP Índice | Rent and sale price indices | TBD |
| Kaggle Brazil Rent | Property-level features | CSV download |
| IBGE | Censo 2022, population estimates | CSV download |

## Local Development

### Prerequisites
- Python 3.11
- Databricks Community Edition account
- dbt-databricks configured locally

### Setup
```bash
# Clone the repository
git clone https://github.com/pedro-gauch/floripa-real-estate-pressure.git
cd floripa-real-estate-pressure

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Running dbt
```bash
cd transform
dbt deps
dbt run
dbt test
```

## Project Status

🚧 Under active development.
