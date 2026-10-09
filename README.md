# -*- coding: utf-8 -*-
"""
Build final academic PDF report for 13046 Microclimates Final Exercise.
No Python code in output. Professional layout with figures and tables.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus import ListFlowable, ListItem
import os

OUT = '/mnt/user-data/outputs/FinalEX_Report_Bahadori.pdf'
FIG = '/mnt/user-data/outputs/figures/'

# ── Page layout ──────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    title='Microclimate Analysis BTU Cottbus',
    author='Matin Bahadori',
)

W = A4[0] - 5*cm   # usable text width

# ── Colour palette ────────────────────────────────────────────────────────────
DARK    = colors.HexColor('#1a1a2e')
ACCENT  = colors.HexColor('#16213e')
BLUE    = colors.HexColor('#0f3460')
LIGHT   = colors.HexColor('#e8f4f8')
MUTED   = colors.HexColor('#555555')
GREEN   = colors.HexColor('#2CA02C')
OLIVE   = colors.HexColor('#7c7c00')
RED     = colors.HexColor('#D62728')
HEADBG  = colors.HexColor('#0f3460')
ROWALT  = colors.HexColor('#f0f6fa')

# ── Styles ────────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def sty(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

Title   = sty('RTitle',  'Title',   fontSize=20, textColor=DARK,
               spaceAfter=4, leading=24, alignment=TA_CENTER)
Sub     = sty('RSub',    'Normal',  fontSize=12, textColor=MUTED,
               spaceAfter=2, leading=16, alignment=TA_CENTER)
Auth    = sty('RAuth',   'Normal',  fontSize=11, textColor=DARK,
               spaceAfter=2, leading=14, alignment=TA_CENTER)
H1      = sty('RH1',     'Heading1', fontSize=13, textColor=colors.white,
               spaceAfter=6, spaceBefore=14, leading=17,
               backColor=HEADBG, leftIndent=-0.3*cm, rightIndent=-0.3*cm,
               borderPad=5)
H2      = sty('RH2',     'Heading2', fontSize=11, textColor=BLUE,
               spaceAfter=4, spaceBefore=10, leading=15, leftIndent=0)
Body    = sty('RBody',   'Normal',   fontSize=10, leading=15,
               spaceAfter=6, alignment=TA_JUSTIFY, textColor=colors.black)
Cap     = sty('RCap',    'Normal',   fontSize=8.5, leading=11,
               spaceAfter=10, alignment=TA_CENTER, textColor=MUTED,
               fontName='Helvetica-Oblique')
THead   = sty('RTH',     'Normal',   fontSize=9, fontName='Helvetica-Bold',
               alignment=TA_CENTER, textColor=colors.white)
TCell   = sty('RTC',     'Normal',   fontSize=9, alignment=TA_CENTER,
               leading=12)
TLeft   = sty('RTL',     'Normal',   fontSize=9, alignment=TA_LEFT,
               leading=12)
Ref     = sty('RRef',    'Normal',   fontSize=9, leading=13,
               spaceAfter=4, leftIndent=1*cm, firstLineIndent=-1*cm,
               textColor=MUTED)
Note    = sty('RNote',   'Normal',   fontSize=8.5, leading=12,
               textColor=MUTED, fontName='Helvetica-Oblique',
               leftIndent=0.5*cm, spaceAfter=8)

def fig(path, width_cm, caption):
    """Return image + caption as a KeepTogether block."""
    img = Image(path, width=width_cm*cm, height=width_cm*cm*0.62)
    return KeepTogether([
        img,
        Paragraph(caption, Cap),
    ])

def table(data, col_widths, header=True):
    """Styled table. First row treated as header if header=True."""
    rows = []
    for r, row in enumerate(data):
        cells = []
        for c, val in enumerate(row):
            s = THead if (header and r == 0) else (TLeft if c == 0 else TCell)
            cells.append(Paragraph(str(val), s))
        rows.append(cells)

    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADBG),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ROWALT]),
        ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#ccddee')),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ])
    return Table(rows, colWidths=[w*cm for w in col_widths], style=style,
                 hAlign='CENTER', repeatRows=1)

# ── STORY ─────────────────────────────────────────────────────────────────────
story = []

# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 2.5*cm))
story.append(Paragraph('Microclimate Analysis of Urban Surface Types', Title))
story.append(Paragraph('at BTU Campus Cottbus', Title))
story.append(Spacer(1, 0.6*cm))
story.append(HRFlowable(width='100%', thickness=2, color=BLUE))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph('Final Exercise - 13046 Microclimates', Sub))
story.append(Paragraph('SoSe 2026 &nbsp;|&nbsp; Prof. Dr. Katja Trachte', Sub))
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph('Matin Bahadori', Auth))
story.append(Paragraph('Matrikel-Nr. 5006380', Auth))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('Brandenburg University of Technology Cottbus-Senftenberg', Auth))
story.append(Paragraph('Faculty of Environment and Natural Sciences', Auth))
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph('Field campaign: 24 June 2026 &nbsp;|&nbsp; 08:45 – 16:30 CEST', Sub))
story.append(Paragraph('BTU Campus Cottbus &nbsp;|&nbsp; Three measurement locations', Sub))
story.append(Spacer(1, 1.5*cm))
story.append(HRFlowable(width='60%', thickness=1, color=colors.HexColor('#ccddee')))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════════════
story.append(Paragraph('1. Introduction', H1))

story.append(Paragraph(
    'Urban areas are characterised by a complex mosaic of surface materials that interact '
    'with solar radiation, atmospheric moisture, and local air flow in fundamentally '
    'different ways. Impervious surfaces such as concrete and asphalt absorb and store '
    'large quantities of shortwave radiation, releasing the accumulated heat slowly as '
    'longwave radiation and sensible heat flux throughout the day and well into the night. '
    'Vegetated surfaces, by contrast, moderate near-surface temperatures through '
    'evapotranspiration, shading, and the higher specific heat capacity of moist soil. '
    'The resulting patchwork of warm and cool zones defines the urban heat island effect '
    'at its finest scale - the microclimate.', Body))

story.append(Paragraph(
    'This report presents the results of a field campaign conducted on 24 June 2026 at '
    'the Brandenburg University of Technology (BTU) Campus in Cottbus, Germany. '
    'Microclimatological variables - air temperature (T<sub>a</sub>), relative humidity '
    '(RH), and wind speed/direction - were recorded manually at 15-minute intervals '
    'across three contrasting surface types: a grove of trees, an open grass area, and '
    'an exposed concrete surface. Measurements were made at two height levels at each '
    'location to capture vertical structure in the near-surface boundary layer.', Body))

story.append(Paragraph(
    'The broader meteorological context for the campaign day was characterised by an '
    'overcast sky associated with a passing occluded front (see synoptic chart, Fig. 2 '
    'of the assignment sheet). This reduced the incoming global horizontal irradiance '
    '(GHI) to only about 6% of the theoretical clear-sky value, fundamentally dampening '
    'the temperature contrasts that would be expected under full sunshine. Despite these '
    'muted forcing conditions, clear and systematic differences between surface types '
    'were nonetheless observed, underscoring the persistent role of surface properties '
    'in shaping local climates.', Body))

story.append(Paragraph(
    'The three overarching research questions addressed in this report are:', Body))

story.append(ListFlowable([
    ListItem(Paragraph(
        'What is the temporal development of microclimatological conditions '
        '(T<sub>a</sub>, RH, wind) from morning through afternoon?', Body), bulletText='1.'),
    ListItem(Paragraph(
        'What is the direct influence of surface and environmental properties '
        'on those conditions?', Body), bulletText='2.'),
    ListItem(Paragraph(
        'How does surface type influence near-surface heat generation?', Body), bulletText='3.'),
], bulletType='bullet', leftIndent=20, spaceBefore=2, spaceAfter=8))

# ═══════════════════════════════════════════════════════════════════════════════
# 2. DATA & METHODS
# ═══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('2. Data and Methods', H1))

story.append(Paragraph('2.1  Field Measurements', H2))
story.append(Paragraph(
    'Handheld sensors (TESTO 480 combined temperature/humidity probes) were deployed '
    'at three locations on the BTU campus (Figure 1 of the assignment sheet). At each '
    'site, sensors were placed at two height levels: Level 1 (L1) near the surface '
    '(approximately 0.05–0.10 m above ground or the dominant surface) and Level 2 (L2) '
    'at 2 m height. Wind speed and direction were recorded at the same heights where '
    'instrument availability permitted. At the Grass location, wind data were available '
    'at one level only; the exact measurement height was not documented in the field '
    'protocol. Observations began at 08:45 CEST and ended at 16:30 CEST, with a '
    '15-minute recording interval, yielding up to 32 time steps per variable. '
    'The Concrete location has a missing 08:45 record, giving 31 usable time steps '
    'for that site.', Body))

story.append(Paragraph('2.2  Radiation Data (DWD)', H2))
story.append(Paragraph(
    'Incoming solar radiation was not measured directly during the campaign. '
    'Data from the German Weather Service (Deutscher Wetterdienst, DWD) automatic '
    'weather station at Lindenberg (Station ID 03015, 52.21 degrees N, 14.12 degrees E, '
    '98 m a.s.l.) were used as a proxy. Lindenberg is located approximately 57 km '
    'north-east of Cottbus. Under the stratiform overcast conditions that prevailed on '
    '24 June 2026, global horizontal irradiance is horizontally uniform over distances '
    'of hundreds of kilometres, making the Lindenberg record directly representative '
    'of conditions at the campaign site. The DWD Cottbus station (ID 00880) has been '
    'offline since February 2026 and could not be used. Ten-minute DWD records were '
    'resampled to 15-minute means and converted from UTC to Central European Summer '
    'Time (CEST = UTC+2) for consistency with the field data.', Body))

story.append(Paragraph('2.3  Clear-Sky Reference', H2))
story.append(Paragraph(
    'A theoretical clear-sky GHI time series was computed for the Cottbus site '
    '(51.758 degrees N, 14.318 degrees E, 69 m a.s.l.) using the Ineichen model as '
    'implemented in the pvlib Python library (Holmgren et al., 2018). The Linke '
    'turbidity coefficient was taken from the SoDa McClear climatology. This reference '
    'curve provides the upper bound of possible irradiance and allows quantification '
    'of the cloud attenuation fraction.', Body))

story.append(Paragraph('2.4  Analysis Methods', H2))
story.append(Paragraph(
    'Descriptive statistics (minimum, maximum, mean, standard deviation) were computed '
    'for T<sub>a</sub> and RH at both height levels for each location, covering the full '
    'campaign period. Vertical temperature gradients were quantified as '
    'Delta-T = T(L1) minus T(L2). Positive Delta-T indicates that the near-surface layer '
    'is warmer than the air at 2 m height, consistent with upward sensible heat flux from '
    'a warm surface. Negative Delta-T indicates the opposite, typical under canopy shading '
    'or evaporative cooling. Wind speed, direction, and relative humidity were analysed '
    'in relation to the radiation record to characterise the diurnal cycle and '
    'cross-location differences.', Body))

# ═══════════════════════════════════════════════════════════════════════════════
# 3. RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('3. Results', H1))

story.append(Paragraph('3.1  Meteorological Context: Solar Radiation', H2))
story.append(Paragraph(
    'The synoptic situation on 24 June 2026 was dominated by an occluded frontal system '
    'passing over central Germany, producing near-continuous overcast skies. The DWD '
    'Lindenberg record confirms very low irradiance throughout the campaign window '
    '(Figure 1). Global horizontal irradiance (GHI) averaged only 46.8 W m<super>-2</super> '
    'over the field hours, with a maximum of 54.2 W m<super>-2</super> - just 6.4% of '
    'the theoretical clear-sky peak of 841 W m<super>-2</super> computed for the '
    'Cottbus location using the Ineichen model. Diffuse horizontal irradiance (DHI) '
    'represented the dominant component of the total, consistent with a thick, '
    'optically uniform cloud layer. The practical implication for the campaign is '
    'that radiative forcing was near-absent: no surface heated strongly under direct '
    'sunlight, which compressed the temperature differences between locations and '
    'height levels compared with what would be observed on a clear day.', Body))

story.append(fig(FIG+'fig7_radiation_DWD.png', 16,
    'Figure 1. Solar irradiance (top) measured at DWD Lindenberg station on 24 June 2026. '
    'Orange: global horizontal irradiance (GHI); blue dashed: diffuse horizontal irradiance (DHI); '
    'grey dotted: theoretical clear-sky GHI (Ineichen model, Cottbus). '
    'The grey shading represents cloud attenuation (~94% of potential). '
    'Bottom panel shows near-surface air temperature at all three locations.'))

story.append(Paragraph('3.2  Air Temperature: Descriptive Statistics', H2))
story.append(Paragraph(
    'Table 1 summarises the temperature statistics across all locations and height '
    'levels for the full campaign period. The Concrete location was consistently the '
    'warmest, with a near-surface mean of 33.2 degrees C and a campaign maximum of '
    '38.7 degrees C - the highest value recorded at any location or height. '
    'Trees showed intermediate temperatures (mean L1 = 31.3 degrees C), while Grass '
    'was the coolest on average (mean L1 = 30.7 degrees C). The standard deviations '
    'reveal that Concrete also exhibited the greatest variability (std = 3.59 degrees C '
    'at L1), reflecting its strong coupling to the limited but nonzero radiative forcing '
    'during brief cloud breaks. Trees and Grass showed lower variability '
    '(std = 2.35 and 2.73 degrees C respectively), consistent with thermal buffering '
    'by vegetation.', Body))

story.append(table([
    ['Location', 'Level', 'Min (deg C)', 'Max (deg C)', 'Mean (deg C)', 'Std (deg C)'],
    ['Trees',    'L1 (~0 m)',  '25.1', '35.2', '31.3', '2.35'],
    ['Trees',    'L2 (2 m)',   '25.2', '37.5', '31.7', '2.24'],
    ['Grass',    'L1 (~0 m)',  '25.1', '36.5', '30.7', '2.73'],
    ['Grass',    'L2 (2 m)',   '25.2', '34.9', '30.4', '2.66'],
    ['Concrete', 'L1 (~0 m)',  '25.9', '38.7', '33.2', '3.59'],
    ['Concrete', 'L2 (2 m)',   '25.9', '36.0', '32.1', '2.74'],
], [3.0, 2.5, 2.5, 2.5, 2.7, 2.5]))
story.append(Paragraph('Table 1. Air temperature statistics for all locations and height levels, 24 June 2026, 08:45–16:30 CEST.', Cap))

story.append(Spacer(1, 0.3*cm))
story.append(fig(FIG+'fig1_temperature.png', 16,
    'Figure 2. Air temperature time series at Trees (top), Grass (middle), and Concrete (bottom). '
    'Solid lines show Level 1 (near-surface); dashed lines show Level 2 (2 m). '
    'Shaded band between the two levels highlights the vertical gradient.'))

story.append(Paragraph('3.3  Vertical Temperature Gradient', H2))
story.append(Paragraph(
    'The vertical temperature gradient Delta-T = T(L1) minus T(L2) reveals the '
    'direction of near-surface energy exchange and is particularly diagnostic of '
    'surface heating behaviour (Table 2). At the Concrete location, L1 was on average '
    '1.18 degrees C warmer than L2, with individual peaks reaching +4.3 degrees C. '
    'This positive gradient - warmer near the surface, cooler above - is the classical '
    'signature of an unstable surface layer driven by sensible heat flux from a warm '
    'impervious substrate. Even under the overcast skies of 24 June 2026, stored heat '
    'in the concrete slab was sufficient to maintain this structure throughout '
    'most of the campaign.', Body))

story.append(Paragraph(
    'The Grass location showed a small positive gradient (mean Delta-T = +0.34 degrees C), '
    'indicating weak but persistent near-surface warming. The Trees location reversed '
    'this pattern: mean Delta-T was -0.38 degrees C, meaning L2 was slightly warmer '
    'than L1. This temperature inversion below the canopy is consistent with radiative '
    'shading by the tree crowns and evaporative cooling at the soil surface. '
    'The canopy intercepts incoming radiation and prevents direct solar heating of '
    'the underlying ground, while transpiration from leaves and soil moisture '
    'evaporation cool the sub-canopy air.', Body))

story.append(table([
    ['Location', 'Mean Delta-T (deg C)', 'Max Delta-T (deg C)', 'Min Delta-T (deg C)', 'Interpretation'],
    ['Trees',    '-0.38', '+3.70', '-3.10', 'Canopy cooling; L2 slightly warmer'],
    ['Grass',    '+0.34', '+2.30', '-1.70', 'Weak near-surface warming'],
    ['Concrete', '+1.18', '+4.30', '-2.30', 'Strong upward sensible heat flux'],
], [2.8, 3.2, 3.2, 3.2, 4.8]))
story.append(Paragraph('Table 2. Vertical temperature gradient Delta-T = T(L1) minus T(L2). Positive values indicate L1 warmer than L2.', Cap))

story.append(fig(FIG+'fig4_height_diff.png', 16,
    'Figure 3. Left: scatter plot of L1 versus L2 temperature for all three locations. Points above '
    'the 1:1 line indicate that the near-surface level is warmer. Right: time series of Delta-T '
    'for each location. Concrete consistently shows the largest positive gradient.'))

story.append(Paragraph('3.4  Relative Humidity', H2))
story.append(Paragraph(
    'Relative humidity generally followed the inverse of the temperature pattern, '
    'as expected from the Clausius-Clapeyron relation: as air warms, its saturation '
    'vapour pressure increases, lowering RH if the absolute moisture content '
    'does not change proportionally. Table 3 confirms this: Concrete, the warmest '
    'location, recorded the lowest mean RH at L1 (32.9%), while Trees and Grass '
    'showed higher values (37.4% and 36.5% respectively).', Body))

story.append(Paragraph(
    'The most striking feature of the RH record is the high variability and elevated '
    'maxima at the Grass location (max L1 = 63.9%, std = 8.94%) compared with Trees '
    '(max = 54.2%, std = 6.66%) and Concrete (max = 52.6%, std = 8.31%). '
    'The high Grass maxima in the morning hours reflect dew on the grass surface '
    'and higher soil moisture, which evaporated as the day warmed. The broader '
    'diurnal range at Grass and Concrete compared to Trees also reflects the '
    'stronger coupling of these open surfaces to the (albeit limited) radiative '
    'forcing of the day.', Body))

story.append(table([
    ['Location', 'Level', 'Min (%)', 'Max (%)', 'Mean (%)', 'Std (%)'],
    ['Trees',    'L1', '28.6', '54.2', '37.4', '6.66'],
    ['Trees',    'L2', '27.0', '52.7', '33.4', '6.24'],
    ['Grass',    'L1', '25.2', '63.9', '36.5', '8.94'],
    ['Grass',    'L2', '24.1', '63.2', '36.2', '9.05'],
    ['Concrete', 'L1', '23.3', '52.6', '32.9', '8.31'],
    ['Concrete', 'L2', '23.8', '51.2', '32.7', '7.58'],
], [3.0, 2.5, 2.5, 2.5, 2.7, 2.5]))
story.append(Paragraph('Table 3. Relative humidity statistics for all locations and height levels.', Cap))

story.append(fig(FIG+'fig8_radiation_RH.png', 16,
    'Figure 4. Dual-axis plot showing measured GHI from DWD Lindenberg (left axis, orange) '
    'and relative humidity at Level 1 for all three locations (right axis). '
    'The general inverse relationship between irradiance and RH is visible despite '
    'the subdued radiation signal.'))

story.append(Paragraph('3.5  Cross-Location Comparison and Statistical Distribution', H2))
story.append(Paragraph(
    'Figure 5 places all three locations on shared temperature and humidity axes, '
    'directly visualising the systematic offset between surface types throughout '
    'the campaign. The ranking Concrete > Trees > Grass in temperature, and '
    'Trees > Grass > Concrete in relative humidity, was maintained consistently '
    'from morning through afternoon. The box plots in Figure 6 confirm that the '
    'distributions are largely non-overlapping for temperature but more similar for '
    'RH, reflecting the greater temperature contrast driven by surface thermal '
    'properties and the more uniform moisture availability under the moist '
    'overcast conditions.', Body))

story.append(fig(FIG+'fig3_comparison.png', 16,
    'Figure 5. Cross-location comparison. Left: air temperature at L1 (solid) and L2 (dashed) '
    'for all three locations on shared axes. Right: relative humidity. '
    'The ranking Concrete > Trees > Grass in temperature is maintained throughout the day.'))

story.append(fig(FIG+'fig6_boxplots.png', 16,
    'Figure 6. Box plots of temperature (left) and relative humidity (right) distributions '
    'for all locations and height levels. Diamonds mark the campaign mean. '
    'Concrete shows the highest temperatures and widest spread; '
    'Grass shows the highest RH variability.'))

story.append(PageBreak())
story.append(Paragraph('3.6  Wind Field', H2))
story.append(Paragraph(
    'Wind speeds were generally low across all locations throughout the campaign '
    '(Figure 7), consistent with the weak pressure gradient associated with the '
    'occluded frontal system. Mean wind speeds remained below 1.5 m s<super>-1</super> '
    'at most measurement levels, with occasional gusts to approximately 2.5 m s<super>-1</super>. '
    'No systematic increase in wind speed with the afternoon temperature peak was observed, '
    'suggesting that local thermally-driven flows were not strong enough to manifest '
    'clearly under the overcast, near-calm conditions.', Body))

story.append(Paragraph(
    'Wind direction was variable, rotating between south-westerly and north-westerly '
    'sectors, consistent with the passage of frontal systems. The Trees location '
    'shows generally lower wind speeds at L1 compared with L2, reflecting canopy '
    'drag attenuation of the flow. At Concrete, L1 and L2 speeds were more similar, '
    'consistent with the aerodynamically smooth character of the paved surface. '
    'Wind roses for Trees and Concrete (lower panels of Figure 7) confirm the '
    'predominant south-west to west flow direction during the measurement period.', Body))

story.append(fig(FIG+'fig5_wind.png', 16,
    'Figure 7. Wind field summary. Top left: wind speed time series at all locations and levels. '
    'Top right: wind direction scatter. Bottom: polar wind roses for Trees L1 and Concrete L1, '
    'with dot colour and size encoding wind speed (m/s).'))

# ═══════════════════════════════════════════════════════════════════════════════
# 4. DISCUSSION
# ═══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('4. Discussion', H1))

story.append(Paragraph('4.1  Research Question 1: Temporal Development of Microclimatic Conditions', H2))
story.append(Paragraph(
    'The temporal evolution of temperature, humidity, and wind on 24 June 2026 was '
    'strongly shaped by the absence of significant solar radiation. Under clear-sky '
    'conditions, a pronounced diurnal cycle would be expected: temperatures rising '
    'sharply from mid-morning to a peak around 13:00–15:00 CEST as GHI reaches '
    'its maximum (~841 W m<super>-2</super>), with a corresponding decrease in RH. '
    'On the campaign day, GHI never exceeded 54 W m<super>-2</super>, suppressing '
    'this cycle substantially. Nonetheless, a gradual warming was observed at all '
    'locations between 09:00 and 14:00 CEST, driven by residual diffuse radiation, '
    'sensible heat advection, and the thermal inertia of the surfaces. This warming '
    'was most pronounced at Concrete (+8–10 degrees C range) and weakest at Trees '
    '(+7–8 degrees C range), consistent with the higher thermal admittance and lower '
    'albedo of impervious surfaces.', Body))

story.append(Paragraph(
    'The inverse humidity response - decreasing RH as temperatures rise - was clearly '
    'visible at all locations, though again dampened compared to a clear day. '
    'The morning period (08:45–10:00) saw the highest RH values, particularly at Grass '
    '(up to 63.9%), likely owing to moisture evaporating from the dew-wetted surface. '
    'The absence of strong radiative forcing meant that the expected afternoon '
    'temperature peak was gentler and shifted slightly later than on a clear summer day. '
    'Wind speeds showed no systematic diurnal signal, remaining low and variable '
    'throughout, consistent with synoptically forced rather than thermally driven flow.', Body))

story.append(Paragraph('4.2  Research Question 2: Influence of Environmental Properties', H2))
story.append(Paragraph(
    'The direct influence of surface and environmental properties on microclimate is '
    'most clearly expressed through the surface energy balance. Each surface type '
    'partitions the available energy between sensible heat flux (H), latent heat flux '
    '(LE), and ground heat storage (G) in a characteristic way, summarised by the '
    'Bowen ratio (B = H / LE).', Body))

story.append(Paragraph(
    'The Concrete surface, being impervious and dry, cannot support evapotranspiration. '
    'Virtually all absorbed radiation is converted to sensible heat (high Bowen ratio, '
    'B >> 1), driving surface and near-surface air temperatures upward. The high '
    'thermal admittance (mu = sqrt(lambda * rho * c_p)) of concrete also means that '
    'heat penetrates deeply into the material and is released slowly, sustaining '
    'elevated temperatures even after radiation decreases. This explains both the '
    'highest mean temperature (33.2 degrees C) and the strongest vertical gradient '
    '(mean Delta-T = +1.18 degrees C) observed at this location.', Body))

story.append(Paragraph(
    'Vegetated surfaces - Trees and Grass - partition energy very differently. '
    'Transpiration through stomata and direct evaporation from wet leaf and soil '
    'surfaces converts a large fraction of absorbed energy into latent heat (low '
    'Bowen ratio), cooling the air in the process. This latent heat pathway is '
    'particularly effective for the Trees location, where the deep root system '
    'maintains a sustained moisture supply and the multi-layered canopy creates '
    'an effective boundary layer that decouples near-surface air from the '
    'overlying atmosphere. The resulting negative Delta-T (-0.38 degrees C on average) '
    'confirms that the near-surface air at Trees is cooled relative to the air above, '
    'a pattern consistent with theoretical expectations for a moist, shaded surface.', Body))

story.append(Paragraph(
    'The Grass location occupies an intermediate position. While capable of '
    'evapotranspiration, a short grass sward provides less shading and aerodynamic '
    'roughness than a tree canopy, and its shallow root system is more susceptible '
    'to drying. Nevertheless, the early-morning moisture signal (high RH, peak 63.9%) '
    'and moderate Delta-T (+0.34 degrees C) suggest that latent cooling was active, '
    'especially before the soil surface dried during the midday hours.', Body))

story.append(Paragraph('4.3  Research Question 3: Surface Properties and Heat Generation', H2))
story.append(Paragraph(
    'The comparison between locations demonstrates that surface type is the dominant '
    'control on near-surface heat generation under the conditions observed, even in '
    'the absence of strong direct radiation. The thermal hierarchy '
    '(Concrete > Trees > Grass in temperature, reversed in humidity) persisted '
    'throughout the 8-hour campaign with only minor deviations.', Body))

story.append(Paragraph(
    'From an urban heat island perspective, these results are significant. Even on an '
    'overcast day when radiative forcing is minimal, the concrete surface was '
    '~2.5 degrees C warmer on average than the vegetated locations. On a clear summer '
    'day with GHI approaching 841 W m<super>-2</super>, the temperature differential '
    'between impervious and vegetated surfaces would be substantially larger - '
    'potentially 5–10 degrees C at the surface and 2–4 degrees C in the near-surface '
    'air layer. This underscores the importance of green infrastructure in urban '
    'planning as a mitigation strategy for heat stress.', Body))

story.append(Paragraph(
    'The two height levels provide additional insight. The convergence of L1 and L2 '
    'temperatures at Trees (mean difference only 0.38 degrees C) compared with the '
    'larger divergence at Concrete (1.18 degrees C) suggests that the mixing and '
    'turbulent exchange processes differ fundamentally between the two environments. '
    'The tree canopy creates a near-neutral or slightly stable sub-canopy microclimate, '
    'while the heated concrete surface drives convective mixing that couples the '
    'near-surface and elevated air layers through a positive lapse rate.', Body))

story.append(Paragraph(
    'It should be acknowledged that the overcast conditions on the campaign day limit '
    'the generalisability of the quantitative results. Systematically higher '
    'irradiance would amplify all observed signals. Additionally, the single-day '
    'snapshot prevents assessment of day-to-day variability, and the relatively '
    'coarse 15-minute resolution may miss short-duration extreme events such as '
    'brief cloud breaks or sudden wind shifts.', Body))

# ═══════════════════════════════════════════════════════════════════════════════
# 5. CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('5. Conclusion', H1))

story.append(Paragraph(
    'This study quantified microclimatic differences between three contrasting urban '
    'surface types - trees, grass, and concrete - at the BTU Cottbus campus during a '
    'field campaign on 24 June 2026. Despite heavily overcast conditions that limited '
    'solar forcing to approximately 6% of the theoretical clear-sky value, systematic '
    'and physically interpretable differences were found between locations.', Body))

story.append(Paragraph(
    'The main findings are as follows. First, the temporal evolution of temperature and '
    'humidity followed a muted but recognisable diurnal cycle, with gradual warming '
    'from morning to midday and a corresponding decrease in relative humidity at all '
    'three sites. Wind speeds were consistently low, reflecting the synoptic '
    'calm associated with the frontal passage.', Body))

story.append(Paragraph(
    'Second, surface and environmental properties exerted a clear and persistent '
    'influence on near-surface conditions. The concrete surface, characterised by '
    'high thermal admittance and zero evapotranspiration capacity, recorded the '
    'highest temperatures (mean 33.2 degrees C, max 38.7 degrees C) and the lowest '
    'humidity (mean RH 32.9%). Vegetated surfaces buffered temperature extremes '
    'through evapotranspiration and shading, with the Trees location showing the '
    'coolest sub-canopy microclimate.', Body))

story.append(Paragraph(
    'Third, the vertical temperature gradient Delta-T confirms fundamentally different '
    'near-surface energy exchange regimes: Concrete drives upward sensible heat flux '
    '(mean Delta-T = +1.18 degrees C), while the Trees canopy creates a stable, '
    'cooled sub-canopy layer (mean Delta-T = -0.38 degrees C). These results '
    'demonstrate that even a modest fraction of vegetated cover can meaningfully '
    'reduce heat generation in urban environments, with important implications for '
    'urban planning and climate adaptation strategies.', Body))

# ═══════════════════════════════════════════════════════════════════════════════
# 6. REFERENCES
# ═══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('References', H1))

refs = [
    'Arnfield, A.J. (2003). Two decades of urban climate research: a review of turbulence, '
    'exchanges of energy and water, and the urban heat island. <i>International Journal of '
    'Climatology</i>, 23(1), 1-26. https://doi.org/10.1002/joc.859',

    'DWD (2026). Climate Data Center (CDC) - Open Data Portal. Deutscher Wetterdienst. '
    'Station Lindenberg (ID 03015). Retrieved October 2026 from '
    'https://opendata.dwd.de/climate_environment/CDC/',

    'Holmgren, W.F., Hansen, C.W., and Mikofski, M.A. (2018). pvlib python: a python '
    'package for modeling solar energy systems. <i>Journal of Open Source Software</i>, '
    '3(29), 884. https://doi.org/10.21105/joss.00884',

    'Oke, T.R. (1987). <i>Boundary Layer Climates</i> (2nd ed.). Methuen, London. '
    'ISBN 0-415-04319-0.',

    'Oke, T.R., Mills, G., Christen, A., and Voogt, J.A. (2017). <i>Urban Climates</i>. '
    'Cambridge University Press. https://doi.org/10.1017/9781139016476',

    'Stewart, I.D., and Oke, T.R. (2012). Local climate zones for urban ecosystem '
    'studies: new tool for urban scientists. <i>Bulletin of the American Meteorological '
    'Society</i>, 93(12), 1879-1900. https://doi.org/10.1175/BAMS-D-11-00019.1',

    'Trachte, K. (2026). Lecture notes: 13046 Microclimates. '
    'Brandenburg University of Technology Cottbus-Senftenberg, SoSe 2026.',
]

for r in refs:
    story.append(Paragraph(r, Ref))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f'Done: {OUT}')
