from objects.vehicle import Vehicle
from objects.owner import Owner

class VehicleRegistrationSystem:

    def __init__(self):

        # Make the Dictionary for storing all the vehicle registration details by number plate as key
        self.registrations = {}

    def add_vehicle(self, license_plate, vehicle:Vehicle, owner:Owner, registration_date, expiration_date):
        self.registrations[license_plate] = {
            'owner': {
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'license_number': owner.license_number,
            },
            'vehicle': {
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'color': vehicle.color,
                'classification': vehicle.classification,
                'vin_number': vehicle.vin_number,
            },
            'registration_date': registration_date,
            'expiration_date': expiration_date
        }

    def update_registration(self, license_plate,field, value ):
        # If license plate is not found return an error message
        if license_plate not in self.registrations:
            print(f"No vehicle found with license plate {license_plate}")
            return

        # Split the field path by periods (e.g., "owner.first_name")
        field_path = field.split(".")
        registration = self.registrations[license_plate]

        # Navigate through the nested dictionary to find the field to update
        target = registration
        for key in field_path[:-1]:  # Traverse to the second-to-last key
            if key in target:
                target = target[key]
            else:
                print(f"Field path '{field}' not found")
                return

        # Update the last field in the path
        last_key = field_path[-1]
        if last_key in target:
            target[last_key] = value
            print(f"Updated {field} to {value}")
        else:
            print(f"Field '{last_key}' not found in {field}")

    def get_registrations(self, license_plate):
        return self.registrations.get(license_plate, None)

    def remove_vehicle(self, license_plate):
        if license_plate in self.registrations:
            del self.registrations[license_plate]

# Test suite for the vehicle registration system implemented using a dictionary

def test_vehicle_registration_system():
    # Create the CarRegistrationSystem object
    car_system = VehicleRegistrationSystem()

    # Test Case 1: Adding vehicle registrations
    print("\n-- Test Case 1: Adding vehicle registrations --")
    vehicle_1 = Vehicle("Toyota", "Camry", 2020, "Blue", "Sedan", "123456789")
    owner_1 = Owner("John", "Doe", "DL12345")
    car_system.add_vehicle("ABC123", vehicle_1, owner_1, "2023-01-01", "2024-01-01")

    vehicle_2 = Vehicle("Honda", "Civic", 2019, "Red", "Sedan", "987654321")
    owner_2 = Owner("Jane", "Doe", "DL67890")
    car_system.add_vehicle("XYZ789", vehicle_2, owner_2, "2022-06-15", "2023-06-15")

    car_system.add_vehicle("LMN456", vehicle_1, owner_1, "2023-04-01", "2024-04-01")  # Another vehicle for the same owner
    print(car_system.registrations)  # Print the current registrations to verify

    # Test Case 2: Retrieving vehicle registration by license plate
    print("\n-- Test Case 2: Retrieving vehicle registration by license plate --")
    print(f"Registration for 'ABC123': {car_system.get_registrations('ABC123')}")
    print(f"Registration for 'XYZ789': {car_system.get_registrations('XYZ789')}")
    print(f"Registration for 'NONEXISTENT': {car_system.get_registrations('NONEXISTENT')}")  # Edge case: Non-existent license plate

    # Test Case 3: Updating specific fields in a vehicle registration
    print("\n-- Test Case 3: Updating specific fields in a vehicle registration --")
    car_system.update_registration("ABC123", "owner.first_name", "Alice")  # Update owner first name
    car_system.update_registration("XYZ789", "vehicle.color", "Green")  # Update vehicle color
    car_system.update_registration("LMN456", "expiration_date", "2025-04-01")  # Update expiration date
    car_system.update_registration("XYZ789", "vehicle.invalid_field", "Value")  # Edge case: Invalid field
    print(car_system.registrations)  # Verify updates

    # Test Case 4: Removing a vehicle registration by license plate
    print("\n-- Test Case 4: Removing a vehicle registration --")
    car_system.remove_vehicle("ABC123")  # Remove existing registration
    print(car_system.registrations)  # Verify removal
    car_system.remove_vehicle("NONEXISTENT")  # Edge case: Try to remove non-existent registration

    # Test Case 5: Edge case - Adding a duplicate license plate
    print("\n-- Test Case 5: Adding a duplicate license plate --")
    car_system.add_vehicle("XYZ789", vehicle_2, owner_2, "2022-06-15", "2023-06-15")  # Attempt to re-add XYZ789
    print(car_system.registrations)

# Running the test suite
if __name__ == "__main__":
    test_vehicle_registration_system()
