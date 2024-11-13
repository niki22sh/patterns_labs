import math
import json
from abc import ABC, abstractmethod

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

class Container(ABC):
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight

    @abstractmethod
    def consumption(self):
        pass

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

class ContainerFactory:
    @staticmethod
    def create_container(container_type, ID, weight):
        if container_type == "basic":
            return BasicContainer(ID, weight)
        elif container_type == "heavy":
            return HeavyContainer(ID, weight)
        elif container_type == "refrigerated":
            return RefrigeratedContainer(ID, weight)
        elif container_type == "liquid":
            return LiquidContainer(ID, weight)
        else:
            raise ValueError("Unknown container type")

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
        return math.sqrt((self.latitude - other.latitude)**2 + (self.longitude - other.longitude)**2)

class ShipBuilder:
    def __init__(self, ID, fuel, currentPort):
        self.ID = ID
        self.fuel = fuel
        self.currentPort = currentPort
        self.totalWeightCapacity = 0
        self.maxAllContainers = 0
        self.maxHeavyContainers = 0
        self.maxRefrigeratedContainers = 0
        self.maxLiquidContainers = 0
        self.fuelConsumptionPerKM = 0

    def set_total_weight_capacity(self, capacity):
        self.totalWeightCapacity = capacity
        return self

    def set_container_limits(self, all_containers, heavy, refrigerated, liquid):
        self.maxAllContainers = all_containers
        self.maxHeavyContainers = heavy
        self.maxRefrigeratedContainers = refrigerated
        self.maxLiquidContainers = liquid
        return self

    def set_fuel_consumption(self, consumption):
        self.fuelConsumptionPerKM = consumption
        return self

    def build(self):
        return Ship(self.ID, self.fuel, self.currentPort, self.totalWeightCapacity, self.maxAllContainers, 
                    self.maxHeavyContainers, self.maxRefrigeratedContainers, self.maxLiquidContainers, 
                    self.fuelConsumptionPerKM)

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
    
def main():

    ports = [
        Port(ID=1, latitude=50.45, longitude=30.52),
        Port(ID=2, latitude=52.37, longitude=4.90)
    ]

    ships = [
        ShipBuilder(ID=1, fuel=500, currentPort=ports[0])
            .set_total_weight_capacity(1000)
            .set_container_limits(10, 5, 2, 3)
            .set_fuel_consumption(1.0)
            .build(),
        
        ShipBuilder(ID=2, fuel=600, currentPort=ports[1])
            .set_total_weight_capacity(1200)
            .set_container_limits(12, 6, 3, 4)
            .set_fuel_consumption(1.2)
            .build()
    ]
    ports[0].incomingShip(ships[0])
    ports[1].incomingShip(ships[1])

    operations = [
        {"action": "load", "shipID": 1, "type": "basic", "containerID": 101, "weight": 100},
        {"action": "sail", "shipID": 1, "portID": 2},
        {"action": "refuel", "shipID": 1, "amount": 300},
        {"action": "load", "shipID": 2, "type": "heavy", "containerID": 102, "weight": 200},
        {"action": "sail", "shipID": 2, "portID": 1},
        {"action": "refuel", "shipID": 2, "amount": 400}
    ]

    for operation in operations:
        if operation["action"] == "load":
            ship = next(s for s in ships if s.ID == operation["shipID"])
            container = ContainerFactory.create_container(operation["type"], operation["containerID"], operation["weight"])
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

    with open("D:\output1.json", "w") as file:
        json.dump(output_data, file, indent=4)

if __name__ == "__main__":
    main()



