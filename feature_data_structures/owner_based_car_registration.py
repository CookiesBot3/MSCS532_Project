class Node:
    def __init__(self, dl_numbers, owner_name, license_plate):
        self.dl_numbers = dl_numbers  # Driver's License Number (unique key)
        self.owner_name = owner_name
        self.vehicles = [license_plate]  # Store a list of vehicles (license plates) under the owner
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    # Get the height of a node
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    # Get the balance factor of a node
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Right rotate subtree rooted with y
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        # Perform rotation
        x.right = y
        y.left = T2
        # Update heights
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        return x

    # Left rotate subtree rooted with x
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        # Perform rotation
        y.left = x
        x.right = T2
        # Update heights
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        return y

    # Insert a vehicle into the AVL tree based on dl_numbers (driver’s license number)
    def insert(self, root, dl_numbers, owner_name, license_plate):
        # Step 1: Perform normal BST insertion
        if not root:
            return Node(dl_numbers, owner_name, license_plate)

        if dl_numbers < root.dl_numbers:
            root.left = self.insert(root.left, dl_numbers, owner_name, license_plate)
        elif dl_numbers > root.dl_numbers:
            root.right = self.insert(root.right, dl_numbers, owner_name, license_plate)
        else:
            # If the owner with the same dl_numbers already exists, add the vehicle to their list
            root.vehicles.append(license_plate)
            return root

        # Step 2: Update the height of the ancestor node
        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1

        # Step 3: Get the balance factor to check if this node became unbalanced
        balance = self.get_balance(root)

        # Step 4: If the node is unbalanced, then apply rotations

        # Left Left Case
        if balance > 1 and dl_numbers < root.left.dl_numbers:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and dl_numbers > root.right.dl_numbers:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and dl_numbers > root.left.dl_numbers:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and dl_numbers < root.right.dl_numbers:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        # Return the (unchanged) node pointer
        return root

    # Remove a license plate for a specific driver's license
    def remove(self, root, dl_number, license_plate):
        if not root:
            return root

        if dl_number < root.dl_numbers:
            root.left = self.remove(root.left, dl_number, license_plate)
        elif dl_number > root.dl_numbers:
            root.right = self.remove(root.right, dl_number, license_plate)
        else:
            # If we found the driver's license node, remove the vehicle from the list
            if license_plate in root.vehicles:
                root.vehicles.remove(license_plate)

            # If no vehicles remain, we delete the node
            if not root.vehicles:
                if not root.left:
                    return root.right
                elif not root.right:
                    return root.left

                # If the node has two children, get the inorder successor (smallest in the right subtree)
                temp = self.get_min_value_node(root.right)
                root.dl_numbers = temp.dl_numbers
                root.vehicles = temp.vehicles
                root.right = self.remove(root.right, temp.dl_numbers, license_plate)

        # If the node had children, we need to update its height and balance the tree
        if root is None:
            return root

        root.height = max(self.get_height(root.left), self.get_height(root.right)) + 1

        balance = self.get_balance(root)

        # Balancing
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Utility function to get the node with the smallest value in a subtree
    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    # Find vehicles by driver's license number
    def find_vehicles_by_dl(self, root, dl_numbers):
        if not root:
            return None

        if dl_numbers < root.dl_numbers:
            return self.find_vehicles_by_dl(root.left, dl_numbers)
        elif dl_numbers > root.dl_numbers:
            return self.find_vehicles_by_dl(root.right, dl_numbers)
        else:
            return {'owner_name': root.owner_name, 'vehicles': root.vehicles}

    # Utility function to print the tree (for debugging)
    def pre_order(self, root):
        if not root:
            return
        print(f"DL Number: {root.dl_numbers}, Owner: {root.owner_name}, Vehicles: {root.vehicles}")
        self.pre_order(root.left)
        self.pre_order(root.right)

def testcases_avl_tree():
    # Initialize the AVL tree
    avl_tree = AVLTree()
    root = None

    # Test Case 1: Insert vehicles for different owners
    print("\n-- Test Case 1: Inserting vehicles for multiple owners --")
    root = avl_tree.insert(root, "DL12345", "Alice", "ABC123")
    root = avl_tree.insert(root, "DL67890", "Bob", "XYZ789")
    root = avl_tree.insert(root, "DL54321", "Charlie", "GHI012")
    avl_tree.pre_order(root)  # Print the tree structure

    # Test Case 2: Insert multiple vehicles for the same owner (with repeated dl_numbers)
    print("\n-- Test Case 2: Inserting multiple vehicles for the same owner --")
    root = avl_tree.insert(root, "DL12345", "Alice", "DEF456")  # Adding another vehicle for Alice
    root = avl_tree.insert(root, "DL67890", "Bob", "UVW345")    # Adding another vehicle for Bob
    avl_tree.pre_order(root)  # Print the tree structure

    # Test Case 3: Search for vehicles owned by a specific driver (using dl_numbers)
    print("\n-- Test Case 3: Searching for vehicles by driver's license number --")
    print("Vehicles for DL12345 (Alice):", avl_tree.find_vehicles_by_dl(root, "DL12345"))
    print("Vehicles for DL67890 (Bob):", avl_tree.find_vehicles_by_dl(root, "DL67890"))
    print("Vehicles for DL54321 (Charlie):", avl_tree.find_vehicles_by_dl(root, "DL54321"))

    # Test Case 4: Edge case - Search for a non-existent driver's license number
    print("\n-- Test Case 4: Searching for a non-existent driver's license number --")
    print("Vehicles for DL99999 (non-existent):", avl_tree.find_vehicles_by_dl(root, "DL99999"))

    # Test Case 5: Remove a license plate
    print("\n-- Test Case 5: Remove a license plate --")
    print("Vehicles for DL12345 (Alice): remove(DEF456)")
    avl_tree.remove(root, "DL12345", "DEF456")
    avl_tree.pre_order(root)  # Print the tree structure

    # Test Case 6: Insert into an empty AVL tree (Edge case)
    print("\n-- Test Case 6: Inserting into an empty AVL tree --")
    empty_tree_root = None
    empty_tree_root = avl_tree.insert(empty_tree_root, "DL11111", "Eve", "LMN345")
    avl_tree.pre_order(empty_tree_root)  # Should only show Eve's data

# Running the test suite
if __name__ == "__main__":
    testcases_avl_tree()