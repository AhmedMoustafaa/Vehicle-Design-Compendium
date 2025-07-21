"handles the xflr5 xml files, output an object (XFLR5AirPlane) containing the geometry"
import xml.etree.ElementTree as ET
import os
import re
from typing import List, Tuple, Optional


class XFLR5Section:
    """Represents a single section within a wing component."""
    def __init__(self,
                 y_position: float,
                 chord: float,
                 x_offset: float,
                 dihedral: float,
                 twist: float,
                 x_panels: int,
                 x_panel_dist: str,
                 y_panels: int,
                 y_panel_dist: str,
                 left_foil_name: str,
                 right_foil_name: str):
        self.y_position = y_position  # Spanwise position
        self.chord = chord            # Chord length
        self.x_offset = x_offset      # X-offset relative to wing origin
        self.dihedral = dihedral      # Dihedral angle (degrees)
        self.twist = twist            # Twist angle (degrees)
        self.x_panels = x_panels      # Number of panels in chordwise direction
        self.x_panel_distribution = x_panel_dist # Chordwise panel distribution
        self.y_panels = y_panels      # Number of panels in spanwise direction to next section
        self.y_panel_distribution = y_panel_dist # Spanwise panel distribution
        self.left_foil_name = left_foil_name
        self.right_foil_name = right_foil_name

    def __repr__(self):
        return (
            f"Section(y={self.y_position:.3f}, Chord={self.chord:.3f}, "
            f"Dihedral={self.dihedral:.1f}, Twist={self.twist:.1f}, "
            f"Foil={self.left_foil_name})"
        )

class XFLR5Wing:
    """Represents a wing component (main wing, elevator, fin, etc.)."""
    def __init__(self,
                 name: str,
                 wing_type: str,
                 position: Tuple[float, float, float],
                 tilt_angle: float,
                 symmetric: bool,
                 is_fin: bool,
                 is_double_fin: bool,
                 is_sym_fin: bool,
                 volume_mass: float, # This seems to be a placeholder for inertia in XFLR5
                 sections: List[XFLR5Section]):
        self.name = name
        self.type = wing_type
        self.position = position # X, Y, Z position of the wing's root leading edge
        self.tilt_angle = tilt_angle # Global tilt of the wing (degrees)
        self.symmetric = symmetric # Is the wing mirrored?
        self.is_fin = is_fin       # Is it a vertical fin?
        self.is_double_fin = is_double_fin
        self.is_sym_fin = is_sym_fin
        self.volume_mass = volume_mass # From <Inertia><Volume_Mass>
        self.sections = sections

    def __repr__(self):
        return (
            f"Wing(Name='{self.name}', Type='{self.type}', Pos={self.position}, "
            f"Sections={len(self.sections)})"
        )

class XFLR5Airplane:
    """Represents the entire airplane parsed from an XFLR5 XML file."""
    def __init__(self,
                 name: str,
                 has_body: bool,
                 length_unit_to_meter: float,
                 mass_unit_to_kg: float,
                 main_wing: Optional[XFLR5Wing] = None,
                 horizontal_stabilizers: List[XFLR5Wing] = None,
                 vertical_stabilizers: List[XFLR5Wing] = None,
                 other_wings: List[XFLR5Wing] = None,
                 designer_name: Optional[str] = None,
                 designer_email: Optional[str] = None):
        self.name = name
        self.has_body = has_body
        self.length_unit_to_meter = length_unit_to_meter
        self.mass_unit_to_kg = mass_unit_to_kg
        self.main_wing = main_wing
        self.horizontal_stabilizers = horizontal_stabilizers if horizontal_stabilizers is not None else []
        self.vertical_stabilizers = vertical_stabilizers if vertical_stabilizers is not None else []
        self.other_wings = other_wings if other_wings is not None else []
        self.designer_name = designer_name
        self.designer_email = designer_email

    def __repr__(self):
        return (
            f"XFLR5Airplane(Name='{self.name}', MainWing={self.main_wing is not None}, "
            f"HStabs={len(self.horizontal_stabilizers)}, VStabs={len(self.vertical_stabilizers)}, "
            f"Email='{self.designer_email}')"
        )

    def get_designer_email(self) -> Optional[str]:
        """Returns the designer email, typically extracted during parsing."""
        return self.designer_email


