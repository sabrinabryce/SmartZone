# web.py
from actuators import lighting, heating, cooling

PASSWORD = "1234"

# Persistent override flags
overrides = {
    "lighting": False,
    "heating": False,
    "cooling": False
}

#
if path.startswith("/images/"):
    try:
        with open(path[1:], "rb") as f:
            conn.send("HTTP/1.1 200 OK\r\n")
            conn.send("Content-Type: image/png\r\n")
            conn.send("Connection: close\r\n\r\n")

            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                conn.send(chunk)

    except:
        conn.send("HTTP/1.1 404 Not Found\r\n\r\n")

    conn.close()
    return
# -----------------------------
# ROUTER
# -----------------------------
def route(path, state):

    if path == "/":
        return login_page()

    elif path.startswith("/status"):
        return render_status(state)

    elif path.startswith("/login"):
        if "pass=1234" in path:
            return page2()
        else:
            return login_page(error=True)

    elif path == "/library":
        return page3()

    elif path == "/floor":
        return page4(state)

    elif path.startswith("/zone101"):
        return page5(state, path)

    else:
        return login_page()


# -----------------------------
# STATUS JSON
# -----------------------------
def render_status(state):

    return '{{"temperature":{},"light":{},"occupied":{},"lighting":{},"heating":{},"cooling":{},"lighting_override":{},"heating_override":{},"cooling_override":{}}}'.format(
        state["temperature"],
        state["light"],
        str(state["occupied"]).lower(),
        str(state["lighting_on"]).lower(),
        str(state["heating_on"]).lower(),
        str(state["cooling_on"]).lower(),
        str(overrides["lighting"]).lower(),
        str(overrides["heating"]).lower(),
        str(overrides["cooling"]).lower()
    )
# -----------------------------
# COMMON HEADER
# -----------------------------
def header():
    return """
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {
        font-family: Verdana, Arial, sans-serif;
        font-size: 24px;
        text-align:center;
        background:white;
    }

    h1 { font-size:36px; }
    h2 { font-size:30px; }

    .map { position:relative; display:inline-block; }
    .map img { max-width:100%; height:auto; }

    .link {
        position:absolute;
        font-size:28px;
        font-weight:bold;
        text-decoration:none;
    }

    .blue { color:blue; }
    .grey { color:grey; }

    .glow {
        animation:pulse 1s infinite;
    }

    @keyframes pulse {
        0% { text-shadow:0 0 5px #00ff00; }
        50% { text-shadow:0 0 20px #00ff00; }
        100% { text-shadow:0 0 5px #00ff00; }
    }

    button {
        font-size:22px;
        padding:10px;
        margin:5px;
    }

    input {
        font-size:22px;
        padding:10px;
    }

    .status-circle {
        display:inline-block;
        width:25px;
        height:25px;
        border-radius:50%;
        margin-left:10px;
    }

    .red { background:red; }
    .green { background:green; }
    .bluebg { background:blue; }
    .off { background:lightgrey; }

    .override {
        box-shadow:0 0 15px red;
    }

    </style>
    </head>
    <body>
    """

def footer():
    return "</body></html>"


# -----------------------------
# PAGE 1 LOGIN
# -----------------------------
def login_page(error=False):

    message = ""
    if error:
        message = "<p style='color:red;'>Incorrect Password</p>"

    return header() + f"""
    <img src="/images/logo.png"><br><br>
    <h2>Password:</h2>
    {message}
    <form action="/login">
        <input type="password" name="pass">
        <input type="submit" value="Enter">
    </form>
    """ + footer()


# -----------------------------
# PAGE 2
# -----------------------------
def page2():
    return header() + """
    <div class="map">
        <img src="/images/ringroad.png">
        <a href="/library" class="link blue"
           style="top:150px; left:300px;">
           [ McPherson Library ]
        </a>
    </div>
    """ + footer()


# -----------------------------
# PAGE 3
# -----------------------------
def page3():
    return header() + """
    <h1>McPherson Library</h1><br>
    <p class="grey">[ Lower Level ]</p>
    <p><a href="/floor" class="blue">[ Main Level ]</a></p>
    <p class="grey">[ First Floor ]</p>
    <p class="grey">[ Second Floor ]</p>
    <p class="grey">[ Third Floor ]</p>
    """ + footer()


# -----------------------------
# PAGE 4 FLOOR MAP
# -----------------------------

