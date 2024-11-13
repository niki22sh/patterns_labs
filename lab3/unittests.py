import unittest
from unittest.mock import Mock
from lab3 import Port, ShipBuilder, ContainerFactory, BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer

class TestPortManagement(unittest.TestCase):

    def setUp(self):
  
        self.port1 = Port(ID=1, latitude=50.45, longitude=30.52)
        self.port2 = Port(ID=2, latitude=52.37, longitude=4.90)
        
        self.ship = ShipBuilder(ID=1, fuel=500, currentPort=self.port1) \
            .set_total_weight_capacity(1000) \
            .set_container_limits(10, 5, 2, 3) \
            .set_fuel_consumption(1.0) \
            .build()

        self.port1.incomingShip(self.ship)

    def test_port_incoming_outgoing(self):
     
        self.assertIn(self.ship, self.port1.current)
        
        self.port1.outgoingShip(self.ship)
        self.assertNotIn(self.ship, self.port1.current)
        self.assertIn(self.ship, self.port1.history)

    def test_sailTo(self):
        distance = self.port1.getDistance(self.port2)
        fuel_needed = distance * self.ship.fuelConsumptionPerKM
        
        self.ship.reFuel(fuel_needed)
        
        success = self.ship.sailTo(self.port2)
        self.assertTrue(success)
        self.assertEqual(self.ship.currentPort, self.port2)
        self.assertNotIn(self.ship, self.port1.current)
        self.assertIn(self.ship, self.port2.current)

    def test_load_unload_containers(self):

        container1 = ContainerFactory.create_container("basic", ID=101, weight=100)
        container2 = ContainerFactory.create_container("heavy", ID=102, weight=200)
        
        load_success1 = self.ship.load(container1)
        load_success2 = self.ship.load(container2)
        self.assertTrue(load_success1)
        self.assertTrue(load_success2)
        self.assertIn(container1, self.ship.containers)
        self.assertIn(container2, self.ship.containers)

        unload_success = self.ship.unLoad(container1)
        self.assertTrue(unload_success)
        self.assertNotIn(container1, self.ship.containers)

    def test_container_factory(self):
        basic_container = ContainerFactory.create_container("basic", ID=1, weight=100)
        heavy_container = ContainerFactory.create_container("heavy", ID=2, weight=200)
        refrigerated_container = ContainerFactory.create_container("refrigerated", ID=3, weight=150)
        liquid_container = ContainerFactory.create_container("liquid", ID=4, weight=250)

        self.assertIsInstance(basic_container, BasicContainer)
        self.assertIsInstance(heavy_container, HeavyContainer)
        self.assertIsInstance(refrigerated_container, RefrigeratedContainer)
        self.assertIsInstance(liquid_container, LiquidContainer)

    def test_fuel_consumption(self):
        basic_container = ContainerFactory.create_container("basic", ID=1, weight=100)
        self.ship.load(basic_container)
        
        distance = 10
        total_consumption = distance * self.ship.fuelConsumptionPerKM + basic_container.consumption()
        
        self.ship.reFuel(total_consumption)
        success = self.ship.sailTo(self.port2)
        self.assertTrue(success)
        self.assertAlmostEqual(self.ship.fuel, 0, places=2)

if __name__ == '__main__':
    unittest.main()

