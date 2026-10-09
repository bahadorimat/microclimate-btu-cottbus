# =============================================================================
# 13046 Microclimates - Final Exercise
# Microclimate Analysis of Urban Surface Types at BTU Campus Cottbus
# Field Campaign: 24 June 2026, 08:45 – 16:30 CEST, 15-min intervals
#
# Student : Matin Bahadori  |  Matrikel: 5006380
# Lecturer: Prof. Dr. Katja Trachte  |  SoSe 2026
#
#
# =============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = r'/Users/matinbahadori/Desktop'   # <-- put your actual folder here
OUT_DIR  = os.path.join(DATA_DIR, 'figures')

DWD_FILE = os.path.join(DATA_DIR, 'produkt_zehn_min_sd_20250405_20261006_03015.txt')

# Campaign window (CEST)
CAMPAIGN_START = '2026-06-24 08:45'
CAMPAIGN_END   = '2026-06-24 16:30'


LAT, LON, ALT = 51.758, 14.318, 69   # degrees N, degrees E, metres a.s.l.

COLOR = {
    'Trees':    '#2CA02C',   # green
    'Grass':    '#BCBD22',   # olive/yellow-green
    'Concrete': '#D62728',   # red
}
BG = '#F8F9FA'   # very light grey panel background

plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'font.size':          10,
    'axes.titlesize':     11,
    'axes.titleweight':   'bold',
    'axes.labelsize':     10,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.grid':          True,
    'grid.linestyle':     '--',
    'grid.alpha':         0.4,
    'legend.framealpha':  0.85,
    'legend.fontsize':    9,
    'figure.facecolor':   'white',
    'savefig.dpi':        200,
    'savefig.bbox':       'tight',
})

os.makedirs(OUT_DIR, exist_ok=True)


def fmt_xaxis(ax, rotate=30):
    """Format x-axis as HH:MM (CEST), one tick per hour."""
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[30]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=rotate, ha='right', fontsize=9)
    ax.set_xlabel('Time (CEST)  —  24 June 2026', fontsize=10)

def set_bg(ax):
    """Light background for an axes panel."""
    ax.set_facecolor(BG)

def save_fig(fig, name):
    """Save figure to OUT_DIR and close it."""
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path)
    plt.close(fig)
    print(f'  Saved: {path}')

print('=' * 60)
print('STEP 1 — Loading field data')
print('=' * 60)

trees = pd.read_csv(os.path.join(DATA_DIR, 'Location_trees.csv'))
trees['Date'] = pd.to_datetime(trees['Date'])
trees = trees.sort_values('Date').set_index('Date')

trees.rename(columns={
    'TEMP_0M(°C)':      'T_L1',
    'TEMP_2M(°C)':      'T_L2',
    'RH_0M(%)':         'RH_L1',
    'RH_2M(%)':         'RH_L2',
    'WS_min_0M(m/s)':   'WS_min_L1',
    'WS max L1(m/s)':   'WS_max_L1',
    'WS_min_0m(m/s)':   'WS_min_L2',
    'WS_max_2m(m/s)':   'WS_max_L2',
    'Wind_dir':          'WD',
    'Dew_point_0m(°C)': 'DP_L1',
    'Dew_point_2m(°C)': 'DP_L2',
    'Air Pressure(hPa)':'AP',
}, inplace=True)

# Mean wind speed = average of min and max over the 15-min interval
trees['WS_L1'] = (pd.to_numeric(trees['WS_min_L1'], errors='coerce') +
                  pd.to_numeric(trees['WS_max_L1'], errors='coerce')) / 2
trees['WS_L2'] =  pd.to_numeric(trees['WS_max_L2'], errors='coerce')

grass = pd.read_csv(os.path.join(DATA_DIR, 'Location_grass.csv'), sep=';')

def fix_grass_timestamp(s):
    dt = pd.to_datetime(s, format='%d.%m.%Y %H:%M')
    if dt.hour < 8:
        dt = dt + pd.Timedelta(hours=12)
    return dt

grass['Date'] = grass['Date'].apply(fix_grass_timestamp)
grass = grass.sort_values('Date').set_index('Date')

