from DSABinarySearchTree import DSABinarySearchTree
import pickle

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
    except IOError:
        print("File could not be read.")
    return tree

def readSerializedMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    print("File name: ")
    try:
        with open(str(input()), 'rb') as f:
            tree = pickle.load(f)
    except FileNotFoundError:
        print("File does not exist.")
    except IOError:
        print("File could not be read.")
    return tree

def displayMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    try:
        DSABinarySearchTree.render(tree.display(), type='pdf')
    except RuntimeError as err:
        print(str(err))
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
        print("File name: ")
        with open(str(input()), 'w') as f:
            for x in traversal():
                f.write("{key}{value}\n"
                    .format(key=x.key, value="".join([f',{v}' for v in x.value])))
    except (ValueError, KeyError):
        print("Please enter a valid menu option.")
    except IOError:
        print("Error occured while writing the file.")
    return tree

def writeSerializedMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    print("File name: ")
    try:
        with open(str(input()), 'wb') as f:
            pickle.dump(tree, f)
    except IOError:
        print("Error occured while writing the file.")
    return tree

if __name__ == "__main__":
    treeMenu()