class XFLR5Parser:
    """
    Parses an XFLR5 XML file and converts it into an XFLR5Airplane object.
    """
    @staticmethod
    def _parse_float(element: ET.Element) -> float:
        """Helper to parse float text content from an XML element."""
        return float(element.text.strip())

    @staticmethod
    def _parse_int(element: ET.Element) -> int:
        """Helper to parse integer text content from an XML element."""
        return int(element.text.strip())

    @staticmethod
    def _parse_bool(element: ET.Element) -> bool:
        """Helper to parse boolean text content from an XML element."""
        return element.text.strip().lower() == 'true'

    @staticmethod
    def _parse_position(element: ET.Element) -> Tuple[float, float, float]:
        """Helper to parse a comma-separated position string into a tuple."""
        pos_str = element.text.strip()
        x, y, z = map(float, pos_str.split(','))
        return x, y, z

    @classmethod
    def _parse_section(cls, section_element: ET.Element) -> XFLR5Section:
        """Parses a single Section sub-element."""
        y_position = cls._parse_float(section_element.find('y_position'))
        chord = cls._parse_float(section_element.find('Chord'))
        x_offset = cls._parse_float(section_element.find('xOffset'))
        dihedral = cls._parse_float(section_element.find('Dihedral'))
        twist = cls._parse_float(section_element.find('Twist'))
        x_panels = cls._parse_int(section_element.find('x_number_of_panels'))
        x_panel_dist = section_element.find('x_panel_distribution').text.strip()
        y_panels = cls._parse_int(section_element.find('y_number_of_panels'))
        y_panel_dist = section_element.find('y_panel_distribution').text.strip()
        left_foil_name = section_element.find('Left_Side_FoilName').text.strip()
        right_foil_name = section_element.find('Right_Side_FoilName').text.strip()

        return XFLR5Section(
            y_position, chord, x_offset, dihedral, twist,
            x_panels, x_panel_dist, y_panels, y_panel_dist,
            left_foil_name, right_foil_name
        )

    @classmethod
    def _parse_wing(cls, wing_element: ET.Element) -> XFLR5Wing:
        """Parses a wing (or stabilizer) component from the XML."""
        name = wing_element.find('Name').text.strip()
        wing_type = wing_element.find('Type').text.strip()
        position = cls._parse_position(wing_element.find('Position'))
        tilt_angle = cls._parse_float(wing_element.find('Tilt_angle'))
        symmetric = cls._parse_bool(wing_element.find('Symetric'))
        is_fin = cls._parse_bool(wing_element.find('isFin'))
        is_double_fin = cls._parse_bool(wing_element.find('isDoubleFin'))
        is_sym_fin = cls._parse_bool(wing_element.find('isSymFin'))
        volume_mass = cls._parse_float(wing_element.find('Inertia').find('Volume_Mass'))

        sections_data = []
        for section_elem in wing_element.find('Sections').findall('Section'):
            sections_data.append(cls._parse_section(section_elem))

        return XFLR5Wing(
            name, wing_type, position, tilt_angle,
            symmetric, is_fin, is_double_fin, is_sym_fin, volume_mass, sections_data
        )

    @staticmethod
    def _extract_info_from_filename(filepath: str) -> Tuple[Optional[str], Optional[str]]:
        filename = os.path.basename(filepath)
        filename_no_ext = os.path.splitext(filename)[0]

        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', filename_no_ext)
        if not email_match:
            return None, None
        email = email_match.group(1)
        parts = filename_no_ext.split(' - ', 1)
        if len(parts) == 2:
            name = parts[1].strip()
            return email, name

        return email, None

    @staticmethod
    def _extract_designer_email_from_filename(filepath: str) -> Optional[str]:
        filename = os.path.basename(filepath)
        match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', filename)
        if match:
            return match.group(1)
        return None

    @classmethod
    def from_xml(cls, filepath: str) -> XFLR5Airplane:
        """
        Parses an XFLR5 XML file and returns an XFLR5Airplane object.
        """
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Error parsing XML file {filepath}: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"XML file not found at {filepath}")

        # Extract units
        units_elem = root.find('Units')
        length_unit_to_meter = cls._parse_float(units_elem.find('length_unit_to_meter'))
        mass_unit_to_kg = cls._parse_float(units_elem.find('mass_unit_to_kg'))

        # Extract Plane level data
        plane_elem = root.find('Plane')
        plane_name = plane_elem.find('Name').text.strip()
        has_body = cls._parse_bool(plane_elem.find('has_body'))

        main_wing = None
        horizontal_stabs: List[XFLR5Wing] = []
        vertical_stabs: List[XFLR5Wing] = []
        other_wings: List[XFLR5Wing] = []

        for wing_elem in plane_elem.findall('wing'):
            wing = cls._parse_wing(wing_elem)
            if wing.type == "MAINWING":
                main_wing = wing
            elif wing.type == "ELEVATOR":
                horizontal_stabs.append(wing)
            elif wing.type == "FIN":
                vertical_stabs.append(wing)
            else:
                other_wings.append(wing)

        designer_email, designer_name = cls._extract_info_from_filename(filepath)

        return XFLR5Airplane(
            name=plane_name,
            has_body=has_body,
            length_unit_to_meter=length_unit_to_meter,
            mass_unit_to_kg=mass_unit_to_kg,
            main_wing=main_wing,
            horizontal_stabilizers=horizontal_stabs,
            vertical_stabilizers=vertical_stabs,
            other_wings=other_wings,
            designer_email=designer_email,
            designer_name = designer_name,

        )

