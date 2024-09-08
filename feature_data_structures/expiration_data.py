import heapq
from datetime import datetime

class ExpirationData:
    def __init__(self):
        # Min-heap to store (expiration_date, license_plate) tuples
        self.expiration_heap = []

    # Add a vehicle's expiration date and license plate to the heap
    def add_registration(self, license_plate, expiration_date):
        expiration_datetime = datetime.strptime(expiration_date, "%Y-%m-%d")
        heapq.heappush(self.expiration_heap, (expiration_datetime, license_plate))
        print(f"Added {license_plate} with expiration date {expiration_date} to the heap.")

    # Get the next vehicle registration to expire (without removing it)
    def get_next_expiration(self):
        if not self.expiration_heap:
            return None
        return self.expiration_heap[0]  # Peek at the smallest element (earliest expiration date)

    # Remove the next vehicle registration to expire from the heap
    def remove_next_expiration(self):
        if not self.expiration_heap:
            return None
        next_expiration = heapq.heappop(self.expiration_heap)  # Pop the smallest element
        print(f"Removed {next_expiration[1]} with expiration date {next_expiration[0]} from the heap.")
        return next_expiration

    # Remove a specific vehicle's registration from the heap (if needed)
    def remove_registration(self, license_plate):
        for i, (exp_date, plate) in enumerate(self.expiration_heap):
            if plate == license_plate:
                del self.expiration_heap[i]
                heapq.heapify(self.expiration_heap)
                print(f"Removed registration for {license_plate}.")
                return True
        print(f"License plate {license_plate} not found in the heap.")
        return False

    # Utility function to check the contents of the heap (for debugging)
    def print_heap(self):
        print("Current Expiration Heap:")
        for exp_date, plate in self.expiration_heap:
            print(f"License Plate: {plate}, Expiration Date: {exp_date.strftime('%Y-%m-%d')}")