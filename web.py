# web.py
from actuators import lighting, heating, cooling

PASSWORD = "1234"

# Persistent override flags
overrides = {
    "lighting": False,
    "heating": False,
    "cooling": False
}

# -----------------------------
# ROUTER
# -----------------------------
def route(path, state):
        
    if path == "/":
        return login_page()

    elif path.startswith("/status"):
        return render_status(state)

    elif path.startswith("/login"):

        # If password parameter exists
        if "pass=" in path:
            if "pass=1234" in path:
                return page2()
            else:
                return login_page(error=True)

        # If no password submitted yet, just show login page
        return login_page()

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
        font-size: 22px;
        text-align: center;
        margin: 0;
        padding: 0;
        background: white;
    }

    img {
        max-width: 100%;
        height: auto;
        display: block;
    }

    .logo {
        width: 40vw;
        max-width: 600px;
        min-width: 180px;
        height: auto;
        margin: 40px auto 20px auto;
        display: block;
    }

    .zone-btn {
        font-size:20px;
        padding:10px 16px;
        border:none;
        border-radius:6px;
        color:white;
    }

    .occupied {
        background: #2ecc71;
        box-shadow: 0 0 12px #2ecc71;
    }

    .empty {
        background: #7f8c8d;
    }
    
     .inactive {
        background: #bdc3c7;
        color: #666;
        cursor: not-allowed;
        opacity: 0.7;
    }

    .inactive:hover {
        box-shadow: none;
    }
    
    .status-circle {
        display:inline-block;
        width:16px;
        height:16px;
        border-radius:50%;
        margin-right:8px;
        vertical-align:middle;
        border:2px solid black;
    }

    /* ON states */
    .green { background:#2ecc71; box-shadow:0 0 8px #2ecc71; }
    .red { background:#e74c3c; box-shadow:0 0 8px #e74c3c; }
    .bluebg { background:#3498db; box-shadow:0 0 8px #3498db; }

    /* OFF state */
    .off {
        background-color:white;
    }

    button {
        font-size:20px;
        padding:8px 14px;
        margin:5px;
    }

    input[type="password"] {
        font-size:20px;
        padding:8px;
        border: 2px solid black;
        border-radius: 4px;
        outline: none;
    }

    input[type="password"]:focus {
        border: 3px solid black;
        box-shadow: 0 0 6px black;
    }

    a:link {
    color: royalblue;
    text-decoration: underline;
    }

    a:visited {
        color: royalblue;
        text-decoration: underline;
    }

    a:hover {
        color: #0033cc;   /* slightly darker blue on hover */
    }

    a:active {
        color: royalblue;
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
    <div class="overlay">

        <img src="/SmartZone.jpg" class="logo">

        <h2>Password:</h2>
        {message}

        <form action="/login">
            <input type="password" name="pass">
            <br><br>
            <input type="submit" value="Enter">
        </form>

    </div>
    """ + footer()


# -----------------------------
# PAGE 2
# -----------------------------
def page2():
    return header() + """
    <div style="position:relative; width:100%; text-align:center;">

        <img src="/ringroad.jpg"
             style="max-width:100%; height:auto;">

        <!-- Example button -->
        <div style="position:absolute; top:40%; left:50%;
                    transform:translate(-50%, -50%);">
            <a href="/library">
                <button>Enter McPherson Library</button>
            </a>
        </div>

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
    <p class="grey">[ Second Floor ]</p>
    <p class="grey">[ Third Floor ]</p>
    <p class="grey">[ Fourth Floor ]</p>
    """ + footer()


# -----------------------------
# PAGE 4 FLOOR MAP
# -----------------------------
def page4(state):

    occ_status = "OCCUPIED" if state["occupied"] else "EMPTY"
    occ_class = "occupied" if state["occupied"] else "empty"

    return header() + f"""
    <div style="position:relative; width:100%; max-width:1200px; margin:auto;">

        <img src="/mainfloor.jpg">

        <!-- ZONE 101 - Middle Left -->
        <div style="position:absolute; top:50%; left:20%;">
            <a href="/zone101">
                <button id="zone101btn" class="zone-btn {occ_class}">
                    Zone 101 ({occ_status})
                </button>
            </a>
        </div>

        <!-- ZONE 102 - Top Left -->
        <div style="position:absolute; top:20%; left:9%;">
            <button class="zone-btn inactive" disabled>
                Zone 102 (INACTIVE)
            </button>
        </div>

        <!-- ZONE 103 - Left Center Middle -->
        <div style="position:absolute; top:45%; left:45%;">
            <button class="zone-btn inactive" disabled>
                Zone 103 (INACTIVE)
            </button>
        </div>

        <!-- ZONE 104 - Top Right -->
        <div style="position:absolute; top:30%; left:75%;">
            <button class="zone-btn inactive" disabled>
                Zone 104 (INACTIVE)
            </button>
        </div>

    </div>

    <script>
    function updateStatus() {{
        fetch('/status')
        .then(r => r.json())
        .then(data => {{

            let btn = document.getElementById("zone101btn");

            if (data.occupied) {{
                btn.className = "zone-btn occupied";
                btn.innerText = "Zone 101 (OCCUPIED)";
            }} else {{
                btn.className = "zone-btn empty";
                btn.innerText = "Zone 101 (EMPTY)";
            }}

        }});
    }}

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
        state["lighting_override"] = True
        state["lighting_on"] = False

    if "light=auto" in path:
        state["lighting_override"] = False

    # HEATING
    if "heat=on" in path:
        state["heating_override"] = True
        state["heating_on"] = True

    if "heat=off" in path:
        state["heating_override"] = True
        state["heating_on"] = False

    if "heat=auto" in path:
        state["heating_override"] = False

    # COOLING
    if "cool=on" in path:
        state["cooling_override"] = True
        state["cooling_on"] = True

    if "cool=off" in path:
        state["cooling_override"] = True
        state["cooling_on"] = False

    if "cool=auto" in path:
        state["cooling_override"] = False

    return header() + f"""
    <h1>McPherson Library | Zone 101</h1>

    <h2>Environmental Status</h2>
    <p>Temperature: <span id="temp">{state['temperature']}</span> °C</p>
    <p>Light Level: <span id="light">{state['light']}</span> %</p>
    <p>Occupancy:
       <span id="occ_text">
           {"OCCUPIED" if state["occupied"] else "UNOCCUPIED"}
       </span>
    </p>

    <h2>System Status</h2>

    <p>
        <span id="light_circle"
              class="status-circle {'green' if state['lighting_on'] else 'off'}"></span>
        Lighting
        <span id="light_text">
            {"ON" if state["lighting_on"] else "OFF"}
        </span>
        {"(MANUAL)" if state["lighting_override"] else "(AUTO)"}
    </p>

    <p>
        <span id="heat_circle"
              class="status-circle {'red' if state['heating_on'] else 'off'}"></span>
        Heating
        <span id="heat_text">
            {"ON" if state["heating_on"] else "OFF"}
        </span>
        {"(MANUAL)" if state["heating_override"] else "(AUTO)"}
    </p>

    <p>
        <span id="cool_circle"
              class="status-circle {'bluebg' if state['cooling_on'] else 'off'}"></span>
        Cooling
        <span id="cool_text">
            {"ON" if state["cooling_on"] else "OFF"}
        </span>
        {"(MANUAL)" if state["cooling_override"] else "(AUTO)"}
    </p>

    <h2>Manual Override</h2>

    <p>
    Lighting:
    <a href="/zone101?light=on"><button>ON</button></a>
    <a href="/zone101?light=off"><button>OFF</button></a>
    <a href="/zone101?light=auto"><button>AUTO</button></a>
    </p>

    <p>
    Heating:
    <a href="/zone101?heat=on"><button>ON</button></a>
    <a href="/zone101?heat=off"><button>OFF</button></a>
    <a href="/zone101?heat=auto"><button>AUTO</button></a>
    </p>

    <p>
    Cooling:
    <a href="/zone101?cool=on"><button>ON</button></a>
    <a href="/zone101?cool=off"><button>OFF</button></a>
    <a href="/zone101?cool=auto"><button>AUTO</button></a>
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
    setInterval(updateStatus, 2000);
    </script>
    """ + footer()