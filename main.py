# This will be the main system that runs the whole application
from datetime import datetime
from objects.vehicle import Vehicle
from objects.owner import Owner

from feature_data_structures.vehicle_registration_system import VehicleRegistrationSystem
from feature_data_structures.expiration_data import ExpirationData
from feature_data_structures.plate_lookup_registry import CompressedTrie
from feature_data_structures.owner_based_car_registration import AVLTree

def main_menu():
    print("\n---- Vehicle Registration System ----")
    print("1. Add Vehicle Registration")
    print("2. Search by License Plate Prefix")
    print("3. Search Vehicle Details by License Plate")
    print("4. Update Vehicle Expiration Date")
    print("5. Remove Vehicle Registration")
    print("6. Get Next Expiring Vehicle")
    print("7. Display All Registrations")
    print("8. Find Vehicles by Driver's License")
    print("9. Exit")
    return input("Enter your choice: ")

# We need to add all the details when a new vehicle is added.
def add_vehicle(trie, heap, car_system, avl_tree):
    print("\n---- Add Vehicle Registration ----")
    license_plate = input("Enter license plate: ")
    make = input("Enter vehicle make: ")
    model = input("Enter vehicle model: ")

    # Input validation for vehicle year (only numeric and within a valid range)
    def get_valid_year(prompt):
        while True:
            year = input(prompt)
            if year.isdigit() and 1886 <= int(year) <= datetime.now().year:  # First car invented in 1886
                return int(year)
            else:
                print(f"Invalid input. Please enter a valid year between 1886 and {datetime.now().year}.")

    year = get_valid_year("Enter vehicle year: ")

    # Input validation for first name and last name
    def get_valid_alpha(prompt, field_name):
        while True:
            text = input(prompt)
            if text.isalpha():
                return text
            else:
                print("Invalid input. Please enter only alphabetic characters for the " + field_name)

    color = get_valid_alpha("Enter vehicle color: ", "color.")
    classification = get_valid_alpha("Enter vehicle classification: ", "classification")

    # Input validation for VIN number (only numeric characters)
    def get_valid_digit(prompt):
        while True:
            vin = input(prompt)
            if vin.isdigit():
                return vin
            else:
                print("Invalid input. Please enter only numeric characters for the VIN number.")

    vin_number = get_valid_digit("Enter vehicle VIN number: ")

    print("\n---- Enter Owner Registration ----")
    first_name = get_valid_alpha("Enter owner's first name: ", "first name.")
    last_name = get_valid_alpha("Enter owner's last name: ", "last name.")

    license_number = input("Enter owner's license number: ")

    # Input validation for date format
    def get_valid_date(prompt):
        while True:
            date = input(prompt)
            try:
                # Try to parse the date in YYYY-MM-DD format
                datetime.strptime(date, "%Y-%m-%d")
                return date
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    print("\n---- Registration Details ----")
    registration_date = get_valid_date("Enter registration date (YYYY-MM-DD): ")
    expiration_date = get_valid_date("Enter expiration date (YYYY-MM-DD): ")

    vehicle = Vehicle(make, model, year, color, classification, vin_number)
    owner = Owner(first_name, last_name, license_number)

    car_system.add_vehicle(license_plate, vehicle, owner, registration_date, expiration_date)
    trie.insert(license_plate)
    heap.add_registration(license_plate, expiration_date)
    avl_tree.root = avl_tree.insert(avl_tree.root, license_number, f"{first_name} {last_name}", license_plate)  # Insert into AVL Tree

    print(f"Vehicle registration added for {license_plate}.")


def search_by_prefix(trie):
    print("\n---- Search by License Plate Prefix ----")
    prefix = input("Enter the license plate prefix: ")
    result = trie.search(prefix)
    if result:
        print(f"License plates starting with '{prefix}': {result}")
    else:
        print(f"No license plates found with prefix '{prefix}'.")

def search_by_plate(car_system):
    print("\n---- Search Registration by License Plate  ----")
    plate = input("Enter the license plate to retrieve full detail: ")
    print("")
    car_system.get_registrations(plate)


def update_expiration_date(heap, car_system):
    print("\n---- Update Vehicle Expiration Date ----")
    license_plate = input("Enter license plate to update: ")
    new_expiration_date = input("Enter new expiration date (YYYY-MM-DD): ")

    car_system.update_registration(license_plate, "expiration_date", new_expiration_date)
    heap.remove_registration(license_plate)  # Remove old expiration date
    heap.add_registration(license_plate, new_expiration_date)  # Add updated expiration date

    print(f"Expiration date updated for {license_plate}.")


def remove_vehicle(trie, heap, car_system, avl_tree):
    print("\n---- Remove Vehicle Registration ----")
    license_plate = input("Enter license plate to remove: ")

    # Get owner information to remove from AVL tree
    vehicle_info = car_system.get_registrations(license_plate)
    if vehicle_info:
        license_number = vehicle_info['owner']['license_number']
        avl_tree.root = avl_tree.remove(avl_tree.root, license_number, license_plate)  # Remove from AVL Tree

    car_system.remove_vehicle(license_plate)
    trie.delete(license_plate)
    heap.remove_registration(license_plate)

    print(f"Vehicle registration removed for {license_plate}.")

def get_next_expiring_vehicle(heap):
    print("\n---- Next Expiring Vehicle ----")
    next_exp = heap.get_next_expiration()
    if next_exp:
        expiration_date, license_plate = next_exp
        print(f"Next expiring vehicle: {license_plate}, Expiration Date: {expiration_date.strftime('%Y-%m-%d')}")
    else:
        print("No vehicles in the system.")

def display_all_registrations(car_system):
    print("\n---- Display All Vehicle Registrations ----")
    # for license_plate, details in car_system.registrations.items():
    #     print(f"License Plate: {license_plate}, Details: {details}")
    car_system.display_all_registrations()

def find_vehicles_by_license(avl_tree):
    print("\n---- Find Vehicles by Driver's License ----")
    license_number = input("Enter driver's license number: ")
    result = avl_tree.find_vehicles_by_dl(avl_tree.root, license_number)

    if result:
        print(f"Vehicles owned by driver with license number '{license_number}': {result}")
    else:
        print(f"No vehicles found for driver's license number '{license_number}'.")

if __name__ == '__main__':
    car_system = VehicleRegistrationSystem()
    trie = CompressedTrie()
    heap = ExpirationData()
    avl_tree = AVLTree()

    while True:
        choice = main_menu()

        if choice == '1':
            add_vehicle(trie, heap, car_system, avl_tree)
        elif choice == '2':
            search_by_prefix(trie)
        elif choice == '3':
            search_by_plate(car_system)
        elif choice == '4':
            update_expiration_date(heap, car_system)
        elif choice == '5':
            remove_vehicle(trie, heap, car_system, avl_tree)
        elif choice == '6':
            get_next_expiring_vehicle(heap)
        elif choice == '7':
            display_all_registrations(car_system)
        elif choice == '8':
            find_vehicles_by_license(avl_tree)
        elif choice == '9':
            print("Exiting system...")
            break
        else:
            print("Invalid choice, please try again.")