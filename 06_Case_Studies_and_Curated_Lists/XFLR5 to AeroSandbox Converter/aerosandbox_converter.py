"Turn XFLR5AirPlane object to aerosandbox object, then perform VLM aerodynamic and stability analysis"

import aerosandbox as asb
import aerosandbox.numpy as np
from typing import List, Tuple, Dict, Optional

from xflr5_parser import XFLR5Airplane, XFLR5Wing, XFLR5Section


class AeroSandboxConverter:
    """
    Converts an XFLR5Airplane object into an aerosandbox.Airplane object.
    Calculates the aircraft's Center of Gravity (CG) based on the Neutral Point (NP)
    (determined by Cm_alpha = 0 via VLM optimization) and a target static margin.
    """

    @staticmethod
    def _create_asb_wing_from_xflr5_wing(
            xflr5_wing: XFLR5Wing,
            length_unit_to_meter: float,
            is_fin: bool = False
    ) -> asb.Wing:
        """
        Converts an XFLR5Wing object (main wing, horizontal stab, vertical stab)
        into an aerosandbox.Wing object.
        """
        asb_xsecs: List[asb.WingXSec] = []
        naca2412_airfoil = asb.Airfoil("NACA2412")
        current_cumulative_z_offset = 0.0

        for i, xflr5_sec in enumerate(xflr5_wing.sections):
            # Convert units for chord and x_offset
            chord = xflr5_sec.chord * length_unit_to_meter
            x_offset_local = xflr5_sec.x_offset * length_unit_to_meter

            # Determine airfoil for this section
            foil_name_xflr5 = xflr5_sec.left_foil_name
            formatted_foil_name = foil_name_xflr5.lower().replace(" ", "")

            #if formatted_foil_name.startswith("naca"):  # Check the formatted name
            airfoil_for_section = asb.Airfoil(formatted_foil_name)

            # XFLR5's `Tilt_angle` is the global wing incidence.
            # XFLR5's `Twist` is local twist relative to that.
            # AeroSandbox `twist` is the total twist angle for the section.
            # So, `Tilt_angle` acts as a uniform twist applied to all sections of this wing.
            combined_twist_angle = xflr5_wing.tilt_angle + xflr5_sec.twist

            # Determine local xyz_le for the WingXSec (relative to the wing's overall root LE)
            if not is_fin:  # For main wing and horizontal stabilizers
                y_le_local = xflr5_sec.y_position * length_unit_to_meter
                x_le_local = x_offset_local

                # Calculate z_le based on cumulative dihedral
                if i > 0:
                    prev_xflr5_sec = xflr5_wing.sections[i - 1]
                    delta_y = (xflr5_sec.y_position - prev_xflr5_sec.y_position) * length_unit_to_meter
                    dihedral_of_segment = np.radians(xflr5_wing.sections[i - 1].dihedral)
                    current_cumulative_z_offset += delta_y * np.tan(dihedral_of_segment)
                z_le_local = current_cumulative_z_offset  # Relative to the wing's root LE Z

                asb_xyz_le = np.array([x_le_local, y_le_local, z_le_local])

            else:  # For vertical stabilizers (fins)
                x_le_local = x_offset_local
                y_le_local = 0.0
                z_le_local = xflr5_sec.y_position * length_unit_to_meter  # XFLR5's y_position is vertical span for fins

                asb_xyz_le = np.array([x_le_local, y_le_local, z_le_local])

            asb_xsecs.append(asb.WingXSec(
                xyz_le=asb_xyz_le,
                chord=chord,
                airfoil=airfoil_for_section,
                twist=combined_twist_angle,  # Total twist for the section
                #analysis_specific_options= {asb.VortexLatticeMethod: dict(
                #    chordwise_resolution=xflr5_sec.x_panels,
                #    spanwise_resolution=xflr5_sec.y_panels,
                #)}
            ))

        asb_symmetric_flag = xflr5_wing.symmetric if not is_fin else False  # Single vertical fin is not symmetric in ASB sense

        return asb.Wing(
            name=xflr5_wing.name,
            xsecs=asb_xsecs,
            symmetric=asb_symmetric_flag
        )

    @staticmethod
    def calculate_dihedral_angles(asb_airplane: asb.Airplane) -> Dict[str, List[float]]:
        """
        Calculates the dihedral angle for each segment of the wings and stabilizers.

        Args:
            asb_airplane: An aerosandbox.Airplane object.

        Returns:
            A dictionary where keys are wing names and values are lists of
            dihedral angles (in degrees) for each segment of that wing.
        """
        dihedral_data = {}
        for wing in asb_airplane.wings:
            # Skip vertical stabilizers as dihedral is not applicable in the same way
            if "fin" in wing.name.lower():
                continue

            wing_dihedrals = []
            for i in range(len(wing.xsecs) - 1):
                section1 = wing.xsecs[i]
                section2 = wing.xsecs[i + 1]

                delta_y = section2.xyz_le[1] - section1.xyz_le[1]
                delta_z = section2.xyz_le[2] - section1.xyz_le[2]

                angle_rad = np.arctan2(delta_z, delta_y)
                angle_deg = np.degrees(angle_rad)
                wing_dihedrals.append(angle_deg)

            dihedral_data[wing.name] = wing_dihedrals

        return dihedral_data

    @staticmethod
    def _calculate_mac_x_le(wing: asb.Wing) -> float:
        """
        Calculates the x-coordinate of the Mean Aerodynamic Chord (MAC)'s leading edge
        for a given ASB Wing object.
        This calculates the weighted average of the x_le of each section.
        """
        if not wing.xsecs:
            return 0.0

        total_weighted_x_le = 0.0
        total_segment_area = 0.0

        for i in range(len(wing.xsecs) - 1):
            xsec1 = wing.xsecs[i]
            xsec2 = wing.xsecs[i + 1]

            # Approximate segment area as trapezoid area
            chord_avg = (xsec1.chord + xsec2.chord) / 2
            span_delta_y = xsec2.xyz_le[1] - xsec1.xyz_le[1]
            segment_area = chord_avg * span_delta_y

            # x_le_avg of the segment
            x_le_avg_segment = (xsec1.xyz_le[0] + xsec2.xyz_le[0]) / 2

            total_weighted_x_le += x_le_avg_segment * segment_area
            total_segment_area += segment_area

        if total_segment_area == 0:
            # Fallback for single section wing or zero span
            if wing.xsecs:
                return wing.xsecs[0].xyz_le[0]
            return 0.0  # Should not happen if xsecs is not empty

        return total_weighted_x_le / total_segment_area

    @classmethod
    def to_aerosandbox(cls, xflr5_airplane: XFLR5Airplane,
                       target_static_margin: float = 0.15,  # 15% static margin
                       cruise_speed_mps: float = 15.0
                       ) -> asb.Airplane:
        """
        Converts an XFLR5Airplane object to an aerosandbox.Airplane object.
        Calculates the aircraft's Center of Gravity (CG) based on the Neutral Point (NP)
        (determined by Cm_alpha = 0 via VLM optimization) and a target static margin.
        """
        asb_wings: List[asb.Wing] = []
        asb_fuselages: List[asb.Fuselage] = []

        wing_translations: Dict[str, np.ndarray] = {}  # Use np.ndarray for vectors

        # Main Wing
        if xflr5_airplane.main_wing:
            asb_main_wing_untranslated = cls._create_asb_wing_from_xflr5_wing(
                xflr5_airplane.main_wing, xflr5_airplane.length_unit_to_meter, is_fin=False
            )
            asb_wings.append(asb_main_wing_untranslated)
            wing_translations[asb_main_wing_untranslated.name] = np.array([
                p * xflr5_airplane.length_unit_to_meter for p in xflr5_airplane.main_wing.position
            ])

        # Horizontal Stabilizers
        for h_stab in xflr5_airplane.horizontal_stabilizers:
            asb_h_stab_untranslated = cls._create_asb_wing_from_xflr5_wing(
                h_stab, xflr5_airplane.length_unit_to_meter, is_fin=False
            )
            asb_wings.append(asb_h_stab_untranslated)
            wing_translations[asb_h_stab_untranslated.name] = np.array([
                p * xflr5_airplane.length_unit_to_meter for p in h_stab.position
            ])

        # Vertical Stabilizers (fins)
        for v_stab in xflr5_airplane.vertical_stabilizers:
            asb_v_stab_untranslated = cls._create_asb_wing_from_xflr5_wing(
                v_stab, xflr5_airplane.length_unit_to_meter, is_fin=True
            )
            asb_wings.append(asb_v_stab_untranslated)
            wing_translations[asb_v_stab_untranslated.name] = np.array([
                p * xflr5_airplane.length_unit_to_meter for p in v_stab.position
            ])

        # Create the final list of translated wings for the airplane
        translated_wings = []
        for wing in asb_wings:
            translation_vector = wing_translations.get(wing.name, np.array([0., 0., 0.]))  # Default if somehow missing
            translated_wings.append(wing.translate(translation_vector))

        s_ref, b_ref = 1.0, 1.0  # Fallback values
        xyz_ref = np.array([0.0, 0.0, 0.0])  # Fallback for xyz_ref
        main_wing_mac = 0.0

        if xflr5_airplane.main_wing and len(translated_wings) > 0:
            # Find the actual translated main wing from the list
            current_asb_main_wing = None
            for tw in translated_wings:
                if tw.name == xflr5_airplane.main_wing.name:
                    current_asb_main_wing = tw
                    break

            if current_asb_main_wing:
                s_ref = current_asb_main_wing.area()
                b_ref = current_asb_main_wing.span()
                main_wing_mac = current_asb_main_wing.mean_aerodynamic_chord()

                # Calculate the x-position of the MAC leading edge for the main wing
                # This uses our new helper function
                mac_x_le_main_wing_global = cls._calculate_mac_x_le(current_asb_main_wing)

                # Set xyz_ref to the leading edge of the main wing's MAC.
                # Y and Z of xyz_ref are typically 0 unless your aircraft has a significant offset.
                # For typical aircraft, MAC is along the XZ plane.
                xyz_ref = np.array([mac_x_le_main_wing_global, 0.0, 0.0])  # Y and Z are usually 0 for xyz_ref
            else:
                print(
                    "Warning: Translated main wing ASB object not found. Cannot accurately calculate s_ref, b_ref, MAC, or xyz_ref.")
        else:
            print(
                "Warning: No main wing found in XFLR5 data or no wings created. Cannot accurately calculate s_ref, b_ref, MAC, or xyz_ref.")

        # Calculate Neutral Point (x_np) as an Optimization Problem
        opti = asb.Opti()
        x_np_opt = opti.variable(init_guess=main_wing_mac * 0.25, lower_bound=0, upper_bound=xflr5_airplane.horizontal_stabilizers[0].position[0])

        provisional_airplane = asb.Airplane(
            name=xflr5_airplane.name,
            wings=translated_wings,
            fuselages=asb_fuselages,
            s_ref=s_ref,
            b_ref=b_ref,
            xyz_ref=x_np_opt
        )
        op_point = asb.OperatingPoint(
            velocity=cruise_speed_mps,
            alpha=0,
            beta=0,
        )

        # Create an AeroProblem with the provisional airplane and operating point.
        aero_problem = asb.VortexLatticeMethod(
            airplane=provisional_airplane,
            op_point=op_point,
            align_trailing_vortices_with_wind=False
        ).run_with_stability_derivatives(alpha=True,beta=False,p=False,q=False,r=False)

        Cm_alpha_at_provisional_cg = aero_problem['Cma']

        # Set the constraint: Cm_alpha = 0
        opti.subject_to(Cm_alpha_at_provisional_cg == 0)
        try:
            sol = opti.solve(verbose=False)
            x_np_calculated = sol.value(x_np_opt)
            print(f"Neutral Point (x_np) calculated via VLM optimization: {x_np_calculated:.3f} m")
            print(f"{sol.value('x_np')}")
        except Exception as e:
            print(f"Error solving for Neutral Point using optimization for '{xflr5_airplane.name}': {e}")
            # Fallback if optimization fails: use a common heuristic
            if main_wing_mac > 0:
                x_np_calculated = xyz_ref[0] + main_wing_mac * 0.25  # 25% MAC from aircraft reference point
                print(f"Falling back to a heuristic NP: {x_np_calculated:.3f} m (xyz_ref[0] + 25% MAC)")
            else:
                x_np_calculated = xyz_ref[0]  # Ultimate fallback if MAC is also zero or invalid
                print(f"Falling back to xyz_ref[0] as NP: {x_np_calculated:.3f} m (MAC not available for heuristic)")

        # Calculate the final x_cg based on the calculated Neutral Point and target static margin
        # Static Margin (SM) = (x_np - x_cg) / MAC
        # So, x_cg = x_np - SM * MAC

        if main_wing_mac == 0:
            print(f"Warning: Main wing MAC is zero or could not be calculated for {xflr5_airplane.name}. "
                  f"Setting x_cg to Neutral Point (x_np) as a fallback.")
            x_cg = x_np_calculated
        else:
            x_cg = x_np_calculated - target_static_margin * main_wing_mac
            print(f"Center of Gravity = {x_cg:.2f}")
            print(f"MAC is {main_wing_mac}")

        y_cg = 0.0
        z_cg = 0.0
        total_mass_kg = 3.0
        xyz_ref = [x_cg, y_cg, z_cg]
        return asb.Airplane(
            name=xflr5_airplane.name,
            wings=translated_wings,
            fuselages=asb_fuselages,
            s_ref=s_ref,
            b_ref=b_ref,
            xyz_ref=xyz_ref
        )



