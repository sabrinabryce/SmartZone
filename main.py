# main.py
import utime
import web
import log
import test
from wifi import *
from control import *
from actuators import ir_emitter


# -----------------------------
# SYSTEM RUN FUNCTION
# -----------------------------
def run_system(logging=True, debug=False):

    # Network setup
    ap = start_ap()
    server = start_server()

    ir_emitter(True)

    print("SmartZone running")

    while True:

        state = update_system()

        # Only log if logging mode enabled
        if logging:
            log.log_state(state)

        # Debug mode prints data live
        if debug:
            print("------ SMARTZONE DEBUG ------")

            print("Temperature:", state["temperature"], "C")
            print("Brightness:", state["light"], "%")
            print("Occupied:", state["occupied"])

            print("\nSystem Status")
            print("Lighting:", state["lighting_on"])
            print("Heating:", state["heating_on"])
            print("Cooling:", state["cooling_on"])

            print("-----------------------------\n")

        try:
            conn, addr = server.accept()
            request = conn.recv(1024).decode()

            # Safely extract path
            try:
                path = request.split(" ")[1]
            except:
                path = "/"

            # -----------------------------
            # IMAGE REQUESTS
            # -----------------------------
            if path.endswith(".jpg") or path.endswith(".png"):

                try:
                    filename = path[1:]

                    conn.send("HTTP/1.1 200 OK\r\n")

                    if filename.endswith(".png"):
                        conn.send("Content-Type: image/png\r\n")
                    else:
                        conn.send("Content-Type: image/jpeg\r\n")

                    conn.send("Connection: close\r\n\r\n")

                    with open(filename, "rb") as f:
                        while True:
                            chunk = f.read(1024)
                            if not chunk:
                                break
                            conn.write(chunk)

                    conn.close()
                    continue

                except:
                    conn.send("HTTP/1.1 404 Not Found\r\n\r\n")
                    conn.close()
                    continue

            # -----------------------------
            # NORMAL PAGE ROUTING
            # -----------------------------
            response = web.route(path, state)

            conn.send("HTTP/1.1 200 OK\r\n")

            if path.startswith("/status"):
                conn.send("Content-Type: application/json\r\n")
                conn.send("Cache-Control: no-cache\r\n")
            else:
                conn.send("Content-Type: text/html\r\n")

            conn.send("Connection: close\r\n\r\n")

            conn.sendall(response)
            conn.close()

        except OSError:
            pass


# -----------------------------
# MAIN MENU
# -----------------------------
def main_menu():

    print("\nWelcome To SmartZone!\n")
    print("Please select an option:\n")

    print("1: Run the system")
    print("   (Starts monitoring + data logging)")

    print("2: Run debug mode")
    print("   (Runs system and prints live data, no logging)")

    print("3: Run testing")
    print("   (Sensor calibration mode)\n")

    choice = input("Enter option (1-3): ")

    if choice == "1":
        run_system(logging=True, debug=False)

    elif choice == "2":
        run_system(logging=False, debug=True)

    elif choice == "3":
        test.run()

    else:
        print("Invalid selection")
        main_menu()


# -----------------------------
# START PROGRAM
# -----------------------------
main_menu()
