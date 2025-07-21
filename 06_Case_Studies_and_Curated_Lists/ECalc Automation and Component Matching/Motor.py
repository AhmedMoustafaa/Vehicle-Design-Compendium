import pandas as pd
from fuzzywuzzy import fuzz
import re
class Motor:
    """
    Represents a motor, allowing initialization with specific parameters
    or by matching an inventory entry to a full database.
    """
    def __init__(self, kv, R_in, i0, weight, manuf=None, name=None):
        self.kv = kv
        self.kt = 9.5694 / self.kv if self.kv != 0 else 0
        self.Rin = R_in
        self.i0 = i0
        self.manuf = manuf
        self.name = name
        self.weight = weight


    @classmethod
    def from_inventory(cls, inventory_entry):
        """
        Creates a Motor instance from a pandas Series representing an inventory entry
        by finding the best match in a full motor database.
        """
        # Pass the globally loaded full_database_df to find_best_match
        best_match = find_best_match(inventory_entry)

        if best_match is not None:
            # Extract data from best_match
            UDCkv = inventory_entry.get('Kv')
            UDCRin = best_match.get('Rin')
            UDCweight = best_match.get('weight')
            UDCManuf = best_match.get('manufacturer')
            UDCmotor_name = best_match.get('type')  # 'type' from full_database corresponds to motor name/model
            UDCi0 = best_match.get('Io')

            return cls(kv=UDCkv, R_in=UDCRin, i0=UDCi0, weight=UDCweight,
                       manuf=UDCManuf, name=UDCmotor_name)
        else:
            return None  # No suitable match found

def clean_model_name(name):
    """
    Removes text in parentheses from a string and strips whitespace.
    E.g., "KDE5215XF-330 (330)" becomes "KDE5215XF-330".
    """
    if isinstance(name, str):
        return re.sub(r'\s*\(.*\)\s*', '', name).strip()
    return name


def find_best_match(inventory_motor, fuzzy_threshold=70):
    """
    Finds the best matching motor from a full database DataFrame for a given inventory motor.

    Comparison Logic (in order of priority):
    1. Exact match (case-insensitive) of the original inventory 'Model' against the original database 'type'.
    2. Exact match (case-insensitive) of the cleaned inventory 'Model' against the cleaned database 'type'.
    3. Fuzzy match (fuzz.token_set_ratio) of the original inventory 'Model' against the original database 'type'
       with a score above 'fuzzy_threshold'.

    Args:
        inventory_motor (pd.Series): A pandas Series representing one motor from the inventory.
                                     Expected keys: 'Model'.
        fuzzy_threshold (int): The minimum fuzz.ratio score for a fuzzy match to be considered valid.

    Returns:
        pd.Series or None: The best matching motor as a pandas Series,
                           or None if no suitable match is found.
    """
    # Define file path for the full motor database
    full_database_motor_file_path = r'resources/ecalcData/pkl_data/motors.pkl'

    # Load the full database directly within the function
    try:
        full_database_df = pd.read_pickle(full_database_motor_file_path)
    except FileNotFoundError:
        print(
            f"Error: Full Motor database PKL file not found at {full_database_motor_file_path}. Please ensure the file exists.")
        return None
    except Exception as e:
        print(f"Error loading full motor database from PKL within find_best_match: {e}")
        return None

    inventory_Model = inventory_motor.get('Model')

    if not isinstance(inventory_Model, str):
        print(f"Warning: 'Model' missing or invalid (expected string) in inventory entry: {inventory_motor.to_dict()}")
        return None

    exact_matches_original = full_database_df[full_database_df['type'].str.lower() == inventory_Model.lower()]
    if not exact_matches_original.empty:
        return exact_matches_original.iloc[0]

    full_database_df['cleaned_type'] = full_database_df['type'].apply(clean_model_name)
    cleaned_inventory_model = clean_model_name(inventory_Model)

    exact_matches_cleaned = full_database_df[
        full_database_df['cleaned_type'].str.lower() == cleaned_inventory_model.lower()]

    if not exact_matches_cleaned.empty:
        return exact_matches_cleaned.iloc[0].drop('cleaned_type')
    else:
        best_fuzzy_match = None
        highest_score = -1

        for index, db_motor in full_database_df.iterrows():
            db_motor_original_type = db_motor.get('type')
            if isinstance(db_motor_original_type, str):
                score = fuzz.token_set_ratio(inventory_Model.lower(), db_motor_original_type.lower())
                if score > highest_score and score >= fuzzy_threshold:
                    highest_score = score
                    best_fuzzy_match = db_motor

        if best_fuzzy_match is not None:
            return best_fuzzy_match.drop('cleaned_type')
        return None



if __name__ == '__main__':
    inventory_file_path = r'resources/udcData/udcData.xlsx'
    full_database_file_path = r'resources/ecalcData/pkl_data/motors.pkl'
    inventory_motor_df = pd.read_excel(inventory_file_path, sheet_name='Available Motors')


    print("\n--- Finding Best Motor Matches ---")

    for index, inv_motor_series in inventory_motor_df.iterrows():
        my_motor_obj = Motor.from_inventory(inv_motor_series)

        print(f"\n--- Inventory Motor Object (Row {index}) ---")
        if my_motor_obj is not None:
            print(f"Inventory Motor Model: {inv_motor_series.get('Model')}")
            print(f"Matched Motor Name: {my_motor_obj.name}")
            print(f"Manufacturer: {my_motor_obj.manuf}")
            print(f"KV: {my_motor_obj.kv}")
            print(f"R_in: {my_motor_obj.Rin:.4f} Ohms")
            print(f"i0: {my_motor_obj.i0} A")
            print(f"Weight: {my_motor_obj.weight} g")
        else:
            print(f"No suitable match found for Inventory Motor (Row {index}): Model: {inv_motor_series.get('Model')}")