grass.rename(columns={
    'Temp L1(°C)':       'T_L1',
    'Temp L2(°C)':       'T_L2',
    'Humidity L1(%)':    'RH_L1',
    'Humidity L2(%)':    'RH_L2',
    'Dew Point L1(°C)':  'DP_L1',
    'Dew Point L2(°C)':  'DP_L2',
    'Air Pressure(hPa)': 'AP',
    'Wind Direction':    'WD',
    'WS max (m/s)':      'WS_max_L1',
    'WS min (m/s)':      'WS_min_L1',
}, inplace=True)

for col in ['T_L1', 'T_L2', 'RH_L1', 'RH_L2', 'WS_max_L1', 'WS_min_L1']:
    grass[col] = pd.to_numeric(grass[col], errors='coerce')

grass['WS_L1'] = (grass['WS_max_L1'] + grass['WS_min_L1']) / 2


concrete = pd.read_csv(os.path.join(DATA_DIR, 'Location_concrete.csv'))
concrete['Date'] = pd.to_datetime(concrete['Date'])
concrete = concrete.sort_values('Date').set_index('Date')

concrete.rename(columns={
    'TEMP_0M(°C)':      'T_L1',
    'TEMP_2M(°C)':      'T_L2',
    'RH_0M(%)':         'RH_L1',
    'RH_2M(%)':         'RH_L2',
    'WS_0m(m/s)':       'WS_L1',
    'WS_2m(m/s)':       'WS_L2',
    'Wind_dir':         'WD',
    'Dew_point_0m(°C)': 'DP_L1',
    'Dew_point_2m(°C)': 'DP_L2',
}, inplace=True)

# Force numeric — concrete CSV stores all values as strings
for col in ['T_L1', 'T_L2', 'RH_L1', 'RH_L2', 'WS_L1', 'WS_L2', 'WD']:
    concrete[col] = pd.to_numeric(concrete[col], errors='coerce')

trees    = trees.loc[CAMPAIGN_START:CAMPAIGN_END]
grass    = grass.loc[CAMPAIGN_START:CAMPAIGN_END]
concrete = concrete.loc[CAMPAIGN_START:CAMPAIGN_END]

# Convenience list for loop-based plotting
datasets = [
    ('Trees',    trees,    COLOR['Trees']),
    ('Grass',    grass,    COLOR['Grass']),
    ('Concrete', concrete, COLOR['Concrete']),
]

print(f'  Trees   : {len(trees)} records  '
      f'({trees.index.min().strftime("%H:%M")} – {trees.index.max().strftime("%H:%M")} CEST)')
print(f'  Grass   : {len(grass)} records  '
      f'({grass.index.min().strftime("%H:%M")} – {grass.index.max().strftime("%H:%M")} CEST)')
print(f'  Concrete: {len(concrete)} records  '
      f'({concrete.index.min().strftime("%H:%M")} – {concrete.index.max().strftime("%H:%M")} CEST)')

# =============================================================================
# STEP 2: LOAD DWD LINDENBERG RADIATION DATA (Station ID 03015)
# =============================================================================
print('\n' + '=' * 60)
print('STEP 2 — Loading DWD Lindenberg radiation data (ID 03015)')
print('=' * 60)

# Semicolon-separated, UTC timestamps, missing = -999
dwd = pd.read_csv(DWD_FILE, sep=';', skipinitialspace=True)
dwd.columns = [c.strip() for c in dwd.columns]

# Parse MESS_DATUM: format YYYYMMDDhhmm  e.g. 202606240645
dwd['datetime'] = pd.to_datetime(
    dwd['MESS_DATUM'].astype(str).str.strip(), format='%Y%m%d%H%M')
dwd = dwd.set_index('datetime').sort_index()

# Replace -999 missing-data code with NaN
for col in ['DS_10', 'GS_10', 'SD_10', 'LS_10']:
    if col in dwd.columns:
        dwd[col] = pd.to_numeric(dwd[col], errors='coerce').replace(-999.0, np.nan)

# Filter to 24 June 2026  (index is UTC)
target_date = pd.Timestamp('2026-06-24').date()
day_dwd = dwd[dwd.index.date == target_date].copy()
print(f'  DWD records on 24 Jun 2026 (UTC): {len(day_dwd)}')