# Example Usage (for testing the parser directly)
if __name__ == "__main__":
    # Create a dummy XML file for testing
    sample_xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE explane>
<explane version="1.0">
    <Units>
        <length_unit_to_meter>1</length_unit_to_meter>
        <mass_unit_to_kg>1</mass_unit_to_kg>
    </Units>
    <Plane>
        <Name>Task 3 (lateral stability)</Name>
        <Description></Description>
        <Inertia/>
        <has_body>false</has_body>
        <wing>
            <Name>Main Wing</Name>
            <Type>MAINWING</Type>
            <Color>
                <red>248</red>
                <green>187</green>
                <blue>208</blue>
                <alpha>255</alpha>
            </Color>
            <Description></Description>
            <Position>         0,           0,           0</Position>
            <Tilt_angle>  0.000</Tilt_angle>
            <Symetric>true</Symetric>
            <isFin>false</isFin>
            <isDoubleFin>false</isDoubleFin>
            <isSymFin>false</isSymFin>
            <Inertia>
                <Volume_Mass>  0.000</Volume_Mass>
            </Inertia>
            <Sections>
                <Section>
                    <y_position>  0.000</y_position>
                    <Chord>  0.370</Chord>
                    <xOffset>  0.000</xOffset>
                    <Dihedral>  2.000</Dihedral>
                    <Twist>  0.000</Twist>
                    <x_number_of_panels>30</x_number_of_panels>
                    <x_panel_distribution>COSINE</x_panel_distribution>
                    <y_number_of_panels>30</y_number_of_panels>
                    <y_panel_distribution>COSINE</y_panel_distribution>
                    <Left_Side_FoilName>NACA 2412</Left_Side_FoilName>
                    <Right_Side_FoilName>NACA 2412</Right_Side_FoilName>
                </Section>
                <Section>
                    <y_position>  1.080</y_position>
                    <Chord>  0.370</Chord>
                    <xOffset>  0.000</xOffset>
                    <Dihedral>  0.000</Dihedral>
                    <Twist>  0.000</Twist>
                    <x_number_of_panels>13</x_number_of_panels>
                    <x_panel_distribution>COSINE</x_panel_distribution>
                    <y_number_of_panels>5</y_number_of_panels>
                    <y_panel_distribution>UNIFORM</y_panel_distribution>
                    <Left_Side_FoilName>NACA 2412</Left_Side_FoilName>
                    <Right_Side_FoilName>NACA 2412</Right_Side_FoilName>
                </Section>
            </Sections>
        </wing>
        <wing>
            <Name>Elevator</Name>
            <Type>ELEVATOR</Type>
            <Color>
                <red>41</red>
                <green>182</green>
                <blue>246</blue>
                <alpha>255</alpha>
            </Color>
            <Description></Description>
            <Position>      0.98,           0,           0</Position>
            <Tilt_angle> -2.000</Tilt_angle>
            <Symetric>true</Symetric>
            <isFin>false</isFin>
            <isDoubleFin>false</isDoubleFin>
            <isSymFin>false</isSymFin>
            <Inertia>
                <Volume_Mass>  0.000</Volume_Mass>
            </Inertia>
            <Sections>
                <Section>
                    <y_position>  0.000</y_position>
                    <Chord>  0.220</Chord>
                    <xOffset>  0.000</xOffset>
                    <Dihedral>  0.000</Dihedral>
                    <Twist>  0.000</Twist>
                    <x_number_of_panels>20</x_number_of_panels>
                    <x_panel_distribution>COSINE</x_panel_distribution>
                    <y_number_of_panels>20</y_number_of_panels>
                    <y_panel_distribution>COSINE</y_panel_distribution>
                    <Left_Side_FoilName>NACA 0006</Left_Side_FoilName>
                    <Right_Side_FoilName>NACA 0006</Right_Side_FoilName>
                </Section>
                <Section>
                    <y_position>  0.342</y_position>
                    <Chord>  0.220</Chord>
                    <xOffset>  0.000</xOffset>
                    <Dihedral>  0.000</Dihedral>
                    <Twist>  0.000</Twist>
                    <x_number_of_panels>13</x_number_of_panels>
                    <x_panel_distribution>COSINE</x_panel_distribution>
                    <y_number_of_panels>7</y_number_of_panels>
                    <y_panel_distribution>UNIFORM</y_panel_distribution>
                    <Left_Side_FoilName>NACA 0006</Left_Side_FoilName>
                    <Right_Side_FoilName>NACA 0006</Right_Side_FoilName>
                </Section>
            </Sections>
        </wing>
        <wing>
            <Name>Fin</Name>
            <Type>FIN</Type>
            <Color>
                <red>79</red>
                <green>195</green>
                <blue>247</blue>
                <alpha>255</alpha>
            </Color>
            <Description></Description>
            <Position>      1.03,           0,           0</Position>
            <Tilt_angle>  0.000</Tilt_angle>
            <Symetric>true</Symetric>
            <isFin>true</isFin>
            <isDoubleFin>false</isDoubleFin>
            <isSymFin>false</isSymFin>
            <Inertia>
                <Volume_Mass>  0.000</Volume_Mass>
            </Inertia>
            <Sections>
                <Section>
                    <y_position>  0.000</y_position>
                    <Chord>  0.163</Chord>
                    <xOffset>  0.000</xOffset>
                    <Dihedral>  0.000</Dihedral>
                    <Twist>  0.000</Twist>
                    <x_number_of_panels>20</x_number_of_panels>
                    <x_panel_distribution>COSINE</x_panel_distribution>
                    <y_number_of_panels>20</y_number_of_panels>
                    <y_panel_distribution>COSINE</y_panel_distribution>
                    <Left_Side_FoilName>NACA 0006</Left_Side_FoilName>
                    <Right_Side_FoilName>NACA 0006</Right_Side_FoilName>
                </Section>
                <Section>
                    <y_position>  0.326</y_position>
                    <Chord>  0.163</Chord>
                    <xOffset>  0.000</xOffset>
                    <Dihedral>  0.000</Dihedral>
                    <Twist>  0.000</Twist>
                    <x_number_of_panels>13</x_number_of_panels>
                    <x_panel_distribution>COSINE</x_panel_distribution>
                    <y_number_of_panels>5</y_number_of_panels>
                    <y_panel_distribution>UNIFORM</y_panel_distribution>
                    <Left_Side_FoilName>NACA 0006</Left_Side_FoilName>
                    <Right_Side_FoilName>NACA 0006</Right_Side_FoilName>
                </Section>
            </Sections>
        </wing>
    </Plane>
