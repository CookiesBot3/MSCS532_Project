# This will be the main system that runs the whole application

from objects.vehicle import Vehicle
from objects.owner import Owner

from feature_data_structures.vehicle_registration_system import VehicleRegistrationSystem
from feature_data_structures.expiration_data import ExpirationData
from feature_data_structures.plate_lookup_registry import Trie
from feature_data_structures.owner_based_car_registration import AVLTree

def menu_page():
    pass

if __name__ == '__main__':
    menu_page()