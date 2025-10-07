from Lim_solver import smart_optimise
from neumann_rates import raw_overpass, raw_overpass_instant
import numpy as np
import matplotlib.pyplot as plt

angle_range=np.arange(30, 155,5)
loss_profiles = [
    np.loadtxt(
        f"qkd/up_link_passes/Total_Uplink_Loss_maxelev_{angle}degrees.csv",
        skiprows=1,
        delimiter=","
    )  if angle<=90 else np.loadtxt(f"qkd/up_link_passes/Total_Uplink_Loss_maxelev_{180-angle}degrees.csv",skiprows=1,delimiter=",") for angle in angle_range]

# with 10km fibre
skl = []
for i,prof in enumerate(loss_profiles):
    params = [9.47893858965945, 9.89101987420694, 0.037228590019520497, 0.03834132110856429, 6135831.8248959305, 1e-09]
    qber, qx, m = raw_overpass(params, prof[:,1]+prof[:,2])
    delta = (qber+qx)/2
    skl+=[smart_optimise(m, delta, eps_qkd=1e-6, t=np.log2(10**8), f=1.19) * m]
plt.plot(angle_range, skl, label="10km fibre")

# without fibre
skl = []
for i,prof in enumerate(loss_profiles):
    params = [7.761328918344407, 7.542259886343475, 0.0335677812551474, 0.02531375770896907, 10826895.017621633, 4e-10]
    qber, qx, m = raw_overpass(params, prof[:,1]+prof[:,2])
    delta = (qber+qx)/2
    skl+=[smart_optimise(m, delta, eps_qkd=1e-6, t=np.log2(10**8), f=1.19) * m]
plt.plot(angle_range, skl, label="0km fibre")
plt.xlabel("Max Elevation Angle (Degrees)")
plt.ylabel("Secret finite key length (bits)")
plt.yscale("log")
plt.legend()
plt.show()