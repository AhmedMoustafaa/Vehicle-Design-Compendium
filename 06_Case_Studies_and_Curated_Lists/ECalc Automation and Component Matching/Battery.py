import pandas as pd
import math

# --- Battery Class ---

class Battery:
    """
    Represents a battery, allowing initialization with specific parameters
    or by matching an inventory entry to a full database.
    """
    def __init__(self, n_cells, voltpercell, cell_Rin, weight, capacity,
                 p_cells=1, battery_type=None, c_rating=None, crate_const=None):
        self.battery_type = battery_type
        self.n_cells = n_cells
        self.p_cells = p_cells
        self.voltpercell = voltpercell
        self.weight = weight
        self.cell_Rin = cell_Rin
        self.Rin = self.cell_Rin * self.n_cells / self.p_cells
        self.volt = self.n_cells * self.voltpercell
        self.capacity = capacity
        self.c_rating = c_rating # This will store the 'crate_max' from best_match
        self.crate_const = crate_const # To store 'crate_const' from best_match if needed for printing


    @classmethod
    def from_inventory(cls, inventory_entry):
        """
        Creates a Battery instance from a pandas Series representing an inventory entry
        by finding the best match in a full battery database.
        """
        best_match = find_best_match(inventory_entry)

        if best_match is not None:
            # Extract data from inventory_entry and best_match
            n_cells = inventory_entry.get('No. of cells', 1)
            p_cells = inventory_entry.get('Capacity') / best_match.get('capacity', 1) if best_match.get('capacity', 1) != 0 else 1

            voltpercell = 3.7
            cell_Rin = best_match.get('Rin')
            weight = best_match.get('weight')
            battery_type = best_match.get('text')
            capacity = inventory_entry.get('Capacity')
            c_rating = best_match.get('crate_max')
            crate_const = best_match.get('crate_const')

            return cls(n_cells=n_cells, voltpercell=voltpercell, cell_Rin=cell_Rin,
                       capacity=capacity, weight=weight, p_cells=p_cells,
                       battery_type=battery_type, c_rating=c_rating, crate_const=crate_const)
        else:
            return None # No suitable match found


def find_best_match(inventory_battery):
    full_database_file_path = r'resources/ecalcData/pkl_data/batteries.pkl'
    full_database_df = pd.read_pickle(full_database_file_path)
    best_match = None

    inventory_c_rating = inventory_battery.get('C-rating')
    inventory_capacity = inventory_battery.get('Capacity')

    if not isinstance(inventory_c_rating, (int, float)) or \
       not isinstance(inventory_capacity, (int, float)):
        print(f"Warning: 'C-rating' or 'Capacity' missing or invalid in inventory entry: {inventory_battery}")
        return None

    # Filter candidates based on C-rate within +/- 5 and explicitly create a copy
    candidates_df = full_database_df[abs(full_database_df['crate_max'] - inventory_c_rating ) <= 10].copy()
    candidates_df = candidates_df[candidates_df['cell_volt'] == 3.7].copy()

    if not candidates_df.empty:
        # Calculate absolute capacity difference for candidates
        candidates_df['capacity_diff'] = abs(candidates_df['capacity'] - inventory_capacity)
        # Find the candidate with the minimum capacity difference
        best_match = candidates_df.loc[candidates_df['capacity_diff'].idxmin()]
        # Remove the temporary 'capacity_diff' column before returning
        best_match = best_match.drop('capacity_diff')

    return best_match



if __name__ == '__main__':
    # Define file paths
    inventory_file_path = r'resources/udcData/udcData.xlsx'
    full_database_file_path = r'resources/ecalcData/pkl_data/batteries.pkl'
    inventory_df = pd.read_excel(inventory_file_path, sheet_name='Available Batteries')

    print("\n--- Finding Best Matches ---")
    for index, inv_bat_series in inventory_df.iterrows():
        my_battery_obj = Battery.from_inventory(inv_bat_series)

        print(f"\n--- Inventory Battery Object (Row {index}) ---")
        if my_battery_obj is not None:
            print(f"Inventory Battery No.: {inv_bat_series.get('Battery No.')}")
            print(f"Battery Type: {my_battery_obj.battery_type}")
            print(f"Cells (sP): {my_battery_obj.n_cells}s{my_battery_obj.p_cells:.2f}p")
            print(f"Voltage: {my_battery_obj.volt}V")
            print(f"Capacity: {my_battery_obj.capacity} mAh")
            print(f"C-rating (from matched max): {my_battery_obj.c_rating}C")
            print(f"C-rating (from matched const): {my_battery_obj.crate_const}C")
            print(f"Internal Resistance: {my_battery_obj.Rin:.4f} Ohms")
            print(f"Weight: {my_battery_obj.weight} g")

        else:
            print(f"No suitable match found for Inventory Battery (Row {index}): Battery No. {inv_bat_series.get('Battery No.')}, C-rating: {inv_bat_series.get('C-rating')}, Capacity: {inv_bat_series.get('Capacity')} mAh")