if __name__ == "__main__":
    import os
    import sys

    # Add parent directory to path to import xflr5_parser from src
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.xflr5_parser import XFLR5Parser, XFLR5Airplane

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
    test_filepath = os.path.join("data", "input_xml_files", test_filename)

    os.makedirs(os.path.join("data", "input_xml_files"), exist_ok=True)
    with open(test_filepath, "w") as f:
        f.write(sample_xml_content)

    print(f"Sample XML file created at: {test_filepath}\n")

    try:
        # 1. Parse XFLR5 XML
        xflr5_airplane_data = XFLR5Parser.from_xml(test_filepath)
        print("XFLR5 Airplane data parsed:")
        print(xflr5_airplane_data)
        print("-" * 30)

        # 2. Convert to AeroSandbox Airplane
        # We need to pass the target static margin and cruise speed for NP calculation.
        asb_airplane = AeroSandboxConverter.to_aerosandbox(
            xflr5_airplane_data,
        )
        print("Converted to AeroSandbox Airplane object:")
        print(asb_airplane)
        print(f"  ASB Airplane Name: {asb_airplane.name}")
        print(f"  ASB Airplane Reference Point (xyz_ref): {asb_airplane.xyz_ref}")
        print(f"  Number of ASB Wings: {len(asb_airplane.wings)}")

        for i, wing in enumerate(asb_airplane.wings):
            print(f"    ASB Wing {i + 1} Name: {wing.name}")
            print(f"      Symmetric: {wing.symmetric}")
            print(f"      Number of Sections: {len(wing.xsecs)}")
            for j, section in enumerate(wing.xsecs):
                print(f"        Section {j + 1}: xyz_le={section.xyz_le}, chord={section.chord:.3f}, "
                      f"twist={section.twist:.1f} deg, airfoil={section.airfoil.name}, ")
                     # f"dihedral_angle={section.dihedral_angle:.1f} deg")

        print("-" * 30)
        print("Calculating dihedral angles for validation:")
        dihedral_results = AeroSandboxConverter.calculate_dihedral_angles(asb_airplane)
        for wing_name, angles in dihedral_results.items():
            formatted_angles = [f"{angle:.2f}°" for angle in angles]
            print(f"  - {wing_name}: {formatted_angles}")

        # Neutral Point Calculated via aerosandbox


    except Exception as e:
        print(f"An error occurred during conversion: {e}")
    finally:
        if os.path.exists(test_filepath):
            os.remove(test_filepath)
            print(f"\nCleaned up dummy file: {test_filepath}")