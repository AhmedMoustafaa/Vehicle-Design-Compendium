import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from scipy.interpolate import griddata

MTOW = 9  # [kg]
S_ref = 0.6  # [m^2]
rho_aluminum = 2700  # [kg/m^3]
rho_foam = 40
g = 9.81
v_cruise = 30  # Assumed cruise speed [m/s] TODO: TO be modified to allow for arrays of velocity (Done in AR_sweep_vecotrized.py file)
t_c_ratio = 0.12  # Assumed wing thickness-to-chord ratio
rho_air = 1.225

main_spar_od = 0.015  # Main spar Outer Diameter [m]
main_spar_t = 0.002  # Main spar thickness [m]
rear_spar_od = 0.012  # Rear spar Outer Diameter [m]
rear_spar_t = 0.001  # Rear spar thickness [m]


def spar_area(od, t):
    """Calculates the cross-sectional area of a hollow circular spar."""
    ri = od / 2 - t
    ro = od / 2
    return np.pi * (ro ** 2 - ri ** 2)


main_spar_A = spar_area(main_spar_od, main_spar_t)
rear_spar_A = spar_area(rear_spar_od, rear_spar_t)
total_spar_A = main_spar_A + rear_spar_A
spar_mass_per_meter = total_spar_A * rho_aluminum


def calculate_wing_weight(AR, S_ref, spar_mass_per_meter, t_c_ratio, rho_foam, total_spar_A):
    """Calculates wing weight based on AR and structural parameters."""
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


def find_min_drag(AR, S_ref, MTOW, v_cruise, g):
    """Finds the minimum drag and corresponding alpha for a given AR."""
    opti = asb.Opti()
    alpha = opti.variable(init_guess=5, lower_bound=-10, upper_bound=15)
    span = (S_ref * AR) ** 0.5
    chord = (S_ref / AR) ** 0.5
    wing = asb.Wing(
        name="Main Wing",
        symmetric=True,
        xsecs=[
            asb.WingXSec(xyz_le=[0, 0, 0], chord=chord, twist=0, airfoil=asb.Airfoil("naca2412")),
            asb.WingXSec(xyz_le=[0, span / 2, 0], chord=chord, twist=0, airfoil=asb.Airfoil("naca2412"))
        ]
    )

    airplane = asb.Airplane(wings=[wing], s_ref=S_ref, c_ref=chord, b_ref=span)
    op_point = asb.OperatingPoint(
        velocity=v_cruise,
        alpha=alpha
    )
    op_point = asb.OperatingPoint(
        velocity=v_cruise,
        alpha=alpha
    )
    aero = asb.AeroBuildup(airplane=airplane, op_point=op_point).run()

    opti.minimize(aero['D'])
    opti.subject_to(aero['L'] == MTOW * g)

    try:
        sol = opti.solve(verbose=False)
        return sol.value(aero['D']), sol.value(aero['L'] / aero['D']), sol.value(alpha)
    except Exception:
        return np.nan, np.nan, np.nan


# Sensitivity Analysis: Sweep AR
print("--- Starting Sensitivity Analysis (Sweeping AR) ---")
AR_values = np.linspace(4, 25, 43)  # Define the range of AR to study
results = []

for AR_val in AR_values:
    weight, spar_w, foam_w = calculate_wing_weight(
        AR_val, S_ref, spar_mass_per_meter, t_c_ratio, rho_foam, total_spar_A
    )
    if np.isnan(weight):
        print(f"Skipping AR = {AR_val:.2f} (Invalid Weight)")
        continue

    drag, L_D, alpha_req = find_min_drag(
        AR_val, S_ref, MTOW, v_cruise, g
    )
    if np.isnan(drag):
        print(f"Skipping AR = {AR_val:.2f} (Aero Optimization Failed)")
        continue

    # Calculate combined objective (Drag + Weight Force)
    objective = drag + weight * g #(This Objective function formulation can be revisited and changed to see how it affects the optimum AR)

    results.append({
        'AR': AR_val,
        'Wing_Weight_kg': weight,
        'Drag_N': drag,
        'L_D': L_D,
        'Alpha_deg': alpha_req,
        'Objective_N': objective
    })
    print(
        f"AR = {AR_val:.2f} -> Weight = {weight:.3f} kg, Drag = {drag:.3f} N, L/D = {L_D:.2f}, Obj = {objective:.3f} N")

print("--- Analysis Complete ---")
df = pd.DataFrame(results)
min_obj_point = df.loc[df['Objective_N'].idxmin()]

