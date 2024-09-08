class Node:
    # Owner name will be first name + last name
    def __init__(self, dl_numbers, owner_name, license_plate):
        self.dl_numbers = dl_numbers
        self.owner_name = owner_name
        self.vehicles = [license_plate]
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

    # Find all vehicles registered to a specific owner using their driver's license number (dl_numbers)
    def find_vehicles_by_dl(self, root, dl_numbers):
        if not root:
            return None

        if dl_numbers < root.dl_numbers:
            return self.find_vehicles_by_dl(root.left, dl_numbers)
        elif dl_numbers > root.dl_numbers:
            return self.find_vehicles_by_dl(root.right, dl_numbers)
        else:
            # Owner found, return the list of vehicles
            return {
                'owner_name': root.owner_name,
                'vehicles': root.vehicles
            }

    # Utility function to print the tree (for debugging)
    def pre_order(self, root):
        if not root:
            return
        print(f"DL Number: {root.dl_numbers}, Owner: {root.owner_name}, Vehicles: {root.vehicles}")
        self.pre_order(root.left)
        self.pre_order(root.right)