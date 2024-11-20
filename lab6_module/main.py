from fastapi import FastAPI
from pydantic import BaseModel
from facade.smart_home_facade import SmartHomeFacade

app = FastAPI()
home_facade = SmartHomeFacade()


class LightingRequest(BaseModel):
    brightness: int


class ClimateRequest(BaseModel):
    temperature: int


class ActionRequest(BaseModel):
    action: str


@app.post("/activate_security/")
def activate_security():
    return {"message": home_facade.activate_security_system()}


@app.post("/control_lighting/")
def control_lighting(request: LightingRequest):
    if request.brightness:
        return {"message": home_facade.control_lighting(request.brightness)}
    else:
        return {"message": home_facade.control_lighting()}


@app.post("/set_climate/")
def set_climate(request: ClimateRequest):
    return {"message": home_facade.set_climate_control(request.temperature)}


@app.post("/play_music/")
def play_music():
    return {"message": home_facade.play_entertainment()}


@app.post("/control_fan/")
def control_fan(request: ActionRequest):
    return {"message": home_facade.control_fan(request.action)}


@app.post("/control_ac/")
def control_ac(request: ActionRequest):
    return {"message": home_facade.control_ac(request.action)}

