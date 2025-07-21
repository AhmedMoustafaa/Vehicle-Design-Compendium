from Motor import Motor
from ESC import ESC
from Propeller import Propeller
from Battery import Battery
from calc import ecalc
import math
from sympy import symbols, solve, sqrt
from aerosandbox import Airplane
from aerosandbox import OperatingPoint
import aerosandbox.numpy as np
class Propulsion:
    def __init__(self,airplane:Airplane,operatingPoint:OperatingPoint,battery:Battery=None,motor:Motor=None,esc:ESC=None,propeller:Propeller=None,AnalysisMethod:str = 'ecalc',**kwargs):
        self.battery = battery
        # Dynamically delegate battery properties with a prefix
        if battery:
            for batt_name, batt_value in vars(battery).items():
                setattr(self, f"battery_{batt_name}", batt_value)
        else: self.battery_Rin = 0
        self.motor = motor
        if motor:
            for motor_name, motor_value in vars(motor).items():
                setattr(self, f"motor_{motor_name}", motor_value)
        else: self.motor_Rin = 0

        self.esc = esc
        if esc:
            for esc_name, esc_value in vars(esc).items():
                setattr(self, f"esc_{esc_name}", esc_value)
        else: self.esc_Rin = 0
        self.propeller = propeller
        if propeller:
            for prop_name, prop_value in vars(propeller).items():
                setattr(self, f"propeller_{prop_name}", prop_value)

        self.R_tot = self.motor_Rin + self.esc_Rin + self.battery_Rin
        self.AnalysisMethod = AnalysisMethod
        self.vcruise = operatingPoint.velocity
        expected_args_ecalc =  ['modelweight',
                                'batteryType',
                                'batterySeriesCells',
                                'batteryParallelCells',
                                'escType',
                                'motorManuf',
                                'motorType',
                                'propType',
                                ]
        args_for_ecalc = {k: v for k, v in kwargs.items() if k in expected_args_ecalc}
        if self.AnalysisMethod.lower() == 'ecalc':
            self.results = self.run_ecalc(
                modelweight=args_for_ecalc['modelweight'],
                wingspan=airplane.b_ref*1000,
                wingarea=airplane.s_ref*100,
                elevation=operatingPoint.atmosphere.altitude,
                vcruise=self.vcruise,
                batteryType=args_for_ecalc['batteryType'],
                batterySeriesCells=args_for_ecalc['batterySeriesCells'],
                batteryParallelCells=args_for_ecalc['batteryParallelCells'],
                escType=args_for_ecalc['escType'],
                motorManuf= args_for_ecalc['motorManuf'],
                motorType=args_for_ecalc['motorType'],
                propType=args_for_ecalc['propType'],
            )

    def getMaxRPM(self):
        rpm_100 = symbols('rpm_100', positive=True)
        T1 = sqrt(self.propeller_NB - 1) * self.propeller_Pc * 4.019e-15 * self.propeller_diameter**4 * self.propeller_pitch * (rpm_100)**3
        T2 = 2 * math.pi * rpm_100 * self.motor_kt * ((self.battery_volt - rpm_100 / self.motor_kv) / self.R_tot - self.motor_i0) / 60
        equation = T1 - T2
        solutions = solve(equation, rpm_100)
        # Assuming we are looking for a real, positive solution, if multiple exist
        for sol in solutions:
            if sol.is_real and sol > 0:
                return float(sol)
        return None # Or raise an error if no suitable solution is found

    def T_static(self, throttle=1, ecalc=1):
        """
        Calculates static thrust based on throttle.
        """
        if ecalc>0:
            return self._Tstaitc_ecalc()
        else:
            if not (0 <= throttle <= 1):
                raise ValueError("Throttle must be between 0 and 1.")

            RPM_100 = self.getMaxRPM()
            if RPM_100 is None:
                return None

            # Ensure propeller_NB - 1 is not negative for sqrt
            if (self.propeller_NB - 1) < 0:
                return 0

            t_static = (self.propeller_eff * np.sqrt(self.propeller_NB - 1) * self.propeller_Tc *
                        2.691e-9 * self.propeller_diameter ** 3 * self.propeller_pitch *
                        (RPM_100 * throttle) ** 2)
            return t_static

    def T_dynamic(self, v=None, throttle=1,ecalc=1):
        """
        Calculates dynamic thrust based on velocity and throttle.
        Uses the provided formula.
        """
        if ecalc>0:
            return self._Tdynamic_ecalc()
        else:
            if not v:
                v = self.vcruise
            RPM_100 = self.getMaxRPM()
            if RPM_100 is None:
                return None

            if not (0 <= throttle <= 1):
                raise ValueError("Throttle must be between 0 and 1.")

            rpm = RPM_100 * throttle
            t_static = self.T_static(throttle, ecalc=0)
            if t_static is None:
                return None

            vp = self.propeller_pitch * 0.0254 * rpm / 60

            if abs(vp) < 1e-9:  # Check if vp is practically zero
                return t_static if abs(
                    v) < 1e-9 else 0.0  # If v is also zero, it's static. Otherwise, no thrust if no prop speed.

            term2_val = (31 * t_static) / (130 * vp ** 2) * v ** 2
            term3_val = 0.4543 * v * t_static / vp

            t_dynamic = t_static - term2_val - term3_val
            return t_dynamic

    def throttle(self, v=None, t_dynamic_target=None, tolerance=0.01,
                     max_iterations=200):
        """
        Finds the throttle setting required to achieve a target dynamic thrust at a given velocity.
        Uses a numerical bisection method (binary search) to find the throttle.

        Args:
            v (float): Current velocity in m/s.
            t_dynamic_target (float): The desired dynamic thrust in Newtons.
            tolerance (float): The acceptable difference between calculated and target dynamic thrust.
            max_iterations (int): Maximum number of iterations for the search.

        Returns:
            float: The throttle setting (0-1), or None if a solution cannot be found within tolerance.
        """
        if v == None:
            v = self.vcruise
        if t_dynamic_target == None:
            self._Tdynamic_ecalc()
        low_throttle = 0.0
        high_throttle = 1.0

        # Check boundary conditions
        min_possible_thrust = self.T_dynamic(v, throttle=0.0, ecalc=0)
        max_possible_thrust = self.T_dynamic(v, throttle=1.0, ecalc=0)

        # Ensure target is within the possible range for the given velocity
        if max_possible_thrust is None or min_possible_thrust is None:
            # Handle cases where T_dynamic returns None (e.g., invalid prop_NB)
            raise Warning("Max thrust or Min thrust is None")

        if t_dynamic_target < min_possible_thrust - tolerance:
            # Target thrust is too low, perhaps negative and not achievable
            # Or perhaps just marginally below what's possible at 0 throttle
            return 0.0

        if t_dynamic_target > max_possible_thrust + tolerance:
            # Target thrust is higher than max possible at full throttle
            raise Warning(F"Target Dynamic Thrust {t_dynamic_target} > max possible thrust {max_possible_thrust}")

        if abs(t_dynamic_target - min_possible_thrust) < tolerance:
            return 0.0
        if abs(t_dynamic_target - max_possible_thrust) < tolerance:
            return 1.0

        for i in range(max_iterations):
            mid_throttle = (low_throttle + high_throttle) / 2
            calculated_t_dynamic = self.T_dynamic(v, throttle=mid_throttle, ecalc=0)

            if calculated_t_dynamic is None:
                raise Warning("Calculated T dynamic is None")


            if abs(calculated_t_dynamic - t_dynamic_target) < tolerance:
                return mid_throttle

            if calculated_t_dynamic < t_dynamic_target:
                low_throttle = mid_throttle
            else:
                high_throttle = mid_throttle

        final_throttle = (low_throttle + high_throttle) / 2
        if abs(self.T_dynamic(v, final_throttle, ecalc=0) - t_dynamic_target) < tolerance:
            return final_throttle
        else:
            return Warning(f"Couldn't Converge T_dynamic given {t_dynamic_target}, calculated T_dyamic = {self.T_dynamic(v, final_throttle, ecalc=0)}")

    def Pm(self, throttle=1):
        if self.AnalysisMethod == 'ecalc':
            return self.results['Motor_mechPower_W']
        else:
            RPM_100 = self.getMaxRPM()
            if RPM_100 is None:
                return None
            pm = sqrt(self.propeller_NB - 1) * self.propeller_Pc * 4.019e-15 * self.propeller_diameter**4 * self.propeller_pitch * (RPM_100 * throttle)**3
            return pm

    def Torque(self, throttle=1):
        if self.AnalysisMethod == 'ecalc':
            throttle = self.results['Motor_Total_Torque']
        RPM_100 = self.getMaxRPM()
        if RPM_100 is None:
            return None
        pm = self.Pm(throttle)
        if pm is None:
            return None
        if RPM_100 * throttle == 0:
            return 0
        torque = pm * 60 / (2 * math.pi * RPM_100 * throttle)
        return torque

    def CurrentDraw(self, throttle=1):
        if self.AnalysisMethod == 'ecalc':
            throttle = self._throttle_ecalc()
        torque = self.Torque(throttle)
        if torque is None:
            return None
        current = self.motor_i0 + torque / self.motor_kt
        return current

    # This section for automating calculations using ecalc
    def run_ecalc(self,
                  modelweight,
                  wingspan,
                  wingarea,
                  elevation,
                  vcruise,
                  batteryType,
                  batterySeriesCells,
                  batteryParallelCells,
                  escType,
                  motorManuf,
                  motorType,
                  propType,
                  ):
        return ecalc(
            modelweight=modelweight,
            wingspan=wingspan,
            wingarea=wingarea,
            elevation=elevation,
            batteryType=batteryType,
            batterySeriesCells=batterySeriesCells,
            batteryParallelCells=batteryParallelCells,
            escType=escType,
            motorManuf=motorManuf,
            motorType=motorType,
            propType=propType,
            vCruise=vcruise,
            propDiameter=self.propeller_diameter,
            propPitch=self.propeller_pitch,
            propNumberOfBlades=self.propeller_NB,
        )

    def T_W(self):
        return self.results['TotalDrive_ThrustWeight_ratio']

    def _Tstaitc_ecalc(self):
        return self.results['Propeller_StaticThrust_g']/1000 * 9.8
    def endurance_ecalc(self):
        return self.results['Battery_MixedFlightTime_min']

    def _Tdynamic_ecalc(self):
        return self.results['Propeller_availThrust_g_kmh'] / 1000 * 9.81

    def throttle_ecalc(self):
        return self.results['Propeller_Revolutions_rpm']/self.getMaxRPM()


