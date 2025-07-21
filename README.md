# A. Learning Path and Recommended Reading for Fixed-Wing UAV Design

This guide outlines a suggested learning path for fixed-wing UAV design, from fundamental concepts to more advanced topics. It also provides a curated list of recommended readings from the textbooks within this compendium, highlighting key chapters and sections relevant to each topic.

## I. Foundational Building Blocks

Understanding the basic terminology and core components is crucial.

### 1. Geometry and Coordinate Systems

* **Concepts to Know:**
    * Angles, Axes, and Different coordinate systems (Body, Wind, Stability Axis).
* **Recommended Reading:**
    * [Etkins - Dynamics Of Flights](../02_Fundamental_Textbooks/Theoreticals/Dynamics%20Of%20Flights%20by%20Etkins.pdf): Introductory chapters on coordinate systems for flight mechanics.

### 2. Anatomy of Aircraft Components

A deep dive into how each part of the aircraft is designed and its impact on performance.

* **Concepts to Know:**
    * **The Anatomy of the Airfoil:**
        * How each geometric parameter affects performance (Maximum Camber & position, Maximum Thickness & position, LE Radius, TE sharpness).
        * Airfoil Families (NACA, Wortmann, Eppler, etc.).
    * **The Anatomy of the Wing:**
        * Planform Parameters and their effects (Aspect Ratio (AR), Taper Ratio (TR), Sweep Angle ($\Lambda$), Wing Area (S)).
        * Three-Dimensional Wing Parameters (Twist, Dihedral).
    * **The Anatomy of the Tail:** Understanding different tail configurations and their purpose.
    * **Lift Enhancement Devices:** Flaps, slats, etc., and their principles.
* **Recommended Reading:**
    * [Gudmundsson - General Aviation Aircraft Design Applied Methods and Procedures](../02_Fundamental_Textbooks/Classic%20Essentials/General%20Aviation%20Aircraft%20Design%20Applied%20Methods%20and%20Procedures%20(Snorri%20Gudmundsson).pdf): Chapters 8-13 (the `anatomy of` series are highly recommended for detailed component understanding).

## II. Core Aerodynamic Concepts

How air interacts with the aircraft, generating forces.

* **Concepts to Know:**
    * How Lift is Created: Effect of Angle of Attack (AoA), Geometry (Camber) on Lift.
    * Drag Types: Parasite, Induced, Wave, Interference, Form, Skin Friction.
    * Drag Modeling: Different methods to model the drag polar ($C_D$ as a function of $C_L$).
    * Flow Types: Laminar & Turbulence Characteristics.
    * Aerodynamic Center & Center of Pressure.
    * Boundary Layer: Causes, Types, Effects.
    * Transition Point: Ways to predict it and how it's modeled in Xfoil.
    * Separation: Causes, Types, Effects.
* **Recommended Reading:**
    * [Drela - Flight Vehicle Aerodynamics](../02_Fundamental_Textbooks/Theoreticals/Flight%20Vehicle%20Aerodynamics%20(Mark%20Drela)%20(Z-Library).pdf): For advanced mathematical and implementation details of aerodynamic analysis.
    * [Sóbester & Forrester - Aircraft Aerodynamic Design Geometry and Optimization](../02_Fundamental_Textbooks/Modern%20Advanced/Aircraft%20Aerodynamic%20Design%20Geometry%20and%20Optimization%20(Andr%C3%A1s%20S%C3%B3bester,%20Alexander%20I%20J%20Forrester).pdf): Provides insights into aerodynamic design principles.
    * [Rizzi A. - Aircraft Aerodynamic Design with Computational Software](../02_Fundamental_Textbooks/Modern%20Advanced/Aircraft%20Aerodynamic%20Design%20with%20Computational%20Software%20(Rizzi%20A.).pdf): Focuses on computational aspects of aerodynamic design.

## III. Performance Fundamentals

Quantifying how an aircraft performs its mission.