# GS_10 = Global Solar (GHI),  DS_10 = Diffuse Solar (DHI)
# Resample 10-min → 15-min, keep campaign window in UTC
rad = day_dwd[['GS_10', 'DS_10']].resample('15min').mean()
rad = rad.between_time('06:45', '14:30')   # 06:45–14:30 UTC = 08:45–16:30 CEST
rad.columns = ['GHI', 'DHI']

# Shift index from UTC to CEST (UTC+2) so it aligns with field data
rad.index = rad.index + pd.Timedelta(hours=2)

print(f'  Resampled 15-min records (CEST): {len(rad)}')
print(f'  GHI  mean = {rad["GHI"].mean():.1f} W/m²  |  '
      f'max = {rad["GHI"].max():.1f} W/m²  |  '
      f'min = {rad["GHI"].min():.1f} W/m²')

# =============================================================================
# STEP 3: pvlib INEICHEN CLEAR-SKY REFERENCE (Cottbus)
# =============================================================================
print('\n' + '=' * 60)
print('STEP 3 — Computing pvlib Ineichen clear-sky model for Cottbus')
print('=' * 60)

has_cs  = False
peak_cs = None
cs_15   = None

try:
    import pvlib

    location = pvlib.location.Location(
        latitude=LAT, longitude=LON,
        tz='Europe/Berlin', altitude=ALT, name='Cottbus',
    )

    # 10-min time series for the full day, local time
    times = pd.date_range(
        '2026-06-24 00:00', '2026-06-24 23:50',
        freq='10min', tz='Europe/Berlin',
    )

    # Ineichen model (uses Linke turbidity climatology)
    cs = location.get_clearsky(times, model='ineichen')

    # Resample to 15-min, keep campaign window, strip timezone
    cs_15 = cs[['ghi', 'dhi']].resample('15min').mean()
    cs_15 = cs_15.between_time('08:45', '16:30')
    cs_15.columns = ['GHI_cs', 'DHI_cs']
    cs_15.index   = cs_15.index.tz_localize(None)

    rad.index = rad.index.tz_localize(None)   # align with cs_15

    peak_cs   = cs_15['GHI_cs'].max()
    cloud_pct = rad['GHI'].mean() / peak_cs * 100
    has_cs    = True

    print(f'  Clear-sky GHI peak (Cottbus): {peak_cs:.0f} W/m²  '
          f'at {cs_15["GHI_cs"].idxmax().strftime("%H:%M")} CEST')
    print(f'  Measured / clear-sky ratio  : {cloud_pct:.1f}%  → HEAVILY OVERCAST')

except ImportError:
    print('  pvlib not installed — skipping clear-sky model')
    print('  Install with:  pip install pvlib')

# =============================================================================
# STEP 4: DESCRIPTIVE STATISTICS
# =============================================================================
print('\n' + '=' * 60)
print('STEP 4 — Descriptive Statistics')
print('=' * 60)

for name, df, _ in datasets:
    print(f'\n  --- {name} ---')
    for lv in ['L1', 'L2']:
        for var, vname in [('T', 'Temp (°C)'), ('RH', 'RH    (%)  ')]:
            col = f'{var}_{lv}'
            if col in df.columns:
                s = df[col].dropna()
                print(f'    {vname} {lv}: '
                      f'min={s.min():.1f}  max={s.max():.1f}  '
                      f'mean={s.mean():.1f}  std={s.std():.2f}  n={len(s)}')

    # Vertical temperature gradient
    if 'T_L1' in df.columns and 'T_L2' in df.columns:
        dt = (df['T_L1'] - df['T_L2']).dropna()
        print(f'    Delta-T (L1-L2):  mean={dt.mean():+.2f}  '
              f'max={dt.max():+.2f}  min={dt.min():+.2f}')

# =============================================================================
# STEP 5: FIGURE 1 — Temperature time series (3 panels, one per location)
# =============================================================================
print('\n' + '=' * 60)
print('STEP 5 — Generating figures')
print('=' * 60)
print('\nFigure 1: Temperature time series')

