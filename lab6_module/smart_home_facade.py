from facade.subsystems import LightingSystem, SecuritySystem, ClimateControlSystem, EntertainmentSystem, SettingsManager
from facade.bridge import Fan, AirConditioner, RemoteControl

class SmartHomeFacade:
    def __init__(self):
        self.lighting = LightingSystem()
        self.security = SecuritySystem()
        self.climate = ClimateControlSystem()
        self.entertainment = EntertainmentSystem()
        self.settings = SettingsManager()

        # Нові пристрої (Bridge Pattern)
        self.fan = RemoteControl(Fan())
        self.ac = RemoteControl(AirConditioner())

    def activate_security_system(self):
        return self.security.arm_system()

    def control_lighting(self, brightness=None):
        if brightness is not None:
            return self.lighting.set_brightness(brightness)
        else:
            return self.lighting.turn_on_lights()

    def set_climate_control(self, target_temp):
        return self.climate.set_temperature(target_temp)

    def play_entertainment(self):
        return self.entertainment.play_music()

    def control_fan(self, action: str):
        if action == "on":
            return self.fan.turn_on()
        elif action == "off":
            return self.fan.turn_off()

    def control_ac(self, action: str):
        if action == "on":
            return self.ac.turn_on()
        elif action == "off":
            return self.ac.turn_off()

