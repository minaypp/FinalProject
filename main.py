import heapq

class Item:
    def __init__(self, name, location, quantity):
        self.name = name
        self.location = location
        self.quantity = quantity

    def __str__(self):
        return f"Item(name={self.name}, location={self.location}, quantity={self.quantity})"


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, priority, item):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Warehouse:
    def __init__(self):
        self.locations = set()
        self.edges = {}
        self.items = {}

    def add_location(self, location_name):
        if location_name in self.locations:
            print(f"Location '{location_name}' already exists.")
        else:
            self.locations.add(location_name)
            if location_name not in self.edges:
                self.edges[location_name] = {}
            print(f"Location '{location_name}' added successfully.")

    def add_path(self, from_location, to_location, weight):
        if from_location not in self.locations:
            print(f"Error: Starting location '{from_location}' does not exist.")
            return
        if to_location not in self.locations:
            print(f"Error: Destination location '{to_location}' does not exist.")
            return
        if weight <= 0:
            print("Error: Weight (distance) must be a positive number.")
            return
        self.edges[from_location][to_location] = weight
        print(f"Path from '{from_location}' to '{to_location}' with weight {weight} added successfully.")

    def add_item(self, item_name, location, quantity):
        if location not in self.locations:
            print(f"Error: Location '{location}' does not exist. Please add the location first.")
            return
        if item_name in self.items:
            print(f"Item '{item_name}' already exists. Updating quantity.")
        item = Item(item_name, location, quantity)
        self.items[item_name] = item
        print(f"Item '{item_name}' added/updated at location '{location}' with quantity {quantity}.")

    def lookup_item(self, item_name):
        return self.items.get(item_name, None)

    def find_shortest_path(self, start, end):
        if start not in self.locations:
            return [], float('inf')
        if end not in self.locations:
            return [], float('inf')

        queue = PriorityQueue()
        queue.put(0, start)
        distances = {loc: float('inf') for loc in self.locations}
        distances[start] = 0
        previous = {loc: None for loc in self.locations}

        while not queue.empty():
            current_location = queue.get()

            if current_location == end:
                break

            for neighbor, weight in self.edges[current_location].items():
                alt = distances[current_location] + weight
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current_location
                    queue.put(alt, neighbor)

        if distances[end] == float('inf'):
            return [], float('inf')

        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]

        return path, distances[end]

    def get_item_route(self, item_names):
        current_location = 'Entrance'
        if 'Entrance' not in self.locations:
            print("Error: 'Entrance' location does not exist.")
            return [], float('inf')

        total_path = []
        total_distance = 0

        for item_name in item_names:
            item = self.lookup_item(item_name)
            if not item:
                print(f"Item '{item_name}' not found. Skipping...")
                continue
            path, distance = self.find_shortest_path(current_location, item.location)
            if not path:
                print(f"No route found to '{item.location}' for '{item_name}'. Skipping...")
                continue
            if total_path and path:
                total_path.extend(path[1:])
            else:
                total_path.extend(path)
            total_distance += distance
            current_location = item.location

        # Attempt to return to 'Exit'
        if 'Exit' in self.locations:
            final_path, final_distance = self.find_shortest_path(current_location, 'Exit')
            if final_path:
                if final_path[0] == current_location:
                    total_path.extend(final_path[1:])
                else:
                    total_path.extend(final_path)
                total_distance += final_distance
            else:
                print("No route found to 'Exit'. Ending route at last item location.")
        else:
            print("No 'Exit' location found. Ending route at last item location.")

        return total_path, total_distance

    def display_route(self, route):
        if route:
            print("Route: " + " -> ".join(route))
        else:
            print("No route available.")


