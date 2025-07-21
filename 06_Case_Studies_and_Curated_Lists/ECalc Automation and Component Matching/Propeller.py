import pandas as pd
class Propeller:
    def __init__(self,NB:float, pitch:float, diameter:float,weight, Tc=1, Pc=1.08, eff:float=None):
        self.NB = NB
        self.pitch = pitch
        self.diameter = diameter
        self.Tc = Tc
        self.Pc = Pc
        self.weight = weight
        if not eff:
            self._get_eff()
        else:
            self.eff = eff


    def _get_eff(self):
        if self.NB == 2:
            self.eff = 1
        elif self.NB == 3:
            self.eff = 0.9
        else:
            raise Exception("Number of Blades can only be 2 or 3")

    @classmethod
    def from_inventory(cls, inventory_entry):
        """
        Creates a Propeller instance from a pandas Series representing an inventory entry
        by finding the best match in a full battery database.
        """
        best_match = find_best_match(inventory_entry)
        if best_match is not None:
            return cls(NB=inventory_entry.get('No. of Blades'),pitch=inventory_entry.get('Pitch'),diameter=inventory_entry.get('Diameter'), Tc=best_match.get('Tconst'),Pc=best_match.get('Pconst'), weight=inventory_entry.get('Weight (g)'))

def find_best_match(inventroy_entry):
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