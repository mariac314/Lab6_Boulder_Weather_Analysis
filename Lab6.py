
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Lab6_functions import sundowner_data_loader

url_base = "https://sundowner.colorado.edu/weather/atoc1/wxobs"

month_df = sundowner_data_loader(url_base)
month_df = month_df.rename(columns={'Unnamed:_17_level_0_Rain':'Rain'})
#print(month_df.size)
#print(month_df.shape)
#print(month_df.head())

# For comparing yearly February trends
yearly_groups = month_df.groupby(month_df.index.year) # Source: https://www.geeksforgeeks.org/python/apply-operations-to-groups-in-pandas/
yearly_cumulative_precip = yearly_groups.Rain.sum()
yearly_temp_data = []
yearly_humidity_data = []
yearly_wind_data = []
labels = []
# This loop generates lists for box plots
for year, group in yearly_groups:
    yearly_temp_data.append(yearly_groups.get_group(year).Temp_Out)
    yearly_humidity_data.append(yearly_groups.get_group(year).Out_Hum)
    yearly_wind_data.append(yearly_groups.get_group(year).Wind_Speed)
    labels.append(year)

# For looking at time series and February 2026 data
month_df['Rolling_24hr_mean'] = month_df['Temp_Out'].rolling('24h').mean()
month_df['Daily_Mean_Temp'] = month_df.groupby(month_df.index.date)['Temp_Out'].transform('mean')
month_df['Anomaly'] = month_df.Temp_Out - month_df.Daily_Mean_Temp
Feb_2026 = yearly_groups.get_group(2026)
Feb_2026_avg_wind = Feb_2026.Wind_Speed.resample('1D').mean()
Feb_2026_max_wind = Feb_2026.Hi_Speed.resample('1D').max()

# Plotting
# Figure 1: Box plot highlighting yearly February temperature trends in Boulder
plt.rcParams['axes.labelsize'] = 12
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2, figsize=(10,12))
ax1.boxplot(yearly_temp_data, showfliers=False)
ax1.set_xlabel('Year')
ax1.set_ylabel('Temperature (°F)')
ax1.set_title('February Temperature in Boulder')
ax1.set_xticklabels(labels)

# Figure 2: Box plot highlighting yearly February humidity trends in Boulder
ax2.boxplot(yearly_humidity_data, showfliers=False)
ax2.set_xlabel('Year')
ax2.set_ylabel('Relative Humidity (%)')
ax2.set_title('February Humidity in Boulder')
ax2.set_xticklabels(labels)

# Figure 3: Cumulative sum of February precipitation over the past 6 years in Boulder
ax3.bar(yearly_cumulative_precip.index, yearly_cumulative_precip.values, color='blue', alpha=0.6)
ax3.set_xlabel('Year')
ax3.set_ylabel('Precipitation (Inches)')
ax3.set_title('Cumulative February Precipitation in Boulder')

# Figure 4: Bar chart showing peak wind gusts and average wind speed for each day in February 2026
ax4.bar(Feb_2026_max_wind.index, Feb_2026_max_wind.values, color='blue', alpha=0.6, label = 'Peak Gust')
ax4.bar(Feb_2026_avg_wind.index, Feb_2026_avg_wind.values, color='orange', label = 'Average Wind Speed')
ax4.set_xlabel('Date')
ax4.set_ylabel('Wind Speed (mph)')
ax4.set_title('February 2026 in Boulder: Wind Speed')
ax4.legend(loc='best')
ax4.tick_params(axis='x', labelrotation=25)

# Figure 5: Time series showing temperature trends during February 2026
ax5.plot(Feb_2026.index, Feb_2026.Temp_Out, color='blue', alpha=0.6, label = '5-min Temp')
ax5.plot(Feb_2026.index, Feb_2026.Rolling_24hr_mean, color='orange', label = '24-hr Rolling Mean')
ax5.set_title('February 2026 in Boulder:  Temperature')
ax5.set_ylabel('Temperature (°F)')
ax5.set_xlabel('Date')
ax5.legend(loc='best')
ax5.tick_params(axis='x', labelrotation=25)

# Figure 6: Time series showing temperature anomalies during February 2026
ax6.plot(Feb_2026.index, Feb_2026.Anomaly, color='blue', alpha=0.6)
ax6.axhline(y=0, color = 'orange', linestyle='--', linewidth=2)
ax6.set_title('February 2026 in Boulder:  Temperature Anomalies')
ax6.set_ylabel('Anomaly (°F)')
ax6.set_xlabel('Date')
ax6.tick_params(axis='x', labelrotation=25)

plt.tight_layout()
plt.savefig('February_Weather_Boulder.png', dpi = 300, bbox_inches='tight')
plt.show()