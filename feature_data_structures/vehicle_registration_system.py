from objects.vehicle import Vehicle
from objects.owner import Owner
from functools import lru_cache

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
        # Clear the cache after adding a new vehicle to ensure cache consistency
        self.get_registrations.cache_clear()

    def update_registration(self, license_plate,field, value ):
        if license_plate in self.registrations:
            if field in self.registrations[license_plate]['vehicle']:
                self.registrations[license_plate]['vehicle'][field] = value
            elif field in self.registrations[license_plate]['owner']:
                self.registrations[license_plate]['owner'][field] = value
            elif field in ['registration_date', 'expiration_date']:
                self.registrations[license_plate][field] = value
            else:
                print(f"Invalid field: {field}")

            # Clear the cache after updating the registration
            self.get_registrations.cache_clear()
        else:
            print(f"Vehicle with license plate {license_plate} not found.")

    @lru_cache(maxsize=100)  # Cache for storing frequently accessed vehicle records (most recent 100 lookups)
    def get_registrations(self, license_plate):
        return self.registrations.get(license_plate, None)

    def remove_vehicle(self, license_plate):
        if license_plate in self.registrations:
            del self.registrations[license_plate]
            self.get_registrations.cache_clear()
        else:
            print(f"Vehicle with license plate {license_plate} not found.")

    def display_all_registrations(self):
        """
        Display all vehicle registrations in the system.
        """
        for license_plate, details in self.registrations.items():
            print(f"License Plate: {license_plate}")
            print(f"Owner: \n\tFirst name: {details['owner']['first_name']}"
                  f"\n\tLast name: {details['owner']['last_name']}"
                  f"\n\tLicense number: {details['owner']['license_number']}")
            print(f"Vehicle: "
                  f"\n\tMake: {details['vehicle']['make']}"
                  f"\n\tModel: {details['vehicle']['model']}"
                  f"\n\tYear: {details['vehicle']['year']}"
                  f"\n\tColor: {details['vehicle']['color']}"
                  f"\n\tClassification: {details['vehicle']['classification']}"
                  f"\n\tVin Number: {details['vehicle']['vin_number']}")
            print(f"Registration Date: {details['registration_date']}")
            print(f"Expiration Date: {details['expiration_date']}\n")

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
    car_system.display_all_registrations()  # Print the current registrations to verify

    # Test Case 2: Retrieving vehicle registration by license plate
    print("\n-- Test Case 2: Retrieving vehicle registration by license plate --")
    print(f"Registration for 'ABC123': {car_system.get_registrations('ABC123')}")
    print(f"Registration for 'XYZ789': {car_system.get_registrations('XYZ789')}")
    print(f"Registration for 'NONEXISTENT': {car_system.get_registrations('NONEXISTENT')}")  # Edge case: Non-existent license plate

    # Test Case 3: Updating specific fields in a vehicle registration
    print("\n-- Test Case 3: Updating specific fields in a vehicle registration --")
    car_system.update_registration("ABC123", "first_name", "Alice")  # Update owner first name
    car_system.update_registration("XYZ789", "color", "Green")  # Update vehicle color
    car_system.update_registration("LMN456", "expiration_date", "2025-04-01")  # Update expiration date
    car_system.display_all_registrations()  # Verify updates
    car_system.update_registration("XYZ789", "invalid_field", "Value")  # Edge case: Invalid field

    # Test Case 4: Removing a vehicle registration by license plate
    print("\n-- Test Case 4: Removing a vehicle registration --")
    car_system.remove_vehicle("ABC123")  # Remove existing registration
    car_system.display_all_registrations()  # Verify removal
    car_system.remove_vehicle("NONEXISTENT")  # Edge case: Try to remove non-existent registration

    # Test Case 5: Edge case - Adding a duplicate license plate
    print("\n-- Test Case 5: Adding a duplicate license plate --")
    car_system.add_vehicle("XYZ789", vehicle_2, owner_2, "2022-06-15", "2023-06-15")  # Attempt to re-add XYZ789
    car_system.display_all_registrations()

# Running the test suite
if __name__ == "__main__":
    test_vehicle_registration_system()
