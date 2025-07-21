"""
Runs aerodynamic analysis on an AeroSandbox airplane object and returns key metrics.
"""
from typing import Dict, Any, Tuple

import aerosandbox as asb
import aerosandbox.numpy as np


class AerodynamicAnalyzer:
    """
    Performs VLM analysis to calculate key aerodynamic and performance metrics.
    """

    def __init__(self, asb_airplane: asb.Airplane, mass_kg: float):
        """
        Initializes the analyzer.

        Args:
            asb_airplane: The AeroSandbox airplane object.
            mass_kg: The mass of the aircraft in kilograms.
        """
        self.airplane = asb_airplane
        self.mass = mass_kg
        self.main_wing_airfoil = asb.Airfoil("NACA2412")

    def _get_trim_and_stability(self) -> Dict[str, Any]:
        """
        Finds the trimmed flight condition (L=W, Cm=0) and stability derivatives.
        """
        opti = asb.Opti()
        op_point = asb.OperatingPoint(
            velocity=opti.variable(init_guess=15, lower_bound=5, upper_bound=25),
            alpha=opti.variable(init_guess=3, lower_bound=-5, upper_bound=10)
        )
        vlm = asb.VortexLatticeMethod(airplane=self.airplane, op_point=op_point)
        aero = vlm.run()

        # Trim constraints
        weight = self.mass * 9.81
        tol = 1e-5
        opti.subject_to(aero['L'] - weight >= tol)
        opti.subject_to(aero['L'] - weight <= tol)
        opti.subject_to(aero['m_b'] >= tol)
        opti.subject_to(aero['m_b'] <= tol)

        try:
            sol = opti.solve(verbose=False)
            trimmed_op = asb.OperatingPoint(
                velocity=sol.value(op_point.velocity),
                alpha=sol.value(op_point.alpha)
            )
            final_aero = asb.VortexLatticeMethod(
                airplane=self.airplane, op_point=trimmed_op
            ).run_with_stability_derivatives(alpha=True,beta=True,p=False,q=False,r=False)

            return {
                "cruise_speed_ms": sol.value(op_point.velocity),
                "cruise_alpha_deg": sol.value(op_point.alpha),
                "cm_alpha": final_aero['Cma'],
                "cl_beta": final_aero['Clb'],
                "cn_beta": final_aero['Cnb'],
                "analysis_succeeded": True
            }
        except RuntimeError:
            return {"analysis_succeeded": False}

    def _calculate_stall_speed_range(self) -> Tuple[float, float]:
        """
        Calculates a range for the stall speed based on an assumed airfoil
        CL_max range is around 1.25].
        """
        cl_max_airfoil = 1.25

        # Assume whole-airplane CL_max is 85% of the airfoil's CL_max
        cl_max_airplane = 0.85 * cl_max_airfoil

        rho = 1.225
        weight = self.mass * 9.81
        s_ref = self.airplane.s_ref

        if s_ref <= 0:
            return 0.0, 0.0

        # V_stall = sqrt(2W / (rho * S * CL_max))
        # Note: Higher CL_max results in lower V_stall
        v_stall = np.sqrt(2 * weight / (rho * s_ref * cl_max_airplane))
        return v_stall

    def _get_aspect_ratio(self) -> float:
        return self.airplane.wings[0].aspect_ratio()

    def _get_cm_at_zero_lift(self) -> float:
        """Finds the pitching moment coefficient at the angle of attack where lift is zero."""
        opti = asb.Opti()
        alpha_at_zero_lift = opti.variable(init_guess=0)

        op_point_zerolift = asb.OperatingPoint(
            velocity=15,
            alpha=alpha_at_zero_lift
        )
        aero = asb.VortexLatticeMethod(self.airplane, op_point=op_point_zerolift).run()

        # Find alpha where CL is 0
        opti.subject_to(aero['CL'] == 0)
        opti.minimize(alpha_at_zero_lift ** 2)  # Minimize alpha to find the most relevant zero-lift point

        try:
            sol = opti.solve(verbose=False)
            # Rerun analysis at the found alpha to get the corresponding Cm
            final_op = asb.OperatingPoint(velocity=20, alpha=sol.value(alpha_at_zero_lift))
            final_aero = asb.VortexLatticeMethod(self.airplane, op_point=final_op).run()
            return final_aero['Cm']
        except RuntimeError:
            return 0

    def run_full_analysis(self) -> Dict[str, Any]:
        """Runs all analyses and returns a dictionary of the results."""
        print("Running aerodynamic analysis...")
        trim_results = self._get_trim_and_stability()

        if not trim_results.get("analysis_succeeded", False):
            print("Analysis failed to converge.")
            return {"analysis_succeeded": False}

        stall_speed_range = self._calculate_stall_speed_range()
        aspect_ratio = self._get_aspect_ratio()
        cm_at_zero_lift = self._get_cm_at_zero_lift()  # Call the new method

        full_results = {
            **trim_results,
            "stall_speed_ms_range": stall_speed_range,
            "aspect_ratio": aspect_ratio,
            "cm_at_zero_lift": cm_at_zero_lift  # Add to results
        }

        print("Analysis complete.")
        return full_results

if __name__ == '__main__':
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.xflr5_parser import XFLR5Parser
    from src.aerosandbox_converter import AeroSandboxConverter

    TEST_XML_PATH = os.path.join("testdata", "input_xml_files", "test_airplane_designer@example.com.xml")
    if not os.path.exists(TEST_XML_PATH):
        print(f"Error: Test XML file not found at {TEST_XML_PATH}")
        sys.exit(1)

    xflr5_plane = XFLR5Parser.from_xml(TEST_XML_PATH)
    asb_plane = AeroSandboxConverter.to_aerosandbox(xflr5_plane)

    analyzer = AerodynamicAnalyzer(asb_plane, mass_kg=3.0)
    analysis_data = analyzer.run_full_analysis()

    print("\n" + "=" * 15, "ANALYSIS RESULTS", "=" * 15)
    if analysis_data['analysis_succeeded']:
        for key, value in analysis_data.items():
            if isinstance(value, float):
                print(f"  {key:<25}: {value:.4f}")
            elif isinstance(value, tuple):
                print(f"  {key:<25}: ({value[0]:.2f}, {value[1]:.2f})")
            else:
                print(f"  {key:<25}: {value}")
    else:
        print("  Could not retrieve analysis data.")
    print("=" * 48)