fig, axes = plt.subplots(3, 1, figsize=(12, 11), sharex=True)
fig.suptitle(
    'Air Temperature — 24 June 2026\nBTU Campus Cottbus Field Campaign',
    fontsize=13, fontweight='bold', y=1.01,
)

for ax, (name, df, col) in zip(axes, datasets):
    set_bg(ax)

    # Solid line for L1, dashed for L2
    ax.plot(df.index, df['T_L1'],
            color=col, lw=2.5, ls='-',  zorder=3, label='L1  (near-surface ≈ 0 m)')
    ax.plot(df.index, df['T_L2'],
            color=col, lw=2.0, ls='--', alpha=0.70, zorder=2, label='L2  (2 m height)')

    # Shaded band between L1 and L2 — highlights vertical gradient
    ax.fill_between(df.index, df['T_L1'], df['T_L2'],
                    color=col, alpha=0.10, zorder=1)

    # Dotted mean line
    mean_t = df['T_L1'].mean()
    ax.axhline(mean_t, color=col, lw=0.8, ls=':', alpha=0.6)
    ax.text(df.index[-1], mean_t + 0.3,
            f'mean L1 = {mean_t:.1f} °C',
            color=col, fontsize=8, ha='right', va='bottom')

    ax.set_ylabel('Temperature (°C)', fontsize=10)
    ax.set_ylim(22, 41)
    ax.set_title(f'Location: {name}', color=col)
    ax.legend(loc='upper left', ncol=2)

    # Annotate maximum
    imax = df['T_L1'].idxmax()
    vmax = df['T_L1'].max()
    ax.annotate(
        f'max {vmax:.1f} °C',
        xy=(imax, vmax), xytext=(8, 6), textcoords='offset points',
        fontsize=8, color=col,
        arrowprops=dict(arrowstyle='->', color=col, lw=0.8),
    )

fmt_xaxis(axes[-1])
fig.tight_layout()
save_fig(fig, 'fig1_temperature.png')

# =============================================================================
# FIGURE 2 — Relative Humidity time series (3 panels)
# =============================================================================
print('Figure 2: Relative humidity time series')

fig, axes = plt.subplots(3, 1, figsize=(12, 11), sharex=True)
fig.suptitle(
    'Relative Humidity — 24 June 2026\nBTU Campus Cottbus Field Campaign',
    fontsize=13, fontweight='bold', y=1.01,
)

for ax, (name, df, col) in zip(axes, datasets):
    set_bg(ax)
    ax.plot(df.index, df['RH_L1'],
            color=col, lw=2.5, ls='-',  zorder=3, label='L1  (near-surface)')
    ax.plot(df.index, df['RH_L2'],
            color=col, lw=2.0, ls='--', alpha=0.70, zorder=2, label='L2  (2 m)')
    ax.fill_between(df.index, df['RH_L1'], df['RH_L2'],
                    color=col, alpha=0.10, zorder=1)

    mean_rh = df['RH_L1'].mean()
    ax.axhline(mean_rh, color=col, lw=0.8, ls=':', alpha=0.6)
    ax.text(df.index[-1], mean_rh + 0.5,
            f'mean L1 = {mean_rh:.1f} %',
            color=col, fontsize=8, ha='right', va='bottom')

    ax.set_ylabel('Rel. Humidity (%)', fontsize=10)
    ax.set_ylim(18, 72)
    ax.set_title(f'Location: {name}', color=col)
    ax.legend(loc='upper right', ncol=2)

fmt_xaxis(axes[-1])
fig.tight_layout()
save_fig(fig, 'fig2_humidity.png')

# =============================================================================
# FIGURE 3 — Cross-location comparison (all 3 locations on shared axes)
# =============================================================================
print('Figure 3: Cross-location comparison')

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle(
    'Cross-Location Comparison — Temperature & Humidity\n'
    'BTU Campus Cottbus, 24 June 2026',
    fontsize=13, fontweight='bold',
)

ls_map = {'L1': '-',  'L2': '--'}
lw_map = {'L1': 2.2, 'L2': 1.6}

