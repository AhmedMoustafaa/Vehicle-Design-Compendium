import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from scipy.interpolate import griddata
import matplotlib
import csv
import pandas as pd


matplotlib.use('TkAgg')

v_cruise_list = [20, 25, 30, 35]
AR_values = np.linspace(4, 25, 43)
MTOW = 9
S_ref = 0.6
rho_aluminum = 2700
rho_foam = 40
g = 9.81
t_c_ratio = 0.12
rho_air = 1.225

# Spar Geometry
main_spar_od = 0.015
main_spar_t = 0.002
rear_spar_od = 0.012
rear_spar_t = 0.001

def spar_area(od, t):
    ri = od / 2 - t
    ro = od / 2
    return np.pi * (ro ** 2 - ri ** 2)

main_spar_A = spar_area(main_spar_od, main_spar_t)
rear_spar_A = spar_area(rear_spar_od, rear_spar_t)
total_spar_A = main_spar_A + rear_spar_A
spar_mass_per_meter = total_spar_A * rho_aluminum

def calculate_wing_weight(AR, S_ref, spar_mass_per_meter, t_c_ratio, rho_foam, total_spar_A):
    span = (S_ref * AR) ** 0.5
    chord = (S_ref / AR) ** 0.5
    spar_weight = spar_mass_per_meter * span
    wing_volume_approx = S_ref * chord * t_c_ratio
    spar_volume = total_spar_A * span
    foam_volume = wing_volume_approx - spar_volume
    if foam_volume < 0:
        return np.nan, np.nan, np.nan
    foam_weight = foam_volume * rho_foam
    total_weight = spar_weight + foam_weight
    return total_weight, spar_weight, foam_weight

def find_min_drag(AR, S_ref, MTOW, v_cruise, rho_air, g):
    opti = asb.Opti()
    alpha = opti.variable(init_guess=5, lower_bound=-10, upper_bound=15)
    span = (S_ref * AR) ** 0.5
    chord = (S_ref / AR) ** 0.5

    wing = asb.Wing(
        name="Main Wing",
        symmetric=True,
        xsecs=[
            asb.WingXSec(xyz_le=[0, 0, 0], chord=chord, twist=0, airfoil=asb.Airfoil("naca2412")),   #TODO
            asb.WingXSec(xyz_le=[0, span / 2, 0], chord=chord, twist=0, airfoil=asb.Airfoil("naca2412"))
        ]
    )

    airplane = asb.Airplane(wings=[wing], s_ref=S_ref, c_ref=chord, b_ref=span)
    op_point = asb.OperatingPoint(velocity=v_cruise, alpha=alpha)
    aero = asb.AeroBuildup(airplane=airplane, op_point=op_point).run()

    opti.minimize(aero['D'])
    opti.subject_to(aero['L'] == MTOW * g)

    try:
        sol = opti.solve(verbose=False)
        return sol.value(aero['D']), sol.value(aero['L'] / aero['D']), sol.value(alpha)
    except Exception:
        return np.nan, np.nan, np.nan



results_dict = {}
wing_weight_cache = {}
surface_data = []

# Analysis Loop
for v_cruise in v_cruise_list:
    print(f"\n--- Running for v_cruise = {v_cruise} m/s ---")
    results = []

    for AR in AR_values:
        if AR not in wing_weight_cache:
            weight, spar_w, foam_w = calculate_wing_weight(
                AR, S_ref, spar_mass_per_meter, t_c_ratio, rho_foam, total_spar_A
            )
            wing_weight_cache[AR] = weight
        else:
            weight = wing_weight_cache[AR]

        if np.isnan(weight):
            continue

        drag, L_D, alpha = find_min_drag(
            AR, S_ref, MTOW, v_cruise, rho_air, g
        )
        if np.isnan(drag):
            continue

        objective = drag + weight * g

        results.append({
            'AR': AR,
            'Wing_Weight_kg': weight,
            'Drag_N': drag,
            'L_D': L_D,
            'Alpha_deg': alpha,
            'Objective_N': objective
        })

        surface_data.append([AR, v_cruise, drag, weight])

    df = pd.DataFrame(results)
    results_dict[v_cruise] = df

