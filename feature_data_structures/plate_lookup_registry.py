class CompressedTrieNode:
    def __init__(self):
        self.children = {}  # Child nodes (for each character)
        self.is_end_of_plate = False  # Indicates if a complete license plate ends here
        self.hash_map_suffix = {}  # Hash map for handling long suffixes

class CompressedTrie:
    def __init__(self):
        self.root = CompressedTrieNode()

    def insert(self, license_plate):
        """
        Insert a license plate into the compressed Trie.
        The first 3 characters are stored in the Trie, and the remaining are stored in a hash map.
        """
        if not license_plate:  # Ignore empty strings
            return

        node = self.root
        i = 0
        while i < len(license_plate):
            if i < 3:  # Use the Trie for the first 3 characters
                current_char = license_plate[i]
                if current_char not in node.children:
                    node.children[current_char] = CompressedTrieNode()
                node = node.children[current_char]
                i += 1
            else:
                # Use the hash map for the remaining part of the license plate
                suffix = license_plate[i:]
                if suffix not in node.hash_map_suffix:
                    node.hash_map_suffix[suffix] = True
                break
        node.is_end_of_plate = i == len(license_plate)  # Set end of plate only if we finished the plate

    def search(self, prefix):
        """
        Search for license plates starting with the given prefix.
        """
        if not prefix:  # Handle empty prefix case
            return []

        node = self.root
        i = 0
        result = []

        # Traverse the Trie for the first 3 characters
        while i < len(prefix) and i < 3:
            current_char = prefix[i]
            if current_char in node.children:
                node = node.children[current_char]
                i += 1
            else:
                return result  # Prefix not found

        # If the prefix length exceeds 3, check the hash map for suffixes
        if i == 3:
            for suffix in node.hash_map_suffix:
                if suffix.startswith(prefix[3:]):
                    result.append(prefix[:3] + suffix)

        # Perform DFS to collect all license plates starting from this node
        self._collect_plates(node, prefix[:i], result)

        return result

    # Delete a license plate from the Trie.
    def delete(self, license_plate):
        def _delete(node, plate, depth):
            if depth == len(plate):
                if node.is_end_of_plate:
                    node.is_end_of_plate = False
                return len(node.children) == 0 and len(node.hash_map_suffix) == 0

            current_char = plate[depth]

            # If depth reaches 3, check the hash map suffix
            if depth >= 3:
                suffix = plate[3:]
                if suffix in node.hash_map_suffix:
                    del node.hash_map_suffix[suffix]
                    return len(node.children) == 0 and len(node.hash_map_suffix) == 0
                return False

            if current_char not in node.children:
                return False

            should_delete_current_node = _delete(node.children[current_char], plate, depth + 1)

            if should_delete_current_node:
                del node.children[current_char]
                return len(node.children) == 0 and len(node.hash_map_suffix) == 0

            return False

        return _delete(self.root, license_plate, 0)

    # Helper function to collect all license plates from the current node.
    # Ensure no duplicates by avoiding adding from both Trie and hash map for the same plate.
    def _collect_plates(self, node, prefix, result):
        if node.is_end_of_plate and prefix not in result:
            result.append(prefix)

        # Collect plates in the Trie
        for char, child_node in node.children.items():
            self._collect_plates(child_node, prefix + char, result)

        # Collect plates from the hash map (ensure no duplicates)
        for suffix in node.hash_map_suffix:
            full_plate = prefix + suffix
            if full_plate not in result:  # Prevent duplicates
                result.append(full_plate)

    # Utility function to print the contents of the Trie for debugging.
    def print_trie(self):
        def _print(node, prefix):
            if node.is_end_of_plate:
                print(f"License plate: {prefix}")
            for char, child in node.children.items():
                _print(child, prefix + char)
            for suffix in node.hash_map_suffix:
                print(f"License plate: {prefix + suffix}")

        _print(self.root, "")


# Test suite for the Trie data structure for License Plate Prefix Lookups
# This is a test procedure following one function after the other
def test_trie():
    trie = CompressedTrie()

    # Test Case 1: Insert license plates into the Trie
    print("\n-- Test Case 1: Inserting license plates --")
    # Insert some license plates
    trie.insert("ABC123")
    trie.insert("ABC456")
    trie.insert("XYZ789")
    trie.insert("DEF123")
    trie.insert("ABX789")
    trie.insert("XYZ101")
    trie.insert("XYZ202")
    trie.insert("A1BCD7")
    trie.insert("A1B123")
    trie.insert("A1BXYZ")
    trie.insert("ABCDEF")
    trie.insert("ABC1EF")

    print("Inserted license plates.")
    # Print the Trie (for debugging)
    print("\n-- Initial Trie --")
    trie.print_trie()

    # Test Case 2: Search for license plates by prefix
    print("\n-- Test Case 2: Searching for license plates by prefix --")
    print("License plates starting with 'ABC':", trie.search("ABC"))
    print("License plates starting with 'A1B':", trie.search('A1B'))
    print("License plates starting with 'XYZ':", trie.search("XYZ"))
    print("License plates starting with 'A':", trie.search("A"))
    print("License plates starting with 'D':", trie.search("D"))
    print("License plates starting with 'XY':", trie.search("XY"))
    print("License plates starting with 'Z':", trie.search("Z"))  # Edge case: No matching prefix

    # Test Case 3: Edge case - Search for a non-existent prefix
    print("\n-- Test Case 3: Searching for a non-existent prefix --")
    print("License plates starting with 'NON':", trie.search("NON"))  # Edge case: Non-existent prefix

    # Test Case 4: Deleting specific license plates
    print("\n-- Test Case 4: Deleting specific license plates --")
    print("\n-- Deleting 'ABC123' --")
    trie.delete("ABC123")
    print("License plates starting with 'ABC123' after deletion:", trie.search("ABC123"))
    print("License plates starting with 'ABC' after deletion:", trie.search("ABC"))
    print("\n-- Deleting 'XYZ101' --")
    trie.delete("XYZ101")
    print("License plates starting with 'XYZ101' after deletion:", trie.search("XYZ101"))
    print("License plates starting with 'XYZ' after deletion:", trie.search("XYZ"))
    print("\n-- Delete 'A1BCD7' ---")
    trie.delete("A1BCD7")
    print("--- Search Results After Deletion ---")
    print("License plates starting with 'A1B' after deletion:", trie.search('A1B'), "\n")
    trie.print_trie()

    # Test Case 5: Edge case - Try to delete a license plate that doesn't exist
    print("\n-- Test Case 5: Deleting a non-existent license plate --")
    trie.delete("NONEXISTENT")
    print("Tried to delete 'NONEXISTENT'.")
    print("License plates starting with 'A' after attempting to delete non-existent plate:", trie.search("A"))
    trie.print_trie()

# Running the test suite
if __name__ == "__main__":
    test_trie()