for name, df, col in datasets:
    for lv, var in [('L1', 'T_L1'), ('L2', 'T_L2')]:
        axes[0].plot(df.index, df[var],
                     color=col, lw=lw_map[lv], ls=ls_map[lv],
                     alpha=1.0 if lv == 'L1' else 0.65,
                     label=f'{name} {lv}')
    for lv, var in [('L1', 'RH_L1'), ('L2', 'RH_L2')]:
        axes[1].plot(df.index, df[var],
                     color=col, lw=lw_map[lv], ls=ls_map[lv],
                     alpha=1.0 if lv == 'L1' else 0.65,
                     label=f'{name} {lv}')

for ax, ylab, title in zip(
        axes,
        ['Temperature (°C)', 'Relative Humidity (%)'],
        ['Temperature — All Locations', 'Relative Humidity — All Locations']):
    set_bg(ax)
    ax.set_ylabel(ylab)
    ax.set_title(title)
    ax.legend(ncol=3, fontsize=8)
    fmt_xaxis(ax)

# Bottom legend: colored patches per location
loc_patches = [Patch(color=COLOR[n], label=n) for n in ['Trees', 'Grass', 'Concrete']]
fig.legend(
    handles=loc_patches,
    loc='lower center', ncol=3, fontsize=9, framealpha=0.9,
    title='Location  (solid = L1 near-surface  |  dashed = L2 at 2 m)',
    title_fontsize=8, bbox_to_anchor=(0.5, -0.04),
)
fig.tight_layout()
save_fig(fig, 'fig3_comparison.png')

# =============================================================================
# FIGURE 4 — Vertical temperature gradient ΔT = L1 − L2
# =============================================================================
print('Figure 4: Height-level differences')

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle(
    'Vertical Temperature Gradient  ΔT = T(L1) − T(L2)\n'
    'BTU Campus Cottbus, 24 June 2026',
    fontsize=13, fontweight='bold',
)

# LEFT — scatter: T(L1) vs T(L2)
ax = axes[0]
set_bg(ax)
for name, df, col in datasets:
    ax.scatter(df['T_L1'], df['T_L2'],
               color=col, label=name, alpha=0.75, s=55, zorder=3)
lims = [22, 42]
ax.plot(lims, lims, 'k--', lw=1.2, alpha=0.5, label='1:1 line  (L1 = L2)')
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel('T at L1 / near-surface (°C)')
ax.set_ylabel('T at L2 / 2 m (°C)')
ax.set_title('L1 vs L2 Scatter\n(above 1:1 → surface is warmer)')
ax.legend()

# RIGHT — ΔT time series
ax = axes[1]
set_bg(ax)
ax.axhline(0, color='black', lw=1.2, ls='--', alpha=0.5, zorder=2,
           label='Zero  (L1 = L2)')
for name, df, col in datasets:
    diff = (df['T_L1'] - df['T_L2']).dropna()
    ax.plot(diff.index, diff, color=col, lw=2.2, zorder=3,
            label=f'{name}  (mean = {diff.mean():+.2f} °C)')
    ax.fill_between(diff.index, diff, 0,
                    where=(diff > 0), alpha=0.10, color=col, zorder=1)

ax.set_ylabel('ΔT = T(L1) − T(L2)  (°C)')
ax.set_title('ΔT over Time\n(positive → near-surface warmer than 2 m)')
ax.legend()
fmt_xaxis(ax)
fig.tight_layout()
save_fig(fig, 'fig4_height_diff.png')

# =============================================================================
# FIGURE 5 — Wind field (speed, direction, wind roses)
# =============================================================================
print('Figure 5: Wind field')

fig = plt.figure(figsize=(14, 9))
fig.suptitle(
    'Wind Field — All Locations\nBTU Campus Cottbus, 24 June 2026',
    fontsize=13, fontweight='bold',
)

# TOP-LEFT — wind speed time series
ax1 = fig.add_subplot(2, 2, 1)
set_bg(ax1)
ax1.plot(trees.index,    trees['WS_L1'],
         color=COLOR['Trees'],    lw=2,   ls='-',  label='Trees L1')
ax1.plot(trees.index,    trees['WS_L2'],
         color=COLOR['Trees'],    lw=1.5, ls='--', label='Trees L2', alpha=0.7)
ax1.plot(grass.index,    grass['WS_L1'],
         color=COLOR['Grass'],    lw=2,   ls='-',  label='Grass (1 level)')