# Visualization
plt.style.use('seaborn-v0_8-whitegrid')
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot 1: Weight vs. AR
ax1.plot(df['AR'], df['Wing_Weight_kg'], 'bo-', label='Total Wing Weight')
ax1.set_ylabel('Wing Weight (kg)')
ax1.set_title('Wing Weight and Drag vs. Aspect Ratio')
ax1.legend()
ax1.grid(True)

# Plot 2: Drag vs. AR
ax2.plot(df['AR'], df['Drag_N'], 'ro-', label='Total Drag')
ax2.set_xlabel('Aspect Ratio (AR)')
ax2.set_ylabel('Drag (N)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

# Plot 3: Pareto Front (Drag vs. Weight)
fig2, ax3 = plt.subplots(figsize=(8, 6))
scatter = ax3.scatter(df['Wing_Weight_kg'], df['Drag_N'], c=df['AR'], cmap='viridis', s=50, zorder=10)
ax3.plot(df['Wing_Weight_kg'], df['Drag_N'], 'k--', alpha=0.5, zorder=5)

# Highlight the minimum objective point
ax3.scatter(min_obj_point['Wing_Weight_kg'], min_obj_point['Drag_N'],
            c='red', s=150, marker='*', edgecolors='black',
            label=f"Min (D + W*g) @ AR={min_obj_point['AR']:.2f}", zorder=15)

ax3.set_xlabel('Wing Weight (kg)')
ax3.set_ylabel('Drag (N)')
ax3.set_title('Pareto Front: Drag vs. Wing Weight (Color = AR)')
ax3.legend()
cbar = plt.colorbar(scatter)
cbar.set_label('Aspect Ratio (AR)')
ax3.annotate(f"AR = {min_obj_point['AR']:.2f}",
             (min_obj_point['Wing_Weight_kg'], min_obj_point['Drag_N']),
             textcoords="offset points", xytext=(10,10), ha='center')

ax3.grid(True)
plt.tight_layout()
plt.show()

# Plot 4: L/D vs AR
fig3, ax4 = plt.subplots(figsize=(8, 6))
ax4.plot(df['AR'], df['L_D'], 'go-', label='L/D Ratio')
ax4.set_xlabel('Aspect Ratio (AR)')
ax4.set_ylabel('Lift-to-Drag Ratio (L/D)')
ax4.set_title('Lift-to-Drag Ratio vs. Aspect Ratio')
ax4.legend()
ax4.grid(True)
plt.tight_layout()
plt.show()

print(f"Point with Minimum (Drag + Weight Force): {min_obj_point}")

### Carpet Plot
df2 = pd.read_csv("drag_weight_surface_data.csv")
ARs = df2["AspectRatio"].values
Vs = df2["CruiseVelocity"].values
Drags = df2["Drag_N"].values
Weights = df2["WingWeight_kg"].values

AR_grid = np.linspace(min(ARs), max(ARs), 100)
V_grid = np.linspace(min(Vs), max(Vs), 100)
AR_mesh, V_mesh = np.meshgrid(AR_grid, V_grid)

Drag_mesh = griddata((ARs, Vs), Drags, (AR_mesh, V_mesh), method='cubic')
Weight_mesh = griddata((ARs, Vs), Weights, (AR_mesh, V_mesh), method='cubic')

fig = go.Figure()

# Surface for Drag
fig.add_trace(go.Surface(
    z=Drag_mesh, x=AR_mesh, y=V_mesh,
    colorscale='Viridis',
    name='Drag',
    showscale=True,
    colorbar=dict(title='Drag (N)')
))

# Surface for Weight
fig.add_trace(go.Surface(
    z=Weight_mesh, x=AR_mesh, y=V_mesh,
    colorscale='Cividis',
    visible=False,
    name='Wing Weight',
    showscale=True,
    colorbar=dict(title='Weight (kg)')
))

fig.update_layout(
    title="3D Surface: Drag and Wing Weight vs AR and Velocity",
    scene=dict(
        xaxis_title='Aspect Ratio (AR)',
        yaxis_title='Cruise Velocity (m/s)',
        zaxis_title='Z Axis'
    ),
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.57, y=1.15,
            buttons=list([
                dict(label="Drag",
                     method="update",
                     args=[{"visible": [True, False]},
                           {"scene": dict(zaxis_title="Drag (N)")}]),
                dict(label="Wing Weight",
                     method="update",
                     args=[{"visible": [False, True]},
                           {"scene": dict(zaxis_title="Weight (kg)")}]),
            ]),
            showactive=True
        )
    ],
    margin=dict(l=0, r=0, b=0, t=50)
)

fig.show()
