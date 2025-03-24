import os

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('GTK4Agg')

uplink = pd.read_csv(f'{os.getcwd()}/qrackling/qrackling_uplink.csv')
downlink = pd.read_csv(f'{os.getcwd()}/qrackling/qrackling_downlink.csv')

merged = pd.merge(uplink, downlink, on='Elevation', suffixes=('_uplink', '_downlink'))

# Compute difference
merged['Difference'] = merged['Atmospheric_uplink'] - merged['Atmospheric_downlink']
print(merged['Difference'])

ax = uplink.plot(
    x='Elevation',
    y='Atmospheric'
)
downlink.plot(
    x='Elevation',
    y='Atmospheric',
    ax=ax
)
plt.legend(['uplink', 'downlink'])
plt.xlabel('Elevation Angle (°)')
plt.ylabel('Transmittance')
plt.title('Qrackling')
plt.grid(True)
plt.show()

plt.plot(
    merged['Elevation'],
    merged['Difference']
)
plt.xlabel('Elevation Angle (°)')
plt.ylabel('Transmittance')
plt.title('Qrackling')
plt.grid(True)
plt.show()