ax1.plot(concrete.index, concrete['WS_L1'],
         color=COLOR['Concrete'], lw=2,   ls='-',  label='Concrete L1')
ax1.plot(concrete.index, concrete['WS_L2'],
         color=COLOR['Concrete'], lw=1.5, ls='--', label='Concrete L2', alpha=0.7)
ax1.set_ylabel('Wind Speed (m s$^{-1}$)')
ax1.set_title('Wind Speed over Time')
ax1.legend(ncol=2, fontsize=8)
ax1.set_ylim(bottom=0)
fmt_xaxis(ax1)

# TOP-RIGHT — wind direction scatter
ax2 = fig.add_subplot(2, 2, 2)
set_bg(ax2)
for name, df, col in datasets:
    if 'WD' in df.columns:
        ax2.scatter(df.index, df['WD'],
                    color=col, label=name, alpha=0.75, s=35, zorder=3)
ax2.set_yticks([0, 45, 90, 135, 180, 225, 270, 315, 360])
ax2.set_yticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'], fontsize=8)
ax2.set_ylabel('Wind Direction')
ax2.set_title('Wind Direction over Time')
ax2.legend()
ax2.set_ylim(-10, 370)
fmt_xaxis(ax2)

# BOTTOM — polar wind roses (angle = direction, radius = speed)
def wind_rose(fig_, subplot_pos, wd_series, ws_series, col, title):
    """
    Polar scatter: each dot = one 15-min record.
    Angle = wind direction (North at top, clockwise).
    Radius = wind speed (m/s).
    Dot color and size both encode wind speed.
    """
    ax = fig_.add_subplot(subplot_pos, polar=True)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    wd_valid = wd_series.dropna()
    ws_al    = ws_series.reindex(wd_valid.index).fillna(0)
    sizes    = (ws_al.values * 25 + 20).clip(10, 150)

    sc = ax.scatter(np.deg2rad(wd_valid.values), ws_al.values,
                    c=ws_al.values, cmap='YlOrRd',
                    s=sizes, alpha=0.75, vmin=0, vmax=3)

    ax.set_title(title, fontsize=10, fontweight='bold', pad=16)
    ax.set_rlabel_position(135)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.grid(True, alpha=0.3)

    cbar = fig_.colorbar(sc, ax=ax, pad=0.12, fraction=0.04)
    cbar.set_label('m/s', fontsize=8)

wind_rose(fig, 223, trees['WD'],    trees['WS_L1'],    COLOR['Trees'],    'Wind Rose — Trees (L1)')
wind_rose(fig, 224, concrete['WD'], concrete['WS_L1'], COLOR['Concrete'], 'Wind Rose — Concrete (L1)')

fig.tight_layout()
save_fig(fig, 'fig5_wind.png')

# =============================================================================
# FIGURE 6 — Statistical distributions (box plots)
# =============================================================================
print('Figure 6: Statistical distributions (box plots)')

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.suptitle(
    'Statistical Distribution of Temperature and Humidity\n'
    'BTU Campus Cottbus, 24 June 2026',
    fontsize=13, fontweight='bold',
)

labels = ['Trees\nL1', 'Trees\nL2', 'Grass\nL1', 'Grass\nL2',
          'Concrete\nL1', 'Concrete\nL2']

box_colors = [
    COLOR['Trees'], COLOR['Trees'],
    COLOR['Grass'], COLOR['Grass'],
    COLOR['Concrete'], COLOR['Concrete'],
]

t_groups  = [trees['T_L1'].dropna(),    trees['T_L2'].dropna(),
             grass['T_L1'].dropna(),    grass['T_L2'].dropna(),
             concrete['T_L1'].dropna(), concrete['T_L2'].dropna()]

rh_groups = [trees['RH_L1'].dropna(),   trees['RH_L2'].dropna(),
             grass['RH_L1'].dropna(),   grass['RH_L2'].dropna(),
             concrete['RH_L1'].dropna(), concrete['RH_L2'].dropna()]

