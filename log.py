# log.py
import utime
import os
from config import ZONE_ID

LOG_INTERVAL = 60  # seconds

_last_log_time = 0
_log_filename = None


# -----------------------------
# Create New Log File Per Boot
# -----------------------------
def _create_new_log():

    global _log_filename

    index = 1
    while True:
        filename = "log_{}.csv".format(index)
        try:
            os.stat(filename)
            index += 1
        except OSError:
            # File does not exist
            _log_filename = filename
            break

    # Create file and write header
    with open(_log_filename, "w") as f:
        f.write("timestamp,zone,occupied,temp_C,light_percent,lighting,heating,cooling\n")

    print("Logging to:", _log_filename)


# -----------------------------
# Public Logging Function
# -----------------------------
def log_state(state):

    global _last_log_time

    current_time = utime.time()

    # Create file if first run
    if _log_filename is None:
        _create_new_log()

    # Only log once per minute
    if current_time - _last_log_time >= LOG_INTERVAL:

        _last_log_time = current_time

        log_line = "{},{},{},{},{},{},{},{}\n".format(
            current_time,
            ZONE_ID,
            state["occupied"],
            state["temperature"],
            state["light"],
            state["lighting_on"],
            state["heating_on"],
            state["cooling_on"]
        )

        with open(_log_filename, "a") as f:
            f.write(log_line)

        print("Logged at", current_time)

