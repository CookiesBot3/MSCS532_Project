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

    # Delete a license plate from the Trie (optional functionality, complex)
    def delete(self, license_plate):
        # Helper function to recursively delete nodes
        def _delete(node, plate, depth):
            if depth == len(plate):
                if not node.is_end_of_plate:
                    return False  # License plate not present
                node.is_end_of_plate = False
                return len(node.children) == 0  # If no children, node can be deleted
            char = plate[depth]
            if char not in node.children:
                return False
            should_delete_current_node = _delete(node.children[char], plate, depth + 1)
            if should_delete_current_node:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_plate
            return False

        _delete(self.root, license_plate, 0)