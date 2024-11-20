class Appliance:
    def start(self):
        raise NotImplementedError("Цей метод має бути реалізований у підкласі")

    def stop(self):
        raise NotImplementedError("Цей метод має бути реалізований у підкласі")


class Fan(Appliance):
    def start(self):
        return "Вентилятор увімкнено."

    def stop(self):
        return "Вентилятор вимкнено."


class AirConditioner(Appliance):
    def start(self):
        return "Кондиціонер увімкнено."

    def stop(self):
        return "Кондиціонер вимкнено."


class Switch:
    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    def turn_on(self):
        return self.appliance.start()

    def turn_off(self):
        return self.appliance.stop()


class RemoteControl(Switch):
    def __init__(self, appliance: Appliance):
        super().__init__(appliance)

    def set_timer(self, minutes):
        return f"Таймер встановлено на {minutes} хвилин."
