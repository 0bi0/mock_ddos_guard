from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, FastAPI
from simulator import generate_traffic
from detector import analyze_event
import time

app = FastAPI(title="Mock DDoS Guard")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔥 GLOBAL SIMULATION STATE
IS_ATTACKING = False
DEFENCES_ENABLED = False
LAST_EVENT = 0

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/toggle-attack")
def toggle_attack():
    global IS_ATTACKING
    IS_ATTACKING = not IS_ATTACKING
    return {"attacking": IS_ATTACKING}


@app.post("/toggle-defences")
def toggle_defences():
    global DEFENCES_ENABLED
    DEFENCES_ENABLED = not DEFENCES_ENABLED
    return {"defences": DEFENCES_ENABLED}


@app.get("/traffic")
def get_traffic():
    event = generate_traffic(
        attack=IS_ATTACKING,
        mitigated=DEFENCES_ENABLED
    )
    alert = analyze_event(event, DEFENCES_ENABLED)

    return {
        "traffic": event,
        "alert": alert,
        "attacking": IS_ATTACKING,
        "defences": DEFENCES_ENABLED
    }
