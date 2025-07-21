# ECalc Automation and Component Matching
---
This folder contains a suite of Python scripts designed to automate interactions with the eCalc online propeller calculator and facilitate the matching of aircraft components (Batteries, Motors, ESCs, Propellers) from an inventory to a comprehensive database. The core functionality revolves around programmatically inputting data into eCalc, retrieving results, and intelligently matching components based on specified criteria.

### Key Features:

* **`calc.py` (ECalc Automation):** This script handles the direct automation of the eCalc website. It uses `selenium` to navigate the site, input aircraft and propulsion system parameters, trigger calculations, and download the resulting performance data. It is designed to streamline the process of obtaining detailed propulsion system performance characteristics from eCalc without manual intervention.
* **Component Matching (`Battery.py`, `Motor.py`, `Propeller.py`, `ESC.py`):** These modules define classes for different aircraft components and include logic to find the "best match" for an inventory item within a larger database (likely stored as a `.pkl` file).
    * **`Battery.py`:** Matches inventory batteries based on C-rating and capacity.
    * **`Motor.py`:** Matches inventory motors, likely using Kv, resistance, and potentially fuzzy matching for names/types.
    * **`Propeller.py`:** Matches inventory propellers based on parameters like number of blades, pitch, and diameter.
    * **`ESC.py`:** Defines a simple class for Electronic Speed Controllers (ESCs).
* **`match_data.py`:** This script likely contains the general logic or helper functions used by `Battery.py`, `Motor.py`, and `Propeller.py` for finding the best match within a database. It centralizes the comparison logic for various component types.
* **`Propulsion.py`:** This module integrates the individual component classes (`Battery`, `Motor`, `ESC`, `Propeller`) and the `calc.py` automation. It defines a `Propulsion` class that can assemble a full propulsion system, use the matched components, and then interface with `calc.py` to get comprehensive propulsion performance data from eCalc. It can calculate metrics such as static thrust, thrust-to-weight ratio, and endurance.

### Workflow:

1.  **Component Matching:** The individual component scripts (`Battery.py`, `Motor.py`, `Propeller.py`) are used to match available inventory items (read from an Excel file, e.g., `udcData.xlsx`) with more detailed specifications from pre-parsed `.pkl` databases (e.g., `batteries.pkl`, `motors.pkl`).
2.  **Propulsion System Assembly:** The `Propulsion.py` script takes these matched components and assembles a complete propulsion system object.
3.  **ECalc Automation:** The `Propulsion` object then leverages `calc.py` to automatically input the relevant parameters into the eCalc website, run simulations, and retrieve performance data, such as static thrust, thrust-to-weight ratios, endurance, and dynamic thrust.

### Usage:

To use these scripts, ensure you have the required Python packages installed (e.g., `selenium`, `pandas`, `fuzzywuzzy`). You will also need to:

* **Configure WebDriver:** Set up `selenium` to correctly interact with your browser (e.g., ChromeDriver for Chrome).
* **Provide Data Files:** Ensure the `resources/udcData/udcData.xlsx` (inventory) and `resources/ecalcData/pkl_data/` (component databases) paths are correct and the files exist.
* **Run Main Scripts:** Execute the individual component matching scripts or `Propulsion.py` directly to see the automation and matching in action.

### Dependencies:

* `pandas`
* `selenium`
* `fuzzywuzzy`
* `scipy`
* `math`
* `sympy`
* `aerosandbox` (specifically `Airplane` and `OperatingPoint` for `Propulsion.py`)
* `re`
* `glob`
* `shutil`
* (Potentially `openpyxl` for reading `.xlsx` files if not already handled by pandas)

**Note:** The `calc.py` script requires a configured Selenium WebDriver and may need specific browser installations (e.g., Tor Browser as indicated in comments within `calc.py`) to function correctly with eCalc's website.