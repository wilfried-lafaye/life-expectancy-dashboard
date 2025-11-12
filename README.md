## Life Expectancy Around the World

Interactive dashboard exploring **life expectancy at birth** by country and region using open WHO data.  
Built with **Python (Dash/Plotly & Folium)** to practice data ingestion, cleaning, and visualization.

**Data source:** World Health Organization (WHO) — see [WHO Data Portal](https://data.who.int/) [web:3].

## Problem statement 

**Have life expectancy gaps between regions of the world narrowed over the past 20 years, and do they differ between genders ?**

**Hypotheses**
  1. The inter-regional gap **declines** over time.
  2. The **female advantage** is **positive** everywhere, but its magnitude **varies** by region.

- **What we measure in the dashboard**
  - Map: life expectancy by **year** and **sex** to spot low/high clusters.
  - Histogram: share of countries per **life-expectancy range**, with **regional breakdown on hover**.
  

## User Guide

### Prerequisites

- **Python 3.11 or 3.12 (This project currently has compatibility issues with Python 3.14 due to deprecated functions used by Dash; please use Python 3.12 or 3.11 instead. The version used for devlopement is Python 3.12.1)**
- **Internet access** (first run fetches data/GeoJSON)
- Dependencies listed in `requirements.txt`

### Installation

```bash
git clone https://github.com/<your-account>/<your-repo>.git
cd <your-repo>
```

# (recommended) virtual environment
python -m venv .venv
## Windows: 
.venv\Scripts\activate
## macOS/Linux:
source .venv/bin/activate


## To run the dashboard : 
launch main.py or Open directly in your browser http://127.0.0.1:8051/.

### How to Use
**Map.py :** shows a world choropleth that you can filter by **year** and **sex**, with a toggle to display data at the **country** or **region** level.

**Histogramme.py :** one bar per life-expectancy range; hover a bar to see regional breakdown (counts and %)

### Dependency issues

in the shell/terminal, run :

**python -m pip install --upgrade pip**

**python -m pip install -r requirements.txt**

## Data    
**Primary source:** World Health Organization (WHO) — *Life expectancy at birth (years)*.

**Key fields used:**
- `TimeDim` (year)
- `Dim1` / `Dim1_norm` (sex)
- `SpatialDim` (country ISO-3)
- `NumericValue` (life expectancy)
- `ParentLocation` (region)

**Cleaning pipeline:**
1. Keep only rows where `SpatialDimType == "COUNTRY"`.
2. Coerce `NumericValue` to numeric.
3. Normalize sex labels to `SEX_MLE`, `SEX_FMLE`, `SEX_BTSX` (plus readable variants).
4. Save cleaned dataset to `data/cleaned/cleaneddata.csv`.

**World boundaries:** public world-countries GeoJSON, aligned by ISO-3 codes with custom patches.

**Data License:**  
The data used in this project is sourced from the World Health Organization (WHO) and is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. This permits free use, sharing, and adaptation of the data provided proper attribution is given to WHO as the source.

## Developper Guide

### Project Structure

```bash
├─ .vscode/ # editor settings (optional)
├─ assets/
│ └─ custom.css # custom styles for Dash (optional)
├─ data/
│ ├─ cleaned/
│ │ └─ cleaneddata.csv # cleaned dataset used by the app
│ └─ raw/
│ └─ rawdata.csv # original data downloaded (optional)
├─ src/
│ ├─ components/ 
│ │ ├─ init.py
│ │ ├─ histogramme.py # histogram (one color + region details on hover)
│ │ └─ map.py # Folium choropleth builder
│ ├─ pages/ # page layouts + page-specific callbacks
│ │ ├─ init.py
│ │ └─ home.py # home page assembling components
│ └─ utils/ # data utilities
│ ├─ init.py
│ ├─ get_data.py # load/clean helpers (raw → cleaned)
│ └─ clean_data.py # one-off cleaning script (optional)
  └─ clean_data.py
├─ config.py # project-level constants/paths (optional)
├─ main.py # Dash entrypoint (navbar, routing, server)
├─ requirements.txt # pinned dependencies
└─ README.md # documentation
```

## Analysis Report

- Global distribution: most countries lie within 70–80 years; a smaller set reaches 80–90.
- Regional heterogeneity: Africa / Eastern Mediterranean dominate 50–60 and 60–70 bins; Europe / Americas dominate higher bins.
- Sex differences: Female life expectancy is typically 3–6 years higher than Male (varies by region).

These insights come from the interactive views (Map & Histogram) and can be refined by changing year/sex filters.

## Copyright

We hereby certify that the code in this repository is original, except for the lines explicitly cited below.
For each borrowed line (or group of lines), we provide the source reference and a brief explanation of the syntax.

Documented borrowings (to be completed if applicable):

Folium loading/rendering: inspired by Folium documentation; ISO-3 join & ID patching implemented by us.
Sex label normalization: mapping designed from WHO labels; implementation by us.
Any line not declared above is deemed to be authored by the project’s contributors.
Omission or lack of declaration will be considered plagiarism.

## License

Released under the MIT License.

## Authors

Keren Benadiba — keren.bendiba@edu.esiee.fr

Wilfried Lafaye — wilfried.lafaye@icloud.com