* **Concepts to Know:**
    * **Fundamental Design and Performance Parameters:**
        * Wing Loading ($W/S$), Thrust-to-Weight Ratio ($T/W$), Drag Polar, Lift-to-Drag Ratio ($L/D$).
        * Load Factor ($n$).
        * Rate of Climb, Range, Endurance.
        * Optimum Flight Conditions: Maximum $(\frac{C_L}{C_D})_{max}$, $(\frac{C_L^{3/2}}{C_D})_{max}$, $(\frac{C_L^{1/2}}{C_D})_{max}$.
    * **Propulsion System Modeling:**
        * Effect of Battery Voltage and Capacity.
        * Effect of Motor Kv and Kt.
        * Effect of Propeller Diameter, Pitch, and Number of Blades.
    * Thrust Available vs. Thrust Required.
    * Maximum Velocity & Minimum Velocity.
    * $C_L$ and Velocity Corresponding to Maximum Range and Maximum Endurance.
* **Recommended Reading:**
    * [Anderson - Aircraft Performance & Design](../02_Fundamental_Textbooks/Classic%20Essentials/Aircraft%20Performance%20&%20Design.pdf): Chapters 5 (Steady Flight Performance) and 6 (Accelerated Flight Performance) are essential.
    * [Keane & Sobester - Small Unmanned Fixed-Wing Aircraft Design](../02_Fundamental_Textbooks/Modern%20Advanced/Small%20Unmanned%20Fixed-Wing%20Aircraft%20Design.%C2%A0%20A%20Practical%20Approach%20(Andrew%20J.%20Keane,%20Andras%20Sobester%20etc.).pdf): Relevant sections on propulsion system modeling and performance for UAVs.

## IV. Aerodynamic & Performance Analysis Methods

Tools and theories used to predict aircraft behavior.

### 1. Aerodynamic Analysis Theories

* **Concepts to Know:** At least know how each one models the airfoil, their accuracy compared to experimental data, and their limitations.
    * **Airfoil Analysis Theories:** Thin Airfoil Theory, 2D Panel Theory, Integrated Boundary Layer.
    * **Wing/Airplane Analysis Theories:** Lifting Line Theory, Vortex Lattice Methods, 3D Panel Theory.
* **Recommended Reading:**
    * [Drela - Flight Vehicle Aerodynamics](../02_Fundamental_Textbooks/Theoreticals/Flight%20Vehicle%20Aerodynamics%20(Mark%20Drela)%20(Z-Library).pdf): In-depth coverage of these theories.
    * [Rizzi A. - Aircraft Aerodynamic Design with Computational Software](../02_Fundamental_Textbooks/Modern%20Advanced/Aircraft%20Aerodynamic%20Design%20with%20Computational%20Software%20(Rizzi%20A.).pdf): Discusses implementation of these methods in software.
    * Refer to the **[`05_Tools_and_Software_Guides/XFLR5`](../05_Tools_and_Software_Guides/XFLR5)** section for practical application of some of these theories.

### 2. Performance Analysis Methods

* **Concepts to Know:** Have an idea about which parameters are present in each equation.
    * **Steady Flight Performance:**
        * Cruise Performance (Range Analysis, Endurance Analysis).
        * Climb Performance (Rate of Climb, Time to Climb, Service Ceiling and Absolute Ceiling).
    * **Accelerated Flight Performance:**
        * Take-off Analysis (Ground Run).
        * Level Turn Analysis (Minimum Turn Radius, Maximum Turn Rate).
        * Landing Analysis (Ground Run).
    * **Numerical Simulation:** How to use these to simulate airplane performance numerically (Approximated solutions to IVPs differential equations) using methods like Runge-Kutta (4th order version implemented in some sizing tools) and Euler Methods.
* **Recommended Reading:**
    * [Anderson - Aircraft Performance & Design](../02_Fundamental_Textbooks/Classic%20Essentials/Aircraft%20Performance%20&%20Design.pdf): Chapters 5 and 6 are key.
    * [Gudmundsson - General Aviation Aircraft Design Applied Methods and Procedures](../02_Fundamental_Textbooks/Classic%20Essentials/General%20Aviation%20Aircraft%20Design%20Applied%20Methods%20and%20Procedures%20(Snorri%20Gudmundsson).pdf): Provides practical methods and procedures for performance analysis.

## V. Flight Mechanics, Stability, & Control

Ensuring the aircraft is controllable and stable in flight.

