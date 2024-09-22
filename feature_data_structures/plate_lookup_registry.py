class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to hold child nodes (one for each character)
        self.is_end_of_plate = False  # True if the node represents the end of a valid license plate
        self.plates = []  # List of full license plates that pass through this node


class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Insert a license plate into the Trie
    def insert(self, license_plate):
        node = self.root
        for char in license_plate:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.plates.append(license_plate)  # Add the license plate to the list at this node
        node.is_end_of_plate = True  # Mark the end of a valid license plate

    # Search for license plates that match a given prefix
    def search_by_prefix(self, prefix):
        node = self.root
        # Traverse the Trie according to the given prefix
        for char in prefix:
            if char not in node.children:
                return []  # Prefix not found
            node = node.children[char]
        # Return all plates that start with the given prefix
        return node.plates

    # Delete a license plate from the Trie
    def delete(self, license_plate):
        # Helper function to recursively delete nodes
        def _delete(node, plate, depth):
            if depth == len(plate):
                if not node.is_end_of_plate:
                    return False  # License plate not present
                node.is_end_of_plate = False  # Unmark the end of the plate
                if plate in node.plates:
                    node.plates.remove(plate)  # Remove the plate from the node's list
                return len(node.children) == 0  # If no children, node can be deleted

            char = plate[depth]
            if char not in node.children:
                return False  # Plate not found

            should_delete_current_node = _delete(node.children[char], plate, depth + 1)

            # Remove the license plate from the current node's plates list
            if plate in node.plates:
                node.plates.remove(plate)

            # If the recursive call says to delete the child, do it
            if should_delete_current_node:
                del node.children[char]
                # Return true if the current node has no other children and isn't the end of another plate
                return len(node.children) == 0 and not node.is_end_of_plate

            return False

        return _delete(self.root, license_plate, 0)

    # Utility function to print the Trie (for debugging)
    def print_trie(self, node=None, prefix=""):
        if node is None:
            node = self.root
        if node.is_end_of_plate:
            print(f"Prefix: {prefix}, Plates: {node.plates}")
        for char, child in node.children.items():
            self.print_trie(child, prefix + char)

# Test suite for the Trie data structure for License Plate Prefix Lookups
# This is a test procedure following one function after the other
def test_trie():
    trie = Trie()

    # Test Case 1: Insert license plates into the Trie
    print("\n-- Test Case 1: Inserting license plates --")
    trie.insert("ABC123")
    trie.insert("ABC456")
    trie.insert("XYZ789")
    trie.insert("DEF123")
    trie.insert("ABX789")
    trie.insert("XYZ101")
    trie.insert("XYZ202")
    print("Inserted license plates.")
    # Print the Trie (for debugging)
    print("\n-- Initial Trie --")
    trie.print_trie()

    # Test Case 2: Search for license plates by prefix
    print("\n-- Test Case 2: Searching for license plates by prefix --")
    print("License plates starting with 'ABC':", trie.search_by_prefix("ABC"))
    print("License plates starting with 'XYZ':", trie.search_by_prefix("XYZ"))
    print("License plates starting with 'A':", trie.search_by_prefix("A"))
    print("License plates starting with 'D':", trie.search_by_prefix("D"))
    print("License plates starting with 'XY':", trie.search_by_prefix("XY"))
    print("License plates starting with 'Z':", trie.search_by_prefix("Z"))  # Edge case: No matching prefix

    # Test Case 3: Edge case - Search for a non-existent prefix
    print("\n-- Test Case 3: Searching for a non-existent prefix --")
    print("License plates starting with 'NON':", trie.search_by_prefix("NON"))  # Edge case: Non-existent prefix

    # Test Case 4: Deleting specific license plates
    print("\n-- Test Case 4: Deleting specific license plates --")
    print("-- Deleting 'ABC123' --")
    trie.delete("ABC123")
    print("Deleted 'ABC123'.")
    print("License plates starting with 'ABC123' after deletion:", trie.search_by_prefix("ABC123"))
    print("License plates starting with 'ABC' after deletion:", trie.search_by_prefix("ABC"))
    print("-- Deleting 'XYZ101' --")
    trie.delete("XYZ101")
    print("License plates starting with 'XYZ101' after deletion:", trie.search_by_prefix("XYZ101"))
    print("License plates starting with 'XYZ' after deletion:", trie.search_by_prefix("XYZ"))
    trie.print_trie()

    # Test Case 5: Edge case - Try to delete a license plate that doesn't exist
    print("\n-- Test Case 5: Deleting a non-existent license plate --")
    trie.delete("NONEXISTENT")
    print("Tried to delete 'NONEXISTENT'.")
    print("License plates starting with 'A' after attempting to delete non-existent plate:", trie.search_by_prefix("A"))
    trie.print_trie()

# Running the test suite
if __name__ == "__main__":
    test_trie()

