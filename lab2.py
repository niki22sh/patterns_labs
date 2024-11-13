import math
import json
from abc import ABC, abstractmethod

# === Інтерфейси ===
class IPort(ABC):
    @abstractmethod
    def incomingShip(self, ship):
        pass
    
    @abstractmethod
    def outgoingShip(self, ship):
        pass

class IShip(ABC):
    @abstractmethod
    def sailTo(self, port):
        pass
    
    @abstractmethod
    def reFuel(self, amount):
        pass
    
    @abstractmethod
    def load(self, container):
        pass
    
    @abstractmethod
    def unLoad(self, container):
        pass

# === Абстрактний клас для контейнерів ===
class Container(ABC):
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight

    @abstractmethod
    def consumption(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Container) and self.ID == other.ID and self.weight == other.weight

# === Різні типи контейнерів ===
class BasicContainer(Container):
    def consumption(self):
        return 2.5 * self.weight

class HeavyContainer(Container):
    def consumption(self):
        return 3.0 * self.weight

class RefrigeratedContainer(HeavyContainer):
    def consumption(self):
        return 5.0 * self.weight

class LiquidContainer(HeavyContainer):
    def consumption(self):
        return 4.0 * self.weight

# === Клас Порт ===
class Port(IPort):
    def __init__(self, ID, latitude, longitude):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []
        self.history = []
        self.current = []

    def incomingShip(self, ship):
        if ship not in self.current:
            self.current.append(ship)
    
    def outgoingShip(self, ship):
        if ship not in self.history:
            self.history.append(ship)
        self.current.remove(ship)

    def getDistance(self, other):
        # Розрахунок геопросторової відстані між портами
        return math.sqrt((self.latitude - other.latitude)**2 + (self.longitude - other.longitude)**2)

# === Клас Корабель ===
class Ship(IShip):
    def __init__(self, ID, fuel, currentPort, totalWeightCapacity, maxAllContainers, maxHeavyContainers, maxRefrigeratedContainers, maxLiquidContainers, fuelConsumptionPerKM):
        self.ID = ID
        self.fuel = fuel
        self.currentPort = currentPort
        self.totalWeightCapacity = totalWeightCapacity
        self.maxAllContainers = maxAllContainers
        self.maxHeavyContainers = maxHeavyContainers
        self.maxRefrigeratedContainers = maxRefrigeratedContainers
        self.maxLiquidContainers = maxLiquidContainers
        self.fuelConsumptionPerKM = fuelConsumptionPerKM
        self.containers = []

    def sailTo(self, port):
        distance = self.currentPort.getDistance(port)
        totalConsumption = self.fuelConsumptionPerKM * distance + sum([c.consumption() for c in self.containers])
        if self.fuel >= totalConsumption:
            self.fuel -= totalConsumption
            self.currentPort.outgoingShip(self)
            port.incomingShip(self)
            self.currentPort = port
            return True
        return False

    def reFuel(self, amount):
        self.fuel += amount

    def load(self, container):
        if len(self.containers) < self.maxAllContainers:
            self.containers.append(container)
            return True
        return False

    def unLoad(self, container):
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

# === Головна програма для роботи з JSON ===
def main():
    # Завантаження вхідних даних з файлу
    with open("input.json", "r") as file:
        data = json.load(file)

    # Списки для збереження портів та кораблів
    ports = []
    ships = []

    # Створення портів
    for port_data in data["ports"]:
        port = Port(port_data["ID"], port_data["latitude"], port_data["longitude"])
        ports.append(port)

    # Створення кораблів
    for ship_data in data["ships"]:
        port = next(p for p in ports if p.ID == ship_data["currentPortID"])
        ship = Ship(ship_data["ID"], ship_data["fuel"], port, ship_data["totalWeightCapacity"], 
                    ship_data["maxAllContainers"], ship_data["maxHeavyContainers"], 
                    ship_data["maxRefrigeratedContainers"], ship_data["maxLiquidContainers"], 
                    ship_data["fuelConsumptionPerKM"])
        port.incomingShip(ship)
        ships.append(ship)

    # Обробка операцій (наприклад, навантаження, вивантаження, плавання)
    for operation in data["operations"]:
        if operation["action"] == "load":
            ship = next(s for s in ships if s.ID == operation["shipID"])
            container = BasicContainer(operation["containerID"], operation["weight"])
            ship.load(container)
        elif operation["action"] == "unload":
            ship = next(s for s in ships if s.ID == operation["shipID"])
            container = next(c for c in ship.containers if c.ID == operation["containerID"])
            ship.unLoad(container)
        elif operation["action"] == "sail":
            ship = next(s for s in ships if s.ID == operation["shipID"])
            destination_port = next(p for p in ports if p.ID == operation["portID"])
            ship.sailTo(destination_port)
        elif operation["action"] == "refuel":
            ship = next(s for s in ships if s.ID == operation["shipID"])
            ship.reFuel(operation["amount"])

    # Формування вихідних даних
    output_data = {}
    for port in ports:
        port_data = {
            "lat": port.latitude,
            "lon": port.longitude,
            "basic_container": [c.ID for c in port.containers if isinstance(c, BasicContainer)],
            "heavy_container": [c.ID for c in port.containers if isinstance(c, HeavyContainer)],
            "liquid_container": [c.ID for c in port.containers if isinstance(c, LiquidContainer)],
            "ship_0": {}
        }
        for ship in port.current:
            ship_data = {
                "fuel_left": round(ship.fuel, 2),
                "basic_container": [c.ID for c in ship.containers if isinstance(c, BasicContainer)],
                "heavy_container": [c.ID for c in ship.containers if isinstance(c, HeavyContainer)],
                "liquid_container": [c.ID for c in ship.containers if isinstance(c, LiquidContainer)],
                "refrigerated_container": [c.ID for c in ship.containers if isinstance(c, RefrigeratedContainer)]
            }
            port_data[f"ship_{ship.ID}"] = ship_data
        output_data[f"Port {port.ID}"] = port_data

    # Запис вихідних даних у файл
    with open("output.json", "w") as file:
        json.dump(output_data, file, indent=4)

if __name__ == "__main__":
    main()