def page4(state):

    # Zone 101 dynamic color
    zone101_class = "glow" if state["lighting_on"] else "blue"

    # Inactive zones (always grey)
    zone102_class = "grey"
    zone103_class = "grey"
    zone104_class = "grey"

    return header() + f"""
    <div class="map">
        <img src="/images/mainfloor.png">

        <!-- Zone 101 (ACTIVE) -->
        <a href="/zone101"
           class="link {zone101_class}"
           style="top:200px; left:250px;">
           [101]
        </a>

        <!-- Zone 102 (INACTIVE) -->
        <span class="link {zone102_class}"
              style="top:200px; left:400px;">
              [102]
        </span>

        <!-- Zone 103 (INACTIVE) -->
        <span class="link {zone103_class}"
              style="top:300px; left:250px;">
              [103]
        </span>

        <!-- Zone 104 (INACTIVE) -->
        <span class="link {zone104_class}"
              style="top:300px; left:400px;">
              [104]
        </span>

    </div>

    <script>
    function updateStatus() {{
        fetch('/status')
        .then(r => r.json())
        .then(data => {{
            var zone101 = document.querySelector('a[href="/zone101"]');
            zone101.className = "link " + (data.lighting ? "glow" : "blue");
        }});
    }}

    updateStatus();
    setInterval(updateStatus, 1000);
    </script>
    """ + footer()

# -----------------------------
# PAGE 5 ZONE CONTROL
# -----------------------------
def page5(state, path):

    # -------------------------------------------------
    # MANUAL OVERRIDE LOGIC (MODIFIES STATE DIRECTLY)
    # -------------------------------------------------

    # LIGHTING
    if "light=on" in path:
        state["lighting_override"] = True
        state["lighting_on"] = True

    if "light=off" in path:
        state["lighting_override"] = False

    # HEATING
    if "heat=on" in path:
        state["heating_override"] = True
        state["heating_on"] = True

    if "heat=off" in path:
        state["heating_override"] = False

    # COOLING
    if "cool=on" in path:
        state["cooling_override"] = True
        state["cooling_on"] = True

    if "cool=off" in path:
        state["cooling_override"] = False

    return header() + f"""
    <h1>Zone 101</h1>

    <h2>Environmental Status</h2>
    <p>Temperature: <span id="temp">{state['temperature']}</span> °C</p>
    <p>Light Level: <span id="light">{state['light']}</span> %</p>
    <p>Occupancy:
       <span id="occ_text">
           {"OCCUPIED" if state["occupied"] else "UNOCCUPIED"}
       </span>
    </p>

    <h2>System Status</h2>

    <p>Lighting
        <span id="light_circle"
              class="status-circle {'green' if state['lighting_on'] else 'off'}"></span>
        <span id="light_text">
            {"ON" if state["lighting_on"] else "OFF"}
        </span>
        {"(MANUAL)" if state["lighting_override"] else "(AUTO)"}
    </p>

    <p>Heating
        <span id="heat_circle"
              class="status-circle {'red' if state['heating_on'] else 'off'}"></span>
        <span id="heat_text">
            {"ON" if state["heating_on"] else "OFF"}
        </span>
        {"(MANUAL)" if state["heating_override"] else "(AUTO)"}
    </p>

    <p>Cooling
        <span id="cool_circle"
              class="status-circle {'bluebg' if state['cooling_on'] else 'off'}"></span>
        <span id="cool_text">
            {"ON" if state["cooling_on"] else "OFF"}
        </span>
        {"(MANUAL)" if state["cooling_override"] else "(AUTO)"}
    </p>

    <h2>Manual Override</h2>

    <p>
        <a href="/zone101?light=on"><button>Light ON</button></a>
        <a href="/zone101?light=off"><button>Light OFF (Return to Auto)</button></a>
    </p>

    <p>
        <a href="/zone101?heat=on"><button>Heat ON</button></a>
        <a href="/zone101?heat=off"><button>Heat OFF (Return to Auto)</button></a>
    </p>

    <p>
        <a href="/zone101?cool=on"><button>Cool ON</button></a>
        <a href="/zone101?cool=off"><button>Cool OFF (Return to Auto)</button></a>
    </p>

    <br><a href="/floor">Back to Floor</a>

    <script>
    function updateStatus() {{
        fetch('/status')
        .then(r => r.json())
        .then(data => {{

            document.getElementById("temp").innerText = data.temperature;
            document.getElementById("light").innerText = data.light;
            document.getElementById("occ_text").innerText =
                data.occupied ? "OCCUPIED" : "UNOCCUPIED";

            document.getElementById("light_circle").className =
                "status-circle " + (data.lighting ? "green" : "off");

            document.getElementById("heat_circle").className =
                "status-circle " + (data.heating ? "red" : "off");

            document.getElementById("cool_circle").className =
                "status-circle " + (data.cooling ? "bluebg" : "off");

            document.getElementById("light_text").innerText =
                data.lighting ? "ON" : "OFF";

            document.getElementById("heat_text").innerText =
                data.heating ? "ON" : "OFF";

            document.getElementById("cool_text").innerText =
                data.cooling ? "ON" : "OFF";
        }});
    }}

    updateStatus();
    setInterval(updateStatus, 1000);
    </script>
    """ + footer()