for ax, groups, ylab, title in zip(
        axes,
        [t_groups, rh_groups],
        ['Air Temperature (°C)', 'Relative Humidity (%)'],
        ['Temperature Distribution', 'Humidity Distribution']):

    set_bg(ax)
    bp = ax.boxplot(
        groups,
        patch_artist=True,
        notch=False,
        widths=0.55,
        medianprops=dict(color='black', lw=2.5),
        whiskerprops=dict(lw=1.5),
        capprops=dict(lw=1.5),
        flierprops=dict(marker='o', markersize=5, alpha=0.5),
    )

    for patch, c in zip(bp['boxes'], box_colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.55)

    # Diamond marker at mean value
    for i, grp in enumerate(groups):
        ax.scatter(i + 1, grp.mean(),
                   marker='D', color='black', s=40, zorder=5,
                   label='Mean' if i == 0 else '')

    ax.set_xticks(range(1, 7))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(ylab)
    ax.set_title(title)
    ax.yaxis.grid(True, ls='--', alpha=0.4)
    ax.set_axisbelow(True)

legend_handles = [
    Patch(facecolor=COLOR['Trees'],    alpha=0.6, label='Trees'),
    Patch(facecolor=COLOR['Grass'],    alpha=0.6, label='Grass'),
    Patch(facecolor=COLOR['Concrete'], alpha=0.6, label='Concrete'),
    plt.scatter([], [], marker='D', color='black', s=40, label='Mean'),
]
fig.legend(handles=legend_handles, loc='lower center', ncol=4,
           bbox_to_anchor=(0.5, -0.04), fontsize=9, framealpha=0.9)
fig.tight_layout()
save_fig(fig, 'fig6_boxplots.png')

# =============================================================================
# FIGURE 7 — DWD Radiation + near-surface temperature (2-panel)
# =============================================================================
print('Figure 7: DWD radiation + temperature')

fig, (ax_rad, ax_temp) = plt.subplots(2, 1, figsize=(12, 9), sharex=False)
fig.suptitle(
    'Solar Radiation & Near-Surface Temperature\n'
    'DWD Lindenberg (ID 03015, 57 km NE of Cottbus) — 24 June 2026',
    fontsize=13, fontweight='bold',
)

# ── TOP: irradiance ──────────────────────────────────────────────────────────
ax_rad.set_facecolor(BG)

ax_rad.fill_between(rad.index, rad['GHI'], alpha=0.30, color='#FF8C00', zorder=1)
ax_rad.plot(rad.index, rad['GHI'],
            color='#CC5500', lw=2.5, zorder=3,
            label='GHI measured  (DWD Lindenberg)')

if not rad['DHI'].isna().all():
    ax_rad.fill_between(rad.index, rad['DHI'], alpha=0.30, color='#4682B4', zorder=1)
    ax_rad.plot(rad.index, rad['DHI'],
                color='#1A5276', lw=2.0, ls='--', zorder=3,
                label='DHI measured  (DWD Lindenberg)')

if has_cs:
    ax_rad.plot(cs_15.index, cs_15['GHI_cs'],
                color='#888', lw=2.0, ls=':', zorder=2,
                label=f'GHI clear-sky  (pvlib Ineichen, Cottbus)  peak = {peak_cs:.0f} W/m²')
    ax_rad.fill_between(
        cs_15.index,
        rad['GHI'].reindex(cs_15.index, method='nearest'),
        cs_15['GHI_cs'],
        alpha=0.06, color='grey', zorder=0,
        label='Cloud attenuation  (~94 %)',
    )

ax_rad.set_ylabel('Irradiance  (W m$^{-2}$)')
ax_rad.set_ylim(bottom=0)
ax_rad.legend(loc='upper right', fontsize=8.5)
ax_rad.set_title('Solar Irradiance  (GHI = Global Horizontal,  DHI = Diffuse)', pad=4)

ax_rad.text(
    0.01, 0.91,
    'OVERCAST CONDITIONS\nGHI << clear-sky potential',
    transform=ax_rad.transAxes, fontsize=8.5, color='#7a4000',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff3cd', alpha=0.9),
)