* **Concepts to Know:**
    * Balance & Stability (Static and Dynamic).
    * Control surface effects on trim.
    * Airplane components' contribution to stability.
    * Dynamic stability modes (Phugoid, Short Period, Roll, Spiral, Dutch Roll).
    * Which dynamic modes are vital to our scale (UAVs often emphasize different modes than large aircraft).
    * Handling Quality Levels (e.g., Cooper-Harper ratings, though more applicable to manned flight, concepts can apply).
* **Recommended Reading:**
    * [Etkins - Dynamics Of Flights](../02_Fundamental_Textbooks/Theoreticals/Dynamics%20Of%20Flights%20by%20Etkins.pdf): A very good and detailed book covering theoretical and practical aspects of stability and control basics.
    * [Gudmundsson - General Aviation Aircraft Design Applied Methods and Procedures](../02_Fundamental_Textbooks/Classic%20Essentials/General%20Aviation%20Aircraft%20Design%20Applied%20Methods%20and%20Procedures%20(Snorri%20Gudmundsson).pdf): Chapter 24 (Longitudinal Stability and Control) and Chapter 25 (LAT-DIR Stability and Control).

## VI. Big Picture Design Process

From mission definition to detailed design.

* **Concepts to Know:**
    * **Pre-conceptual Phase:** Mission Analysis, Specifying Constraints, Similar UAVs surveying (market, historical, etc.).
    * **Conceptual Design Phase:**
        * Qualitative & Quantitative Design Path Definition: Identify key high-level (e.g., $W/S$ or $T/W$) design parameters that represent differences across these paths.
        * Design Space Exploration: Modeling the design space in a multi-disciplinary fashion by connecting the design parameters to form meaningful carpet plots, applying constraints, and scoring each design point.
        * Applying Sensitivity Analyses: Not only applied to the mission score, but can be used whenever uncertainties are present (e.g., for a matching plot problem).
        * Informed Configuration Selection: Based on previous analysis with manufacturing, time, and economical costs in mind.
    * **Preliminary Design Phase:**
        * Wing Design: How to select reasonable-envisioned values for planform parameters like AR, TR.
        * Airfoil Selection: Selecting an airfoil in a systematic manner reflecting your design philosophy.
        * Stability Surfaces Sizing & Control Surfaces Sizing.
        * Flight Envelope Analyses.
        * Performance under wind conditions.
    * **Detailed Design:** Finalizing design specifications for manufacturing.
* **Recommended Reading:**
    * [Gudmundsson - General Aviation Aircraft Design Applied Methods and Procedures](../02_Fundamental_Textbooks/Classic%20Essentials/General%20Aviation%20Aircraft%20Design%20Applied%20Methods%20and%20Procedures%20(Snorri%20Gudmundsson).pdf): Chapter 1 (The Aircraft Design Process) and Chapter 3 (Initial Sizing), Chapter 6 (Aircraft Weight Analysis).
    * [Keane & Sobester - Small Unmanned Fixed-Wing Aircraft Design](../02_Fundamental_Textbooks/Modern%20Advanced/Small%20Unmanned%20Fixed-Wing%20Aircraft%20Design.%C2%A0%20A%20Practical%20Approach%20(Andrew%20J.%20Keane,%20Andras%20Sobester%20etc.).pdf): Chapters 8-15 provide a practical approach to the design process specifically for UAVs, including Design of Experiments (DOE), Design Space Exploration (DSE), and optimization.
    * [Torenbeek - Advanced Aircraft Design Conceptual Design, Analysis and Optimization of Subsonic Civil Airplanes](../02_Fundamental_Textbooks/Modern%20Advanced/Advanced%20Aircraft%20Design%20Conceptual%20Design,%20Analysis%20and%20Optimization%20of%20Subsonic%20Civil%20Airplanes%20(Egbert%20Torenbeek).pdf): Chapter 1 (Design of the Well-Tempered Aircraft, especially Sections 1.4, 1.5, 1.7 on automated design synthesis and optimization), Chapter 2 (Early Conceptual Design), Chapter 7 (Aircraft Design Optimization), Chapter 8 (Theory of Optimum Weight), Chapters 10 & 11 (Wing Design), Chapter 12 (Unified Cruise Performance).
    * Refer to the **[`04_Research_Deep_Dives/Aero-struct`](../04_Research_Deep_Dives/Aero-struct)** (which contains specific papers on optimization, e.g., in `Design Methodology`) for more academic perspectives on design methodologies.