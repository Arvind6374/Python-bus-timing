import datetime
from typing import Dict, List, Optional
import json
import os

class BusScheduleManager:
    def __init__(self):
        self.routes = {}
        self.schedules = {}
        self.buses = {}
        self.stops = {}
        
    def add_route(self, route_id: str, stops: List[str], route_name: str):
        self.routes[route_id] = {
            'route_name': route_name,
            'stops': stops,
            'active': True
        }
        
    def add_bus(self, bus_id: str, route_id: str, capacity: int):
        self.buses[bus_id] = {
            'route_id': route_id,
            'capacity': capacity,
            'status': 'active'
        }
        
    def add_schedule(self, route_id: str, schedule_data: Dict):
        if route_id not in self.routes:
            raise ValueError(f"Route {route_id} does not exist")
            
        self.schedules[route_id] = schedule_data
        
    def get_next_bus(self, stop_id: str, current_time: Optional[datetime.datetime] = None):
        if current_time is None:
            current_time = datetime.datetime.now()
            
        next_buses = []
        current_time_str = current_time.strftime('%H:%M')
        
        for route_id, schedule in self.schedules.items():
            if stop_id in self.routes[route_id]['stops']:
                stop_times = schedule.get(stop_id, [])
                for time in stop_times:
                    if time > current_time_str:
                        next_buses.append({
                            'route_id': route_id,
                            'time': time,
                            'route_name': self.routes[route_id]['route_name']
                        })
                        
        return sorted(next_buses, key=lambda x: x['time'])
        
    def save_data(self, filename: str = 'bus_data.json'):
        data = {
            'routes': self.routes,
            'schedules': self.schedules,
            'buses': self.buses,
            'stops': self.stops
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            
    def load_data(self, filename: str = 'bus_data.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.routes = data.get('routes', {})
                self.schedules = data.get('schedules', {})
                self.buses = data.get('buses', {})
S                self.stops = data.get('stops', {})

class BusScheduleInterface:
    def __init__(self):
        self.manager = BusScheduleManager()
        
    def setup_sample_data(self):
        self.manager.add_route('R1', ['S1', 'S2', 'S3', 'S4'], 'SMBT')
        self.manager.add_route('R2', ['S3', 'S4', 'S5', 'S6'], 'TOWN BUS')
        
    
        schedule_r1 = {
            'S1': ['07:00', '08:00', '09:00', '15:00', '16:00', '17:00'],
            'S2': ['07:15', '08:15', '09:15', '15:15', '16:15', '17:15'],
            'S3': ['07:30', '08:30', '09:30', '15:30', '16:30', '17:30'],
            'S4': ['07:45', '08:45', '09:45', '15:45', '16:45', '17:45']
        }
        
        schedule_r2 = {
            'S3': ['07:00', '08:00', '09:00', '15:00', '16:00', '17:00'],
            'S4': ['07:15', '08:15', '09:15', '15:15', '16:15', '17:15'],
            'S5': ['07:30', '08:30', '09:30', '15:30', '16:30', '17:30'],
            'S6': ['07:45', '08:45', '09:45', '15:45', '16:45', '17:45']
        }
        
        self.manager.add_schedule('R1', schedule_r1)
        self.manager.add_schedule('R2', schedule_r2)
        
        self.manager.add_bus('B1', 'R1', 50)
        self.manager.add_bus('B2', 'R1', 50)
        self.manager.add_bus('B3', 'R2', 40)
        self.manager.add_bus('B4', 'R2', 40)
        
    def run_interface(self):
        print("\nWelcome to Bus Schedule System")
        self.setup_sample_data()
        
        while True:
            print("\nOptions:")
            print("1. View next buses from a stop")
            print("2. View route information")
            print("3. View all routes")
            print("4. Save schedule data")
            print("5. Load schedule data")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                stop_id = input("Enter stop ID (e.g., S1): ")
                next_buses = self.manager.get_next_bus(stop_id)
                if next_buses:
                    print(f"\nNext buses from stop {stop_id}:")
                    for bus in next_buses:
                        print(f"Route: {bus['route_name']} ({bus['route_id']}) - Time: {bus['time']}")
                else:
                    print("No more buses scheduled from this stop today.")
                    
            elif choice == '2':
                route_id = input("Enter route ID (e.g., R1): ")
                if route_id in self.manager.routes:
                    route = self.manager.routes[route_id]
                    print(f"\nRoute: {route['route_name']}")
                    print(f"Stops: {' -> '.join(route['stops'])}")
                    if route_id in self.manager.schedules:
                        print("\nSchedule:")
                        for stop, times in self.manager.schedules[route_id].items():
                            print(f"{stop}: {', '.join(times)}")
                else:
                    print("Route not found.")
                    
            elif choice == '3':
                print("\nAll Routes:")
                for route_id, route in self.manager.routes.items():
                    print(f"{route_id}: {route['route_name']} - Stops: {' -> '.join(route['stops'])}")
                    
            elif choice == '4':
                self.manager.save_data()
                print("Schedule data saved successfully.")
                
            elif choice == '5':
                self.manager.load_data()
                print("Schedule data loaded successfully.")
                
            elif choice == '6':
                print("Thank you for using Bus Schedule System.")
                break
                
            else:
                print("Invalid choice. Please try again.")

def main():
    interface = BusScheduleInterface()
    interface.run_interface()

if __name__ == "__main__":
    main()