if __name__ == '__main__':
    import aerosandbox as asb
    import aerosandbox.numpy as np
    import pandas as pd
    import re

    batteries_data = pd.read_pickle(r'resources/ecalcData/pkl_data/batteries.pkl')
    esc_data = pd.read_pickle(r'resources/ecalcData/pkl_data/esc.pkl')
    motors_data = pd.read_pickle(r'resources/ecalcData/pkl_data/motors.pkl')

    Battery_row = batteries_data[batteries_data['text'] == 'LiPo 4200mAh - 80/120C']
    Battery1 = Battery(n_cells=6, p_cells=1, voltpercell=float(Battery_row['cell_volt'].iloc[0]), cell_Rin=float(Battery_row['Rin'].iloc[0]))

    Motor_row = motors_data[motors_data['type'] == 'MN705-S KV260 (260)']
    Motor1 = Motor(kv=float(Motor_row['Kv'].iloc[0]), i0=float(Motor_row['Io'].iloc[0]), R_in=float(Motor_row['Rin'].iloc[0]))

    Esc_row = esc_data[esc_data['text'] == 'max 50A']
    Esc1 = ESC(Rin=float(Esc_row['Rin'].iloc[0]))

    prop = Propeller(pitch=8,diameter=15,NB=2)


    # Trainer Definition
    wing_airfoil = asb.Airfoil('clarky')
    tail_airfoil = asb.Airfoil('naca0010')

    wing = asb.Wing(
        name='main wing',
        xyz_le=[0, 0, 0],
        symmetric=True,
        xsecs=[
            asb.WingXSec(  # Root
                xyz_le=[0, 0, 0],
                chord=0.24988,
                twist=0,  # degrees
                airfoil=wing_airfoil,
            ),
            asb.WingXSec(  # Mid
                xyz_le=[0, 1.4 / 2, 0],
                chord=0.24988,
                twist=0,  # degrees
                airfoil=wing_airfoil,
            )]
    )

    htail = asb.Wing(
        name="Horizontal Stabilizer",
        symmetric=True,
        xsecs=[
            asb.WingXSec(  # root
                xyz_le=[0, 0, 0],
                chord=0.175,
                twist=-2.5,
                airfoil=tail_airfoil,
                control_surfaces=[asb.ControlSurface(
                    name="Elevator",
                    symmetric=True,
                    trailing_edge=True,
                    hinge_point=0.75,
                    deflection=10,
                )],

            ),
            asb.WingXSec(  # tip
                xyz_le=[(170.5 - 79.61) / 1000, 0.2, 0],
                chord=79.61 / 1000,
                twist=-2.5,
                airfoil=tail_airfoil
            )
        ]
    )

    vtail = asb.Wing(
        name="Vertical Stabilizer",
        symmetric=False,
        xsecs=[
            asb.WingXSec(
                xyz_le=[0, 0, 0],
                chord=0.175,
                twist=0,
                airfoil=tail_airfoil,
                control_surface_is_symmetric=True,  # Rudder
                control_surface_deflection=0,
            ),
            asb.WingXSec(
                xyz_le=[(170.5 - 89.72) / 1000, 0, 0.24964],
                chord=89.72 / 1000,
                twist=0,
                airfoil=tail_airfoil
            )
        ]
    )
    fuselage = asb.Fuselage(
        name="Fuselage",
        xsecs=[
            asb.FuselageXSec(
                xyz_c=[-0.17, 0, -0.04],
                height=0.08,
                width=0.11,
                shape=10000
            ),
            asb.FuselageXSec(
                xyz_c=[0.46 - 0.17, 0, -0.04],
                height=0.08,
                width=0.11,
                shape=10000
            ),
            asb.FuselageXSec(
                xyz_c=[0.9 - 0.17, 0, -(80 - (899.85 - 460) * np.sind(4.3)) / 2 / 1000],
                height=(80 - (899.85 - 460) * np.sind(4.3)) / 1000,
                width=0.045,
                shape=10000
            )

        ]
    )
    # Propulsion

    # Complete Airplane
    trainer = asb.Airplane(
        name='trainer',
        xyz_ref=[0.073, 0, -0.05],
        s_ref=wing.area(),
        b_ref=wing.span(),
        wings=[
            wing,
            htail.translate([612.34 / 1000, 0, -0.025]),
            vtail.translate([612.34 / 1000, 0, -0.025])
        ],
        fuselages=[fuselage]
    )
    opcon = OperatingPoint(velocity=20)

    expected_args_ecalc = {'modelweight'                : 2500,
                           'batteryType'                : "LiPo 4200mAh - 80/120C",
                            'batterySeriesCells'        :6,
                            'batteryParallelCells'      :1,
                            'escType'                   :"max 50A",
                            'motorManuf'                :"T-Motor ",
                            'motorType'                 :"MN705-S KV260",
                           'propType'                   :"APC Electric E",
                           }
    propulsion = Propulsion(battery=Battery1,motor=Motor1,esc=Esc1,airplane=trainer, operatingPoint=opcon, propeller=prop,**expected_args_ecalc)
    t_static = propulsion.T_static()
    T_w = propulsion.T_W()
    endurance = propulsion.endurance_ecalc()
    t_dynamic = propulsion.T_dynamic()
    throttle = propulsion.throttle_ecalc()

    print(f"Static Thrust is {t_static:.3f} N")
    print(f"Dynamic Thrust is {t_dynamic:.3f} N")
    print(f"T/W is {T_w:.3f}")
    print(f"throttle is {throttle*100:.3f} %")
    print(f"endurance is {endurance:.3f} Minute")
    print(f"max rpm is {propulsion.getMaxRPM():.3f}")