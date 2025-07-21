import pandas as pd

def retrieve_battery(inventory_battery):
    """
    Comparison Logic:
    1. Find batteries in the full_database_df where 'crate_max' is within +/- 5 of
       the 'C-rating' from the inventory_battery.
    2. Among these candidates, select the one with the closest capacity to the
       'Capacity' of the inventory_battery.
    """
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
    candidates_df = full_database_df[abs(full_database_df['crate_max'] - inventory_c_rating) <= 5].copy()

    if not candidates_df.empty:
        # Calculate absolute capacity difference for candidates
        candidates_df['capacity_diff'] = abs(candidates_df['capacity'] - inventory_capacity)
        # Find the candidate with the minimum capacity difference
        best_match = candidates_df.loc[candidates_df['capacity_diff'].idxmin()]
        # Remove the temporary 'capacity_diff' column before returning
        best_match = best_match.drop('capacity_diff')

    return best_match


# Define file paths
inventory_file_path = r'resources/udcData/udcData.xlsx'
full_database_file_path = r'resources/ecalcData/pkl_data/batteries.pkl'

inventory_df = pd.read_excel(inventory_file_path,sheet_name='Available Batteries')
full_database_df = pd.read_pickle(full_database_file_path)



print("\n--- Finding Best Matches ---")

if not inventory_df.empty and not full_database_df.empty:
    for index, inv_bat in inventory_df.iterrows():
        match = retrieve_battery(inv_bat)
        if match is not None:
            print(f"\nInventory Battery (Row {index}): Battery No. {inv_bat.get('Battery No.')}, C-rating: {inv_bat.get('C-rating')}, Capacity: {inv_bat.get('Capacity')} mAh")
            print(f"Best Match Found: {match.get('text')}, C-rating: {match.get('crate_const')}, Capacity: {match.get('capacity')} mAh")
        else:
            print(f"\nNo suitable match found for Inventory Battery (Row {index}): Battery No. {inv_bat.get('Battery No.')}, C-rating: {inv_bat.get('C-rating')}, Capacity: {inv_bat.get('Capacity')} mAh")
else:
    print("\nCannot perform matching: Inventory or Full Database is empty or failed to load.")
