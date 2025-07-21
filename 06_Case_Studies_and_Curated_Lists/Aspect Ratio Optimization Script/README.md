# Aspect Ratio Optimization Script

This Python script is designed to **optimize an aircraft wing's aspect ratio (AR)** by considering both its **aerodynamic drag and structural weight**. It uses the powerful `aerosandbox` library for detailed aerodynamic calculations and `matplotlib` for clear data visualization.

The script first calculates the wing's weight based on parameters like AR, material densities (aluminum for spars, foam for infill), and assumed structural dimensions. Simultaneously, it leverages `aerosandbox` to determine the minimum drag and the corresponding angle of attack required to generate sufficient lift to support the aircraft's maximum takeoff weight (MTOW). To find the best balance, the script combines drag and the force equivalent of wing weight into a single objective function. It then systematically sweeps through a range of AR values, analyzing their impact on **wing weight, drag, the lift-to-drag (L/D) ratio**, and this combined objective.

---

### Visualization and Analysis

The analysis culminates in several insightful plots:

* **Wing Weight and Drag vs. Aspect Ratio:** Visualizes how these key metrics change with varying AR.
* **Pareto Front of Drag vs. Wing Weight:** Illustrates the trade-off between drag and wing weight, with points colored by their corresponding AR.
* **Lift-to-Drag Ratio vs. Aspect Ratio:** Shows the aerodynamic efficiency trends across different ARs.

---

### Interactive 3D Surface Plots

In addition to the 2D plots, this script also includes functionality to visualize the relationship between drag, wing weight, aspect ratio, and cruise velocity using **interactive 3D surface plots**. It reads pre-calculated data from a `drag_weight_surface_data.csv` file, interpolates this data to create smooth surfaces, and then uses `plotly` to generate dynamic visualizations. These plots allow for an interactive exploration of how drag and wing weight vary across different combinations of aspect ratio and cruise velocity, with a convenient toggle to switch between viewing the drag surface and the wing weight surface. This provides a comprehensive understanding of the design space.

---

### Customization

You can easily adjust key parameters such as `MTOW` (maximum takeoff weight), `S_ref` (reference area), `v_cruise` (cruise velocity), spar dimensions, and material densities directly within the script to adapt it to different design specifications.