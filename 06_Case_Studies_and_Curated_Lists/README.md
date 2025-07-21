# 6. Case Studies and Curated Lists

This folder contains a collection of Python scripts and Jupyter notebooks designed to assist in various stages of aircraft design and analysis. From optimizing wing geometry and performing detailed aerodynamic simulations to automating propulsion system calculations and integrating data from external tools, this project aims to streamline the aircraft design workflow.

## Project Structure

* **[Aspect Ratio Optimization Script](./Aspect%20Ratio%20Optimization%20Script/)**: This script study an optimization problem to the wing aspect ratio by analyzing the trade-offs between aerodynamic drag and structural weight. It includes 2D and interactive 3D visualizations to explore the design space.

* **[AeroSandbox Aircraft Analysis Tutorial](./AeroSandbox%20Analysis%20Tutorial/)**: A Jupyter Notebook providing a hands-on tutorial for using the `aerosandbox` library. It covers defining aircraft geometry, setting up atmospheric conditions, performing various aerodynamic analyses (VLM, AeroBuildup, Lifting Line Theory), finding trim conditions, and integrating with external tools like AVL.

* **[ECalc Automation and Component Matching](./ECalc%20Automation%20and%20Component%20Matching/)**: This folder houses scripts for automating interactions with the eCalc online propeller calculator. It also includes modules for intelligently matching and selecting propulsion system components (batteries, motors, ESCs, and propellers) from an inventory against a comprehensive database, and then using eCalc to calculate their performance.

* **[XFLR5 to AeroSandbox Converter and Aerodynamic Analyzer](./XFLR5%20to%20AeroSandbox%20Converter/)**: This set of scripts provides a pipeline for converting aircraft geometry defined in XFLR5 XML files into `aerosandbox` objects. It then performs detailed aerodynamic and stability analyses, including the calculation of trim conditions, stability derivatives, stall speed, and pitching moment characteristics.