pk_idx = rad['GHI'].idxmax()
pk_val = rad['GHI'].max()
ax_rad.annotate(
    f'Peak GHI\n{pk_val:.0f} W/m²\n{pk_idx.strftime("%H:%M")} CEST',
    xy=(pk_idx, pk_val), xytext=(25, 8), textcoords='offset points',
    fontsize=8,
    arrowprops=dict(arrowstyle='->', color='#CC5500', lw=1.2),
    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9),
)

ax_rad.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax_rad.xaxis.set_major_locator(mdates.HourLocator())

# ── BOTTOM: near-surface temperature ────────────────────────────────────────
ax_temp.set_facecolor(BG)
for name, df, col in datasets:
    if 'T_L1' in df.columns:
        ax_temp.plot(df.index, df['T_L1'],
                     color=col, lw=2.2, label=f'{name}  L1')

ax_temp.set_ylabel('Air Temperature  (°C)')
ax_temp.set_title('Near-Surface Temperature (L1) — All Locations', pad=4)
ax_temp.legend(loc='upper left')
fmt_xaxis(ax_temp)

fig.tight_layout()
save_fig(fig, 'fig7_radiation_DWD.png')

# =============================================================================
# FIGURE 8 — GHI vs. Relative Humidity (dual-axis)
# =============================================================================
print('Figure 8: GHI vs. relative humidity')

fig, ax_ghi = plt.subplots(figsize=(12, 5))
ax_rh = ax_ghi.twinx()
set_bg(ax_ghi)

# Left axis: GHI
ax_ghi.fill_between(rad.index, rad['GHI'], alpha=0.20, color='#FF8C00', zorder=1)
ax_ghi.plot(rad.index, rad['GHI'],
            color='#CC5500', lw=2.5, zorder=3,
            label='GHI measured  (DWD Lindenberg)')
if has_cs:
    ax_ghi.plot(cs_15.index, cs_15['GHI_cs'],
                color='#aaa', lw=1.8, ls=':', zorder=2,
                label='GHI clear-sky  (Cottbus)')
ax_ghi.set_ylabel('Global Irradiance  (W m$^{-2}$)', color='#CC5500')
ax_ghi.tick_params(axis='y', colors='#CC5500')
ax_ghi.set_ylim(bottom=0)

# Right axis: RH per location
for name, df, col, ls in [
        ('Trees',    trees,    COLOR['Trees'],    '-'),
        ('Grass',    grass,    COLOR['Grass'],    '--'),
        ('Concrete', concrete, COLOR['Concrete'], ':')]:
    if 'RH_L1' in df.columns:
        ax_rh.plot(df.index, df['RH_L1'],
                   color=col, lw=2.0, ls=ls,
                   label=f'RH  {name}  L1')

ax_rh.set_ylabel('Relative Humidity  (%)')
ax_rh.set_ylim(15, 75)

# Combined legend from both axes
lines_ghi, labels_ghi = ax_ghi.get_legend_handles_labels()
lines_rh,  labels_rh  = ax_rh.get_legend_handles_labels()
ax_ghi.legend(lines_ghi + lines_rh, labels_ghi + labels_rh,
              loc='upper left', fontsize=8.5, ncol=2, framealpha=0.9)

fmt_xaxis(ax_ghi)
ax_ghi.set_title(
    'Solar Radiation (DWD Lindenberg) vs. Relative Humidity — 24 June 2026',
    fontweight='bold',
)
fig.tight_layout()
save_fig(fig, 'fig8_radiation_RH.png')

# =============================================================================
# DONE
# =============================================================================
print('\n' + '=' * 60)
print('All 8 figures saved to:', OUT_DIR)
print('=' * 60)
print('  fig1_temperature.png   - Temperature time series (3 panels per location)')
print('  fig2_humidity.png      - Relative humidity time series (3 panels)')
print('  fig3_comparison.png    - All locations on shared axes (T and RH)')
print('  fig4_height_diff.png   - Vertical gradient DeltaT (L1 - L2)')
print('  fig5_wind.png          - Wind speed, direction + polar wind roses')
print('  fig6_boxplots.png      - Statistical box plots (T and RH)')
print('  fig7_radiation_DWD.png - DWD GHI/DHI + clear-sky + temperature')
print('  fig8_radiation_RH.png  - GHI vs. relative humidity (dual-axis)')