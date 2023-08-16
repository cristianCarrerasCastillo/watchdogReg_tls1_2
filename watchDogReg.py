import winreg
import os
import datetime
import argparse

parser = argparse.ArgumentParser(description="WatchDogReg")
parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
parser.add_argument("-d", "--debug", action="store_true", required=False, help="Debug mode")
args = parser.parse_args()

debug = False
def check_reg(reg, value):
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg) as key:
            val = winreg.QueryValueEx(key, value)[0]
            if val != 1:
                print_states(debug, f"Registry {reg} exists but is not set to 1.")
                winreg.CloseKey(key)
                writing_log(f"Registry {reg} exists but is not set to 1.")
                return False
            winreg.CloseKey(key)
            return True
    except FileNotFoundError:
        print_states(debug, f"Registry {reg}\{value} does not exist.")
        winreg.CloseKey(key)
        writing_log(f"Registry {reg}\{value} does not exist.")
        return False

def create_reg(reg, value):
    try:
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg) as key:
            winreg.SetValueEx(key, value, 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            data = f"Registry {reg}\{value} created."
            writing_log(data)
            print_states(debug, data)
    except PermissionError:
        writing_log("PermissionError: Please run this script as administrator.")
        print_states(debug, "PermissionError: Please run this script as administrator.")
    except Exception as e:
        writing_log(f"Error: {e}")
        print_states(debug, f"Error: {e}")

def check_log_path(path_log):
    try:
        if not os.path.exists(path_log):
            print_states(debug, "Creating path...")
            os.makedirs(path_log)
            print_states(debug, "Path created.")
        if not os.path.exists(path_log + r"\log.txt"):
            print_states(debug, "Creating log...")
            with open(path_log + r"\log.txt", "w") as file:
                file.write("Log Watchdog Created. this file is generated for WatchDogReg\n")
                file.write("Developed by: Cristian Carreras\n")
                file.write("---------------------------------------------\n")
                file.close()
            print_states(debug, "Log created.")
    except Exception as e:
        print_states(debug, "Error: ", e)

def writing_log(data):
    path_log = r"C:\watchdogReg"
    check_log_path(path_log)
    print_states(debug, "Writing log...")
    with open(path_log + r"\log.txt", "a") as file:
        file.write(f"{datetime.datetime.now()}: {data}\n")
        file.close()
    print_states(debug, "Log written.")

def print_states(debug, data):
    if debug:
        print(data)

def main():
    value_1 = "SystemDefaultTlsVersions"
    value_2 = "SchUseStrongCrypto"
    validator = False

    reg_1 = r"SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v2.0.50727"
    reg_2= r"SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v4.0.30319"

    reg_3 = r"SOFTWARE\Microsoft\.NETFramework\v2.0.50727"
    reg_4= r"SOFTWARE\Microsoft\.NETFramework\v4.0.30319"

    for reg in [reg_1, reg_2, reg_3, reg_4]:
        if check_reg(reg, value_1) == False:
            print_states(debug, "Creating registry...")
            writing_log("Creating registry...")
            create_reg(reg, value_1)
            create_reg(reg, value_2)
            validator =  True

    if validator:
        print_states(debug, "Restarting...")
        writing_log("Restarting the computer...")
        os.system("shutdown /r /t 1800")

if __name__ == "__main__":
    if args.debug:
        print("Debug mode activated")
        print("Checking registry...")
        writing_log("Debug mode activated")
        writing_log("Checking registry...")
        debug = True
    main()
