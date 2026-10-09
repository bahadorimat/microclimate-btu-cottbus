# Microclimate Analysis — BTU Campus Cottbus

**Course:** 13046 Microclimates, SoSe 2026  
**University:** Brandenburg University of Technology Cottbus-Senftenberg  
**Supervisor:** Prof. Dr. Katja Trachte  
**Author:** Matin Bahadori — Matrikel 5006380  
**Field Campaign:** 24 June 2026, 08:45 - 16:30 CEST  

---

## What this project is about

This is the final exercise for the Microclimates course.  
We measured temperature, humidity, and wind at three different surface types on the BTU campus: **Trees**, **Grass**, and **Concrete** and compared how each surface behaves differently throughout the day.

Measurements were taken every 15 minutes at two height levels (near-surface and 2 m).  
Solar radiation data comes from the DWD (German Weather Service) station at Lindenberg.

---

## Files in this repository

```
microclimate-btu-cottbus/
|
|-- FinalEX_complete.py          # Main analysis script - generates all 8 figures
|-- build_report.py              # Script that builds the final PDF report
|-- FinalEX_Report_Bahadori.pdf  # Final academic report (ready to submit)
|-- README.md                    # This file
|
+-- figures/
    |-- fig1_temperature.png     # Temperature time series (all 3 locations)
    |-- fig2_humidity.png        # Relative humidity time series
    |-- fig3_comparison.png      # Cross-location comparison
    |-- fig4_height_diff.png     # Vertical temperature gradient (L1 vs L2)
    |-- fig5_wind.png            # Wind speed, direction, wind roses
    |-- fig6_boxplots.png        # Statistical distributions (box plots)
    |-- fig7_radiation_DWD.png   # DWD solar radiation + clear-sky model
    +-- fig8_radiation_RH.png    # Radiation vs. relative humidity
```

---

## How to run the analysis yourself

### Requirements

```bash
pip install pandas matplotlib numpy pvlib scipy
```

### Step 1 - Set your data folder

Open `FinalEX_complete.py` and change line 15 to point to the folder where your CSV files are:

```python
DATA_DIR = r'/your/path/to/data/folder'
```

You need these 4 files in that folder:
- `Location_trees.csv`
- `Location_grass.csv`
- `Location_concrete.csv`
- `produkt_zehn_min_sd_20250405_20261006_03015.txt` (DWD radiation data)

### Step 2 - Run the script

```bash
python FinalEX_complete.py
```

This will create a `figures/` subfolder and save all 8 plots there automatically.

### Step 3 - Build the PDF report (optional)

```bash
pip install reportlab
python build_report.py
```

This generates `FinalEX_Report_Bahadori.pdf` in the same folder.

---

## Key findings

| Location | Mean Temp (C) | Mean RH (%) | Vertical DeltaT (C) |
|----------|--------------|-------------|---------------------|
| Trees    | 31.3         | 37.4        | -0.38 (cooler near ground) |
| Grass    | 30.7         | 36.5        | +0.34               |
| Concrete | 33.2         | 32.9        | +1.18 (warmer near ground) |

- **Concrete** was the hottest surface - no evapotranspiration, all energy goes to heat.
- **Trees** were the coolest near the ground - canopy shading and evaporation cool the air.
- The campaign day was heavily overcast (only ~6% of clear-sky solar radiation), which muted differences between locations. On a sunny day, contrasts would be much larger.

---

## Data sources

- Field measurements: TESTO 480 handheld sensors, BTU Campus Cottbus
- Solar radiation: DWD Open Data, Station Lindenberg ID 03015
- Clear-sky model: pvlib Ineichen model (Cottbus coordinates)
