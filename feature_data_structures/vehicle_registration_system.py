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