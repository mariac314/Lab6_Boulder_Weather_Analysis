
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Lab6_functions import sundowner_data_loader

url_base = "https://sundowner.colorado.edu/weather/atoc1/wxobs"

month_df = sundowner_data_loader(url_base)

#print(month_df.size)
#print(month_df.shape)
#print(month_df.head())

# For looking at time series data
month_df['Rolling_24hr_mean'] = month_df['Temp_Out'].rolling('24h').mean()
month_df['Daily_Mean_Temp'] = month_df.groupby(month_df.index.date)['Temp_Out'].transform('mean')
month_df['Anomaly'] = month_df.Temp_Out - month_df.Daily_Mean_Temp
yearly_groups = month_df.groupby(month_df.index.year) # Source: https://www.geeksforgeeks.org/python/apply-operations-to-groups-in-pandas/

# For bar graphs comparing yearly February trends
yearly_avg_temp = yearly_groups.Temp_Out.mean()
yearly_temp_std = yearly_groups.Temp_Out.std()
yearly_avg_humidity = yearly_groups.Out_Hum.mean()
yearly_humidity_std = yearly_groups.Out_Hum.std()

# For looking individually at February 2026
Feb_2026 = yearly_groups.get_group(2026)

# Plot figures
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(12,7))
ax1.bar(yearly_avg_temp.index, yearly_avg_temp.values, color='blue', alpha=0.6)
ax1.errorbar(yearly_avg_temp.index, yearly_avg_temp.values, yerr=yearly_temp_std, fmt='o',color='orange')
ax1.set_xlabel('Year')
ax1.set_ylabel('Temperature (°F)')
ax1.set_title('Average February Temperature in Boulder')

ax2.bar(yearly_avg_humidity.index, yearly_avg_humidity.values, color='blue', alpha=0.6)
ax2.errorbar(yearly_avg_humidity.index, yearly_avg_humidity.values, yerr=yearly_humidity_std, fmt='o',color='orange')
ax2.set_xlabel('Year')
ax2.set_ylabel('Relative Humidity (%)')
ax2.set_title('Average February Humidity in Boulder')

ax3.plot(Feb_2026.index, Feb_2026.Temp_Out, color='blue', alpha=0.6, label = '5-min Temp')
ax3.plot(Feb_2026.index, Feb_2026.Rolling_24hr_mean, color='orange', label = '24-hr Rolling Mean')
ax3.set_title('February 2026 in Boulder:  Temperature')
ax3.set_ylabel('Temperature (°F)')
ax3.set_xlabel('Date')
ax3.legend(loc='best')
ax3.tick_params(axis='x', labelrotation=45)

ax4.plot(Feb_2026.index, Feb_2026.Anomaly, color='blue', alpha=0.6)
ax4.axhline(y=0, color = 'orange', linestyle='--', linewidth=2)
ax4.set_title('February 2026 in Boulder:  Temperature Anomalies')
ax4.set_ylabel('Anomaly (°F)')
ax4.set_xlabel('Date')
ax4.tick_params(axis='x', labelrotation=45)

plt.tight_layout()
plt.savefig('February_Weather_Boulder.png', dpi = 300, bbox_inches='tight')
plt.show()