</explane>
"""
    test_filename = "test_airplane_designer@example.com.xml"
    test_filepath = os.path.join("testdata", "input_xml_files", test_filename)
    os.makedirs(os.path.join("testdata", "input_xml_files"), exist_ok=True)

    with open(test_filepath, "w") as f:
        f.write(sample_xml_content)

    print(f"Sample XML file created at: {test_filepath}\n")

    try:
        airplane = XFLR5Parser.from_xml(test_filepath)
        print("Successfully parsed airplane data:")
        print(airplane)
        if airplane.main_wing:
            print(f"  Main Wing: {airplane.main_wing.name}, Sections: {len(airplane.main_wing.sections)}")
            print(f"    Main Wing Position: {airplane.main_wing.position}")
            for i, section in enumerate(airplane.main_wing.sections):
                print(f"      Section {i+1}: {section}")
        if airplane.horizontal_stabilizers:
            print(f"  Horizontal Stabilizers ({len(airplane.horizontal_stabilizers)}):")
            for hstab in airplane.horizontal_stabilizers:
                print(f"    - {hstab.name}, Position: {hstab.position}, Tilt: {hstab.tilt_angle}")
        if airplane.vertical_stabilizers:
            print(f"  Vertical Stabilizers ({len(airplane.vertical_stabilizers)}):")
            for vstab in airplane.vertical_stabilizers:
                print(f"    - {vstab.name}, Position: {vstab.position}")
        print(f"  Designer Email: {airplane.get_designer_email()}")

    except (ValueError, FileNotFoundError) as e:
        print(f"Error during parsing: {e}")
    finally:
        if os.path.exists(test_filepath):
            os.remove(test_filepath)
            print(f"\nCleaned up dummy file: {test_filepath}")