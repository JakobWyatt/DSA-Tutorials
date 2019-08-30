from DSABinarySearchTree import DSABinarySearchTree

def treeMenu():
    options = {
        1: (readCsvMenu, "Read a csv file into a tree."),
        2: (readSerializedMenu, "Read a serialized file into a tree."),
        3: (displayMenu, "Display the tree."),
        4: (writeCsvMenu, "Write a tree to a csv file."),
        5: (writeSerializedMenu, "Write a tree to a serialized file."),
        6: (None, "Exit the menu.")
    }
    picked = 0
    tree = DSABinarySearchTree()
    while picked != 6:
        print("Enter an option from the menu:")
        for k, v in options.items():
            print(f"{k}: {v[1]}")
        try:
            picked = int(input())
            action = options[picked][0]
            if action != None:
                tree = action(tree)
        except (ValueError, KeyError):
            print("Please enter a valid menu option.")

def readCsvMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    print("File name: ")
    filename = str(input())
    tree = DSABinarySearchTree()
    try:
        with open(filename, 'r') as f:
            for x in f:
                arr = x.rstrip('\n').split(',')
                try:
                    tree.insert(arr[0], arr[1:])
                except ValueError:
                    print("Key already exists.")
    except FileNotFoundError:
        print("File does not exist.")
    return tree

def readSerializedMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    ...

def displayMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    DSABinarySearchTree.render(tree.display(), type='pdf')
    return tree

def writeCsvMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    print("Traversal method:")
    options = {
        1: (tree.preorder, "Preorder"),
        2: (tree.inorder, "Inorder"),
        3: (tree.postorder, "Postorder")
    }
    for k, v in options.items():
        print(f"{k}: {v[1]}")
    try:
        traversal = options[int(input())][0]
    except (ValueError, KeyError):
        print("Please enter a valid menu option.")
    print("File name: ")
    try:
        with open(str(input()), 'w') as f:
            for x in traversal():
                f.write("{key},{value}\n"
                    .format(key=x.key, value=",".join(x.value)))
    except IOError:
        print("Error occured while writing the file.")
    return tree

def writeSerializedMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    ...

if __name__ == "__main__":
    treeMenu()
