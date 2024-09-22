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

    # Update the expiration date for a given vehicle
    def update_registration(self, license_plate, new_expiration_date):
        # Step 1: Remove the old registration entry
        removed = self.remove_registration(license_plate)
        if removed:
            # Step 2: Add the new registration with the updated expiration date
            self.add_registration(license_plate, new_expiration_date)
            print(f"Updated expiration date for {license_plate} to {new_expiration_date}.")
        else:
            print(f"Failed to update: License plate {license_plate} not found.")

    # Utility function to check the contents of the heap (for debugging)
    def print_heap(self):
        print("Current Expiration Heap:")
        for exp_date, plate in self.expiration_heap:
            print(f"License Plate: {plate}, Expiration Date: {exp_date.strftime('%Y-%m-%d')}")


# Testing the ExpirationHeap (Priority Queue) implementation

def test_expiration_heap():
    expiration_manager = ExpirationData()

    # Test Case 1: Add vehicle registrations with different expiration dates
    print("\n-- Test Case 1: Adding vehicle registrations --")
    expiration_manager.add_registration("ABC123", "2024-01-15")
    expiration_manager.add_registration("XYZ789", "2023-12-01")
    expiration_manager.add_registration("DEF456", "2024-03-10")
    expiration_manager.add_registration("LMN101", "2023-11-20")
    expiration_manager.print_heap()

    # Test Case 2: Get the next registration to expire
    print("\n-- Test Case 2: Getting the next registration to expire --")
    next_expiration = expiration_manager.get_next_expiration()
    if next_expiration:
        print(f"Next to expire: {next_expiration[1]} on {next_expiration[0].strftime('%Y-%m-%d')}")

    # Test Case 3: Remove the next registration to expire and verify the heap
    print("\n-- Test Case 3: Removing the next registration to expire --")
    expiration_manager.remove_next_expiration()
    expiration_manager.print_heap()  # Verify the heap after removal

    # Test Case 4: Remove a specific registration (valid case)
    print("\n-- Test Case 4: Removing a specific registration (DEF456) --")
    expiration_manager.remove_registration("DEF456")
    expiration_manager.print_heap()  # Verify the heap after removing specific registration

    # Test Case 5: Try to remove a non-existent registration
    print("\n-- Test Case 5: Trying to remove a non-existent registration (NONEXISTENT) --")
    expiration_manager.remove_registration("NONEXISTENT")

    # Test Case 6: Update expiration date for an existing registration
    print("\n-- est Case 6: Update registration (XYZ789) --")
    print("-- Update Registration 'XYZ789' --")
    expiration_manager.update_registration("XYZ789", "2024-05-01")
    expiration_manager.print_heap()

    # Update expiration date for a non-existent registration
    print("\n-- Attempt to Update Non-Existent Registration 'NON123' --")
    expiration_manager.update_registration("NON123", "2025-01-01")
    expiration_manager.print_heap()

    # Test Case 7: Edge Case - Remove from an empty heap
    print("\n-- Test Case 7: Removing from an empty heap --")
    # Emptying the heap by removing all elements
    expiration_manager.remove_next_expiration()  # Continue until empty
    expiration_manager.remove_next_expiration()  # Remove the last element
    expiration_manager.print_heap()  # Heap should now be empty
    next_expiration = expiration_manager.get_next_expiration()  # Try to get the next expiration
    if next_expiration is None:
        print("Heap is empty, no next expiration.")


# Running the test suite
if __name__ == "__main__":
    test_expiration_heap()
