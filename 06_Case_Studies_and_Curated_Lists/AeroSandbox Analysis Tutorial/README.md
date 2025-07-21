# AeroSandbox Aircraft Analysis Tutorial
---
This Jupyter Notebook serves as a comprehensive tutorial for performing aircraft aerodynamic analysis and optimization using the `aerosandbox` library. It guides users through the process of defining aircraft geometry, setting atmospheric conditions, and conducting aerodynamic analyses using various methods, including the Vortex Lattice Method (VLM), AeroBuildup, and both Linear and Nonlinear Lifting Line Theory. The tutorial emphasizes finding aircraft trim conditions by optimizing for scenarios where lift equals weight and the pitching moment is zero. Furthermore, it demonstrates how to compare the results obtained from different aerodynamic analysis techniques and includes a section on integrating with external tools like AVL for more advanced analysis, with a note on its prerequisite installation.

### Key Sections:

* **Aircraft Geometry Definition:** Learn to construct detailed `Wing` and `Fuselage` objects within `aerosandbox`, including defining wing sections with custom airfoils, leading edge coordinates, chord, and twist, as well as fuselage cross-sections using superellipse parameters.
* **Atmospheric Conditions Setup:** Understand how to define the flight environment by setting atmospheric properties such as altitude.
* **Optimization Framework (`Opti`):** Explore the `Opti` class, which is central to setting up and solving nonlinear programs (NLPs) for aerospace design problems. It allows for the definition of decision variables (like velocity and angle of attack), constraints (e.g., lift equals weight, zero moment), and objective functions.
* **Aerodynamic Analysis Methods:** Dive into practical applications of different aerodynamic models available in `aerosandbox`:
    * **Vortex Lattice Method (VLM):** Used for calculating lift, drag, and moment coefficients by discretizing lifting surfaces into horseshoe vortices.
    * **AeroBuildup:** A component-buildup method for aerodynamic analysis, primarily based on principles from DATCOM Digital.
    * **Lifting Line Theory (Linear and Nonlinear):** Explore both linear and nonlinear approaches to lifting line theory for analyzing wing aerodynamics.
* **Trim Condition Optimization:** The notebook illustrates how to set up and solve optimization problems to find the aircraft's trim conditions, ensuring stable flight by balancing lift and weight and achieving zero pitching moment.
* **External Tool Integration (AVL):** A section dedicated to performing analyses using AVL, an external aerodynamic analysis tool, highlighting the process and necessary setup (e.g., adding AVL to system PATH).

## Usage

To run this tutorial, execute the cells sequentially within a Jupyter environment. Ensure all dependencies are installed. The script will define an example "trainer" aircraft, perform aerodynamic analyses using multiple methods, solve for trim conditions, and print the results to the console.

## Dependencies

* `aerosandbox`
* `aerosandbox.numpy` (aliased as `np`)
* `matplotlib`
* `scipy`
* `tqdm` (for progress bars in some sections)

## Important Notes

* For AVL analysis, ensure that AVL is correctly installed and its executable is accessible via your system's PATH, or specify its direct path in the script.
* Pay attention to the comparisons between different aerodynamic methods, as highlighted in the notebook, to understand their strengths and limitations.