df_surface = pd.DataFrame(surface_data, columns=["AspectRatio", "CruiseVelocity", "Drag_N", "WingWeight_kg"])
df_surface.to_csv("drag_weight_surface_data.csv", index=False)

# Plotting (2D)
plt.style.use('seaborn-v0_8-whitegrid')
colors = plt.cm.viridis(np.linspace(0, 1, len(v_cruise_list)))

# Wing Weight vs AR (only once)
fig1, ax1 = plt.subplots(figsize=(10, 6))
AR_sorted = sorted(wing_weight_cache.keys())
weights_sorted = [wing_weight_cache[AR] for AR in AR_sorted]
ax1.plot(AR_sorted, weights_sorted, 'k-o', label='Wing Weight')
ax1.set_ylabel('Wing Weight (kg)')
ax1.set_xlabel('Aspect Ratio (AR)')
ax1.set_title('Wing Weight vs Aspect Ratio')
ax1.legend()
ax1.grid(True)

# Drag vs AR
fig2, ax2 = plt.subplots(figsize=(10, 6))
for v, color in zip(v_cruise_list, colors):
    df = results_dict[v]
    ax2.plot(df['AR'], df['Drag_N'], marker='o', label=f"v = {v} m/s", color=color)
ax2.set_ylabel('Drag (N)')
ax2.set_xlabel('Aspect Ratio (AR)')
ax2.set_title('Drag vs Aspect Ratio at Different Cruise Speeds')
ax2.legend()
ax2.grid(True)

# L/D vs AR
fig3, ax3 = plt.subplots(figsize=(10, 6))
for v, color in zip(v_cruise_list, colors):
    df = results_dict[v]
    ax3.plot(df['AR'], df['L_D'], marker='s', label=f"v = {v} m/s", color=color)
ax3.set_ylabel('Lift-to-Drag Ratio (L/D)')
ax3.set_xlabel('Aspect Ratio (AR)')
ax3.set_title('L/D Ratio vs Aspect Ratio at Different Cruise Speeds')
ax3.legend()
ax3.grid(True)

# # 3D Surface Plot: AR vs Velocity vs Drag
# fig4 = plt.figure(figsize=(10, 7))
# ax4 = fig4.add_subplot(111, projection='3d')
#
# # Convert to arrays
# surface_data = np.array(surface_data)
# ARs = surface_data[:, 0]
# Vs = surface_data[:, 1]
# Drags = surface_data[:, 2]
#
# # Grid for surface plot
# AR_grid = np.linspace(ARs.min(), ARs.max(), 100)
# V_grid = np.linspace(Vs.min(), Vs.max(), 100)
# AR_grid_mesh, V_grid_mesh = np.meshgrid(AR_grid, V_grid)
#
# # Interpolate drag data on grid
# Drag_grid = griddata((ARs, Vs), Drags, (AR_grid_mesh, V_grid_mesh), method='cubic')
#
# surf = ax4.plot_surface(
#     AR_grid_mesh,
#     V_grid_mesh,
#     Drag_grid,
#     cmap=cm.viridis,
#     edgecolor='none',
#     rstride=1,
#     cstride=1,
#     linewidth=0,
#     antialiased=True,
#     shade=True
# )
# ax4.contour(AR_grid_mesh, V_grid_mesh, Drag_grid, zdir='z', offset=Drag_grid.min(), cmap='viridis', linestyles='dotted')
# ax4.contour(AR_grid_mesh, V_grid_mesh, Drag_grid, zdir='x', offset=ARs.min(), cmap='viridis', linestyles='dotted')
# ax4.contour(AR_grid_mesh, V_grid_mesh, Drag_grid, zdir='y', offset=Vs.max(), cmap='viridis', linestyles='dotted')
# ax4.set_xlabel("Aspect Ratio (AR)")
# ax4.set_ylabel("Cruise Velocity (m/s)")
# ax4.set_zlabel("Drag (N)")
# ax4.set_title("3D Surface: Drag vs AR vs Cruise Velocity")
# fig4.colorbar(surf, shrink=0.5, aspect=10, label="Drag (N)")
#
# plt.tight_layout()
# plt.show()