class UserInterface:
    def __init__(self):
        self.warehouse = Warehouse()
        self.initialize_defaults()

    def initialize_defaults(self):
        # Default locations
        locations = ['Entrance', 'A1', 'A2', 'B1', 'B2', 'Exit']
        for loc in locations:
            self.warehouse.add_location(loc)

        # Default paths
        self.warehouse.add_path('Entrance', 'A1', 2)
        self.warehouse.add_path('A1', 'A2', 2)
        self.warehouse.add_path('A2', 'B2', 2)
        self.warehouse.add_path('B2', 'Exit', 3)
        self.warehouse.add_path('Entrance', 'B1', 4)
        self.warehouse.add_path('B1', 'B2', 1)
        self.warehouse.add_path('A1', 'B1', 2)
        # Added cycle
        self.warehouse.add_path('B2', 'A1', 1)

        # Default items
        self.warehouse.add_item('Item1', 'A1', 10)
        self.warehouse.add_item('Item2', 'B2', 5)
        self.warehouse.add_item('Item3', 'A2', 15)

    def main_menu(self):
        while True:
            print("\n----- Warehouse Management System -----")
            print("1. Add a new storage location")
            print("2. Add a path between locations")
            print("3. Add or update an item")
            print("4. View item details")
            print("5. Find shortest route between two locations")
            print("6. Calculate best route for multiple item retrieval")
            print("7. Help / Instructions")
            print("8. Run Automated Tests")
            print("9. Exit")
            choice = input("Select an option: ").strip()

            if choice == '1':
                self.add_location_ui()
            elif choice == '2':
                self.add_path_ui()
            elif choice == '3':
                self.add_item_ui()
            elif choice == '4':
                self.view_item_ui()
            elif choice == '5':
                self.find_shortest_route_ui()
            elif choice == '6':
                self.get_item_route_ui()
            elif choice == '7':
                self.display_help()
            elif choice == '8':
                self.run_tests()
            elif choice == '9':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_location_ui(self):
        location_name = input("Enter the name of the new location: ").strip()
        if location_name:
            self.warehouse.add_location(location_name)
        else:
            print("Invalid location name.")

    def add_path_ui(self):
        from_location = input("Enter the starting location: ").strip()
        to_location = input("Enter the destination location: ").strip()
        try:
            weight = float(input("Enter the weight (distance) of the path: ").strip())
        except ValueError:
            print("Invalid weight. Please enter a numeric value.")
            return
        self.warehouse.add_path(from_location, to_location, weight)

    def add_item_ui(self):
        item_name = input("Enter the name of the item: ").strip()
        location = input("Enter the storage location of the item: ").strip()
        try:
            quantity = int(input("Enter the quantity of the item: ").strip())
        except ValueError:
            print("Invalid quantity. Please enter an integer.")
            return
        self.warehouse.add_item(item_name, location, quantity)

    def view_item_ui(self):
        item_name = input("Enter the name of the item to view: ").strip()
        if not item_name:
            print("Invalid item name.")
            return
        item = self.warehouse.lookup_item(item_name)
        if item:
            print(item)
        else:
            print(f"Item '{item_name}' not found.")

    def find_shortest_route_ui(self):
        start = input("Enter the starting location: ").strip()
        end = input("Enter the destination location: ").strip()
        path, distance = self.warehouse.find_shortest_path(start, end)
        if path:
            print(f"Shortest path from '{start}' to '{end}':")
            self.warehouse.display_route(path)
            print(f"Total distance: {distance}")
        else:
            print(f"No path found from '{start}' to '{end}'.")

    def get_item_route_ui(self):
        user_input = input("Enter item names separated by commas: ").strip()
        if not user_input:
            print("No items entered.")
            return
        item_names = [name.strip() for name in user_input.split(',')]
        route, total_distance = self.warehouse.get_item_route(item_names)
        if route:
            print("Optimal route to collect items:")
            self.warehouse.display_route(route)
            print(f"Total distance: {total_distance}")
        else:
            print("No valid route was found for the given items.")

    def display_help(self):
        print("\n--- Help / Instructions ---")
        print("This warehouse management system allows you to:")
        print("- Add new storage locations and paths between them")
        print("- Add items to locations and view their details")
        print("- Find the shortest route between two locations")
        print("- Calculate the best route to retrieve multiple items and return to 'Exit'")
        print("\nTips:")
        print("- Ensure that all locations you reference when adding paths or items already exist.")
        print("- When searching for shortest routes, verify the start and end locations exist.")
        print("- Use the 'Calculate best route' option to plan picking multiple items efficiently.")
        print("- The system includes a cycle in the graph to demonstrate non-trivial graph structures.")
        print("- 'Run Automated Tests' to check basic functionalities quickly.")

    def run_tests(self):
        print("\n--- Running Automated Tests ---")

        # Test shortest path from Entrance to A1 (should be 2)
        path, dist = self.warehouse.find_shortest_path('Entrance', 'A1')
        print("\nTest 1: Shortest path Entrance->A1")
        print("Expected Distance: 2")
        print(f"Calculated Route: {path if path else 'No route found'}")
        print(f"Calculated Distance: {dist}")
        if path and dist == 2:
            print("Result: PASS")
        else:
            print("Result: FAIL")

        # Test shortest path from A1 to Exit
        # Optimal route: A1 -> B1 -> B2 -> Exit = 2 + 1 + 3 = 6
        path, dist = self.warehouse.find_shortest_path('A1', 'Exit')
        print("\nTest 2: Shortest path A1->Exit")
        print("Expected Distance: 6")
        print(f"Calculated Route: {path if path else 'No route found'}")
        print(f"Calculated Distance: {dist}")
        if path and dist == 6:
            print("Result: PASS")
        else:
            print("Result: FAIL")

        # Test item retrieval route:
        # This test checks if any valid route is found and that the total distance > 0.
        route, total_dist = self.warehouse.get_item_route(['Item1', 'Item2', 'Item3'])
        print("\nTest 3: Multi-item retrieval (Item1, Item2, Item3)")
        print("Expected: A valid route and total distance > 0")
        print(f"Calculated Route: {route if route else 'No route found'}")
        print(f"Calculated Distance: {total_dist}")
        if route and total_dist > 0:
            print("Result: PASS")
        else:
            print("Result: FAIL")

        print("--- Automated Tests Completed ---")




if __name__ == "__main__":
    ui = UserInterface()
    ui.main_menu()
