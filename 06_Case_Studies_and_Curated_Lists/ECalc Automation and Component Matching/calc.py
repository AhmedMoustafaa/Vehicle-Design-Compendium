from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
from time import sleep, time
import pandas as pd
import re
import glob
import shutil

from fuzzywuzzy import fuzz

from selenium.webdriver.remote.webelement import WebElement


def inField(field: WebElement, value):
    if isinstance(value, (float or int)):
        value = round(value, 3)
    field.send_keys(Keys.CONTROL + "a")
    sleep(0.2)
    field.send_keys(Keys.DELETE)
    sleep(0.2)
    field.send_keys(str(value))


def select_closest_option(select_element: WebElement, desired_text: str, threshold: int = 70):
    select = Select(select_element)

    options_texts = [option.text for option in select.options]

    best_match_text = None
    best_score = -1

    for option_text in options_texts:
        score = fuzz.ratio(desired_text.lower(), option_text.lower())

        if score > best_score:
            best_score = score
            best_match_text = option_text

    if best_match_text and best_score >= threshold:
        try:
            select.select_by_visible_text(best_match_text)
            print(f"Selected closest match for '{desired_text}': '{best_match_text}' (Score: {best_score})")
            return True
        except Exception as e:
            print(f"Error selecting '{best_match_text}' by visible text: {e}")
            return False
    else:
        print(f"No close match found for '{desired_text}' (best score: {best_score}) with threshold {threshold}.")
        raise ValueError(
            f"No suitable option found for '{desired_text}' in dropdown. Best match: '{best_match_text}' (Score: {best_score})")


