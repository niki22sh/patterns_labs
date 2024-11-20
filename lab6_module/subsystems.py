from facade.singleton import SingletonMeta

class SettingsManager(metaclass=SingletonMeta):
    def __init__(self):
        self.preferred_temperature = 22
        self.lighting_preset = "тепле"

    def get_preferred_temperature(self):
        return self.preferred_temperature

    def get_lighting_preset(self):
        return self.lighting_preset


class EnergyManager(metaclass=SingletonMeta):
    def __init__(self):
        self.energy_usage = 0

    def monitor_usage(self):
        return f"Поточне споживання енергії: {self.energy_usage} кВт·год"

    def optimize_energy(self):
        return "Енергоспоживання оптимізовано!"


class LightingSystem:
    def turn_on_lights(self):
        return "Освітлення увімкнено."

    def turn_off_lights(self):
        return "Освітлення вимкнено."

    def set_brightness(self, level):
        return f"Яскравість встановлена на {level}%."


class SecuritySystem:
    def arm_system(self):
        return "Система безпеки активована."

    def disarm_system(self):
        return "Система безпеки деактивована."


class ClimateControlSystem:
    def set_temperature(self, target_temp):
        return f"Температура встановлена на {target_temp}°C."


class EntertainmentSystem:
    def play_music(self):
        return "Музика відтворюється."

    def stop_music(self):
        return "Музика зупинена."


