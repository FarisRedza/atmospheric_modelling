import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('GTK4Agg')

df = pd.read_csv('/workspaces/atmospheric_loss_modelling/SatQuMA/channel/atmosphere/MODTRAN_wl_785.0-850.0-5.0nm_h1_500.0km_h0_0.0km_elevation_data.csv')
plt.plot(df['# theta (deg)'], df['785 nm'])
plt.xlabel('Elevation Angle (°)')
plt.ylabel('Transmittance')
plt.title('MODTRAN Downlink')
plt.grid(True)
plt.ylim([0, 1])
plt.xlim([0, 90])
plt.show()