def ecalc(
        modelweight,
        wingspan, wingarea,
        elevation,

        batteryType, batterySeriesCells, batteryParallelCells,
        escType,
        motorManuf, motorType,
        propType, propDiameter, propPitch, propNumberOfBlades, vCruise=0,
        project_name="ecalcproject"
):
    def parse_ecalc_csv(file_path, max_rpm, torque):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        data = {}

        def get_section_lines(start_marker, end_marker, full_lines):
            section_lines = []
            in_section = False
            for line in full_lines:
                if start_marker in line:
                    in_section = True
                    section_lines.append(line)
                    continue

                if in_section:
                    if end_marker in line:
                        break
                    section_lines.append(line)
            return section_lines

        def get_value_from_line(lines_list, label_start, column_index, is_float=True, default_val=None):
            for line in lines_list:
                if line.strip().startswith(label_start):
                    parts = line.strip().split(';')
                    if len(parts) > column_index:
                        value_str = parts[column_index].strip()
                        value_str = re.sub(r'[a-zA-Z%°/]+$', '', value_str).strip()
                        value_str = value_str.replace(',', '')

                        if is_float and value_str not in ('-', ''):
                            try:
                                return float(value_str)
                            except ValueError:
                                return default_val
                        return value_str if value_str not in ('-', '') else default_val
            return default_val

        # --- Project Name ---
        data['Project_Name'] = get_value_from_line(lines, "Project Name;;", column_index=2, is_float=False)

        # --- Battery Section ---
        battery_lines = get_section_lines("Battery;;", "Controller;;", lines)
        data['Battery_Type'] = get_value_from_line(battery_lines, "Battery;;", column_index=2, is_float=False)
        data['Battery_Configuration'] = get_value_from_line(battery_lines, "Configuration:;;", column_index=2,
                                                            is_float=False)
        data['Battery_Load_C'] = get_value_from_line(battery_lines, "Load:;C;", column_index=2)
        data['Battery_Voltage_V'] = get_value_from_line(battery_lines, "Voltage:;V;", column_index=2)
        data['Battery_RatedVoltage_V'] = get_value_from_line(battery_lines, "Rated Voltage:;V;", column_index=2)
        data['Battery_Energy_Wh'] = get_value_from_line(battery_lines, "Energy:;Wh;", column_index=2)
        data['Battery_TotalCapacity_mAh'] = get_value_from_line(battery_lines, "Total Capacity:;mAh;", column_index=2)
        data['Battery_max_discharge_pct'] = get_value_from_line(battery_lines, "max. discharge:;;", column_index=2,
                                                                is_float=False)
        data['Battery_UsedCapacity_mAh'] = get_value_from_line(battery_lines, "Used Capacity:;mAh;", column_index=2)
        data['Battery_min_FlightTime_min'] = get_value_from_line(battery_lines, "min. Flight Time:;min;",
                                                                 column_index=2)
        data['Battery_MixedFlightTime_min'] = get_value_from_line(battery_lines, "Mixed Flight Time:;min;",
                                                                  column_index=2)
        data['Battery_Weight_g'] = get_value_from_line(battery_lines, "Weight:;g;", column_index=2)

        # --- Controller Section ---
        controller_lines = get_section_lines("Controller;;", "Motor @ Maximum;;", lines)
        data['Controller_Type'] = get_value_from_line(controller_lines, "Controller;;", column_index=2, is_float=False)
        data['Controller_Current_A_cont'] = get_value_from_line(controller_lines, "Current:;A cont.;", column_index=2)
        data['Controller_Current_A_max'] = get_value_from_line(controller_lines, ";A max;", column_index=2)
        data['Controller_Weight_g'] = get_value_from_line(controller_lines, "Weight:;g;", column_index=2)
        data['Controller_BatteryExtensionWire_Type'] = get_value_from_line(controller_lines,
                                                                           "Battery extension Wire:;;", column_index=2,
                                                                           is_float=False)

        bat_wire_length_val = None
        start_search_bat_wire = False
        for line in controller_lines:
            if "Battery extension Wire:;;" in line:
                start_search_bat_wire = True
            if start_search_bat_wire and "Length:;mm;" in line:
                bat_wire_length_val = get_value_from_line([line], "Length:;mm;", column_index=2)
                start_search_bat_wire = False  # Reset for the next one
                break
        data['Controller_BatWire_Length_mm'] = bat_wire_length_val if bat_wire_length_val is not None else 0.0

        data['Controller_MotorExtensionWire_Type'] = get_value_from_line(controller_lines, "Motor extension Wire:;;",
                                                                         column_index=2, is_float=False)

        mot_wire_length_val = None
        start_search_mot_wire = False
        for line in controller_lines:
            if "Motor extension Wire:;;" in line:
                start_search_mot_wire = True
            if start_search_mot_wire and "Length:;mm;" in line:
                mot_wire_length_val = get_value_from_line([line], "Length:;mm;", column_index=2)
                break
        data['Controller_MotWire_Length_mm'] = mot_wire_length_val if mot_wire_length_val is not None else 0.0
        # --- Motor @ Maximum Section ---
        motor_lines = get_section_lines("Motor @ Maximum;;", "Propeller", lines)
        data['Motor_Type'] = get_value_from_line(motor_lines, "Motor @ Maximum;;", column_index=2, is_float=False)
        data['Motor_GearRatio'] = get_value_from_line(motor_lines, "Gear Ratio:;: 1;", column_index=2)
        data['Motor_Weight_g'] = get_value_from_line(motor_lines, "Weight:;g;", column_index=2)
        data['Motor_Current_A'] = get_value_from_line(motor_lines, "Current:;A;", column_index=2)
        data['Motor_Voltage_V'] = get_value_from_line(motor_lines, "Voltage:;V;", column_index=2)
        data['Motor_Revolutions_rpm'] = get_value_from_line(motor_lines, "Revolutions*:", column_index=2)
        data['Motor_electricPower_W'] = get_value_from_line(motor_lines, "electric Power:;W;", column_index=2)
        data['Motor_mechPower_W'] = get_value_from_line(motor_lines, "mech. Power:;W;", column_index=2)
        data['Motor_Efficiency_pct'] = get_value_from_line(motor_lines, "Efficiency:;%;", column_index=2)
        data['Motor_estTemperature_C'] = get_value_from_line(motor_lines, "est. Temperature:;°C;", column_index=2)
        data['Motor_Total_Torque'] = torque

        # --- Propeller Section ---
        propeller_lines = get_section_lines("Propeller;;", "Total Drive;;", lines)
        data['Propeller_Type'] = get_value_from_line(propeller_lines, "Propeller;;", column_index=2, is_float=False)
        data['Propeller_NumBlades'] = get_value_from_line(propeller_lines, "# Blades:;;", column_index=2)
        data['Propeller_StaticThrust_g'] = get_value_from_line(propeller_lines, "Static Thrust:;g;", column_index=2)
        data['Propeller_Revolutions_rpm'] = get_value_from_line(propeller_lines, "Revolutions*:", column_index=2)
        data['Propeller_StallThrust_g'] = get_value_from_line(propeller_lines, "Stall Thrust:;g;", column_index=2)
        data['Propeller_Max_rpm'] = max_rpm

        dynamic_thrust_long = get_value_from_line(propeller_lines,"avail.Thrust @ Flight Speed:;g@km/h;",column_index=2,is_float=False)
        if dynamic_thrust_long:
            dynamic_thrust_extracted = float(dynamic_thrust_long.split(" @ ")[0])
            data['Propeller_availThrust_g_kmh'] = dynamic_thrust_extracted
        else: #dynamic_thrust is None
            data['Propeller_availThrust_g_kmh'] = dynamic_thrust_long

        data['Propeller_PitchSpeed_kmh'] = get_value_from_line(propeller_lines, "Pitch Speed:;km/h;", column_index=2)
        data['Propeller_specificThrust_gW'] = get_value_from_line(propeller_lines, "specific Thrust:;g/W;",
                                                                  column_index=2)

        # --- Total Drive Section ---
        total_drive_lines = get_section_lines("Total Drive;;", "Airplane", lines)
        data['TotalDrive_Weight_g'] = get_value_from_line(total_drive_lines, "Drive Weight:;g;", column_index=2)
        data['TotalDrive_PowerWeight_W_kg'] = get_value_from_line(total_drive_lines, "Power-Weight:;W/kg;",
                                                                  column_index=2)
        data['TotalDrive_ThrustWeight_ratio'] = get_value_from_line(total_drive_lines, "Thrust-Weight:;: 1;",
                                                                    column_index=2)
        data['TotalDrive_Current_max_A'] = get_value_from_line(total_drive_lines, "Current @ max:;A;", column_index=2)
        data['TotalDrive_Pin_max_W'] = get_value_from_line(total_drive_lines, "P(in) @ max:;W;", column_index=2)
        data['TotalDrive_Pout_max_W'] = get_value_from_line(total_drive_lines, "P(out) @ max:;W;", column_index=2)
        data['TotalDrive_Efficiency_max_pct'] = get_value_from_line(total_drive_lines, "Efficiency @ max:;%;",
                                                                    column_index=2)


        # --- Airplane Section ---
        airplane_lines = get_section_lines("Airplane", "Remarks:;;", lines)
        data['Airplane_NumMotors'] = get_value_from_line(airplane_lines, "# of Motors:;;", column_index=2)
        data['Airplane_AllUpWeight_g'] = get_value_from_line(airplane_lines, "All-up Weight:;g;", column_index=2)
        data['Airplane_WingArea'] = get_value_from_line(airplane_lines, "Wing Area:;;", column_index=2, is_float=False)
        data['Airplane_WingLoad_g_dm2'] = get_value_from_line(airplane_lines, "Wing Load:;g/dm²;", column_index=2)
        data['Airplane_CubicWingLoad'] = get_value_from_line(airplane_lines, "Cubic Wing Load:;;", column_index=2,
                                                             is_float=False)
        data['Airplane_estStallSpeed_kmh'] = get_value_from_line(airplane_lines, "est. Stall Speed:;km/h;",
                                                                 column_index=2)
        data['Airplane_estSpeed_level_kmh'] = get_value_from_line(airplane_lines, "est. Speed (level):;km/h;",
                                                                  column_index=2)
        data['Airplane_estSpeed_vertical_kmh'] = get_value_from_line(airplane_lines, "est. Speed (vertical):;km/h;",
                                                                     column_index=2)
        data['Airplane_estRateOfClimb_ms'] = get_value_from_line(airplane_lines, "est. rate of climb:;m/s;",
                                                                 column_index=2)

        # --- Remarks ---
        data['Remarks'] = get_value_from_line(lines, "Remarks:;;", column_index=2, is_float=False)

        return pd.Series(data)

    tor_process = None
    driver = None
    download_dir = os.path.join(os.getcwd(), "ecalcCSVs")

    try:
        if os.path.exists(download_dir):
            shutil.rmtree(download_dir)
        os.makedirs(download_dir)

        tor_process = os.popen(r'D:\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
        print("Starting Tor process...")
        sleep(15)

        PROXY = "socks5://localhost:9050"
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.always_open_pdf_externally": True
        }
        options.add_experimental_option("prefs", prefs)

        service = Service(r'resources/drivers/chromedriver.exe')
        driver = webdriver.Chrome(options=options, service=service)
        wait = WebDriverWait(driver, 30)

        driver.get("https://www.ecalc.ch/motorcalc.php")

        modal_confirm_ok = wait.until(EC.element_to_be_clickable((By.ID, "modalConfirmOk")))
        modal_confirm_ok.click()
        print("Clicked modal confirm.")

        sleep(1)
        js_script = """
        function manipulateMType() {
            const manufacturerSelect = document.getElementById("inMManufacturer");
            const mTypeSelect = document.getElementById("inMType");

            if (manufacturerSelect && mTypeSelect) {
                const selectedManufacturer = manufacturerSelect.value;
                Array.from(mTypeSelect.options).forEach((option, index) => {
                    if (index > 0) {
                        option.removeAttribute("disabled");
                        const optionText = option.textContent.split(' ').slice(0, -1).join(' ');
                        option.value = `${selectedManufacturer}|${optionText}`;
                    }
                });
            }
        }

        function manipulateSelectElements() {
            const selectElementIds = ["inBCell", "inEType"];
            selectElementIds.forEach(id => {
                const selectElement = document.getElementById(id);
                if (selectElement) {
                    if (id === "inEType") {
                        Array.from(selectElement.options).forEach((option, index) => {
                            if (index > 0) {
                                option.removeAttribute("disabled");
                                option.value = index;
                            }
                        });
                    } else {
                        Array.from(selectElement.options).forEach(option => {
                            option.removeAttribute("disabled");
                            option.value = option.textContent;
                        });
                    }
                }
            });

            const manufacturerSelect = document.getElementById("inMManufacturer");
            if (manufacturerSelect) {
                manufacturerSelect.addEventListener("change", manipulateMType);
            }
            manipulateMType();
        }
        manipulateSelectElements();
        """
        js_script2 = """
        const downloadButton = document.getElementById("DownloadCSV");
        if (downloadButton) {
            downloadButton.removeAttribute("disabled");
        }
        const addButton = document.getElementById("AddCSV");
        if (addButton) {
            addButton.removeAttribute("disabled");
        }
        const clearButton = document.getElementById("ClearCSV");
        if (clearButton) {
            clearButton.removeAttribute("disabled");
        }
        """
        driver.execute_script(js_script)
        print("Executed JS for dropdown and button manipulation.")
        sleep(1.5)

        input_values_map = {
            'modelweight': modelweight,
            'wingspan': wingspan,
            'wingarea': wingarea,
            'elevation': elevation,
            'batteryType': batteryType,
            'batterySeriesCells': batterySeriesCells,
            'batteryParallelCells': batteryParallelCells,
            'escType': escType,
            'motorManuf': motorManuf,
            'motorType': motorType,
            'propType': propType,
            'propDiameter': propDiameter,
            'propPitch': propPitch,
            'propNumberOfBlades': propNumberOfBlades,
            'vCruise': vCruise*3.6,  #m/s to km/h
        }

        ELEMENT_IDS = {
            'modelweight': "inGWeight",
            'wingspan': "inGWingSpan",
            'wingarea': "inGWingArea",
            'elevation': "inGElevation",
            'batteryType': "inBCell",
            'batterySeriesCells': "inBS",
            'batteryParallelCells': "inBP",
            'escType': "inEType",
            'motorManuf': "inMManufacturer",
            'motorType': "inMType",
            'propType': "inPType",
            'propDiameter': "inPDiameter",
            'propPitch': "inPPitch",
            'propNumberOfBlades': "inPBlades",
            'vCruise':"inPSpeed"
        }

        param_groups = {
            'General': ['modelweight', 'wingspan', 'wingarea', 'elevation'],
            'Battery': ['batteryType', 'batterySeriesCells', 'batteryParallelCells'],
            'ESC': ['escType'],
            'Motor': ['motorManuf', 'motorType'],
            'Propeller': ['propType', 'propDiameter', 'propPitch', 'propNumberOfBlades','vCruise']
        }

        for group_name, param_names_list in param_groups.items():
            print(f"\n--- Setting {group_name} Fields ---")
            for param_name in param_names_list:
                try:
                    field_id = ELEMENT_IDS[param_name]
                    field_element = wait.until(EC.presence_of_element_located((By.ID, field_id)))
                    value_to_set = input_values_map[param_name]

                    if field_id in ["inBCell", "inEType", "inMManufacturer", "inMType", "inPType"]:
                        try:
                            select_closest_option(field_element, str(value_to_set),
                                                  threshold=80)
                        except ValueError as ve:
                            print(f"Warning: {ve} for {param_name} ({field_id}). Attempting exact match as fallback.")
                            select = Select(field_element)
                            try:
                                select.select_by_visible_text(str(value_to_set))
                                field_id.send_keys(Keys.ENTER)
                                print(
                                    f"Set {param_name} ({field_id}) to '{value_to_set}' (by exact visible text fallback)")
                            except Exception as e_exact:
                                print(
                                    f"Error: Could not set {param_name} ({field_id}) to '{value_to_set}' (Exact match fallback failed too): {e_exact}")
                                raise
                    else:
                        inField(field_element, value_to_set)
                        print(f"Set {param_name} ({field_id}) to '{value_to_set}'")
                    sleep(0.5)

                except Exception as e:
                    print(f"Failed to set {param_name} (ID: {field_id}): {e}")
        driver.execute_script(js_script2)
        calculatebtn = wait.until(EC.element_to_be_clickable((By.NAME, 'btnCalculate')))
        Addtobtn = wait.until(EC.element_to_be_clickable((By.ID, 'AddCSV')))
        Downloadbtn = wait.until(EC.element_to_be_clickable((By.ID, 'DownloadCSV')))
        clearbtn = wait.until(EC.element_to_be_clickable((By.ID, 'ClearCSV')))

        calculatebtn.click()
        print("Clicked 'Calculate' button.")

        try:
            confirm_calculation_modal = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary")))
            confirm_calculation_modal.click()
            print("Clicked calculation confirmation modal.")
            sleep(1)
        except Exception as e:
            print(f"No calculation confirmation modal found or error clicking it: {e}")
        rpm_span_element = wait.until(EC.presence_of_element_located((By.ID, "outOptRpm")))
        float_span_element = wait.until(EC.presence_of_element_located((By.ID, "outTotTorque")))
        print(rpm_span_element)
        rpm_max = float(rpm_span_element.text)
        torque = float(float_span_element.text)

        driver.execute_script(js_script2)
        driver.execute_script("arguments[0].scrollIntoView(true);", Addtobtn)
        sleep(1)
        Addtobtn.send_keys(Keys.RETURN)
        print("Clicked 'Add to >>' button.")
        try:
            alert = wait.until(EC.alert_is_present())

            alert_text = alert.text
            print(f"Alert text: {alert_text}")

            alert.send_keys(project_name)
            print(f"Inputted project name: '{project_name}'")

            alert.accept()
            print("Accepted project name alert.")
            sleep(1)

        except Exception as e:
            print(f"Error handling project name alert: {e}")
            raise
        sleep(2)
        driver.execute_script("arguments[0].scrollIntoView(true);", Downloadbtn)
        Downloadbtn.send_keys(Keys.RETURN)
        print("Clicked 'Download .csv' button.")

        downloaded_file_path = None
        timeout = 30
        check_interval = 1
        start_time = time()

        while time() - start_time < timeout:
            all_csv_files = glob.glob(os.path.join(download_dir, '*.csv'))
            complete_csv_files = [f for f in all_csv_files if not f.endswith('.crdownload')]

            if complete_csv_files:
                complete_csv_files.sort(key=os.path.getmtime, reverse=True)
                downloaded_file_path = complete_csv_files[0]
                print(f"Detected downloaded file: {downloaded_file_path}")
                break
            sleep(check_interval)

        if not downloaded_file_path:
            raise Exception("CSV file did not download within the expected time.")

        df_parsed = parse_ecalc_csv(downloaded_file_path, rpm_max, torque)
        print("\nSuccessfully parsed CSV into DataFrame:")
        print("--------------------------------------------------------------------------------------------------------------------")
        #print(df_parsed.head())

        return df_parsed

    except Exception as e:
        print(f"An error occurred during ecalc execution: {e}")
        if driver:
            driver.save_screenshot(os.path.join(os.getcwd(), "error_screenshot.png"))
        return None

    finally:
        if driver:
            pass
        if tor_process:
            print("Please manually close Tor Browser or its process if it's still running.")


if __name__ == '__main__':
    results = ecalc(
        modelweight=3000,
        wingspan=2540,
        wingarea=70,
        elevation=20,
        batteryType="LiPo 4200mAh - 80/120C",
        batterySeriesCells=6,
        batteryParallelCells=1,
        escType="max 50A",
        motorManuf="T-Motor ",
        motorType="MN705-S KV260",
        propType="APC Electric E",
        propDiameter=15,
        propPitch=8,
        propNumberOfBlades=2,
        vCruise=18,
        project_name="TestProject"
    )
    if results is not None:
        print("\nDataFrame from eCalc:")
        print(results)