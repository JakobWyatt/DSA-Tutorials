import os
import errno
import pickle
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
        # Print menu options
        print("\nEnter an option from the menu:")
        for k, v in options.items():
            print(f"{k}: {v[1]}")

        try:
            # Pick which action to take and execute the corresponding function
            picked = int(input())
            action = options[picked][0]
            if action is not None:
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
                # For each line, split it by comma.
                # Store the first element as the key
                # and all other elements as the values.
                arr = x.rstrip('\n').split(',')
                try:
                    tree.insert(arr[0], arr[1:])
                except ValueError as ex:
                    print(ex)
    except IOError as ioex:
        print(f"File could not be read: {os.strerror(ioex.errno)}")
    except ValueError as valErr:
        print(f"Invalid file format: {valErr}")
    return tree


def readSerializedMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    print("File name: ")
    try:
        with open(str(input()), 'rb') as f:
            tree = pickle.load(f)
    except IOError as ex:
        print(f"File could not be read: {os.strerror(ex.errno)}")
    except Exception as ex:
        print(f"Reading pickled object failed: {ex}")
    return tree


def displayMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    try:
        # Render as a pdf, as default svg rendering breaks for large trees.
        DSABinarySearchTree.render(tree.display(), type='pdf')
    except RuntimeError as err:
        print(err)
    return tree


def writeCsvMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    # Print all options.
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
                # When there are no elements in the value array,
                # do not print a trailing comma. This allows files
                # to be written as they were read originally.
                f.write("{key}{value}\n"
                        .format(key=x.key,
                                value="".join([f',{v}' for v in x.value])))
    except (ValueError, KeyError):
        print("Please enter a valid menu option.")
    except IOError as ex:
        print(f"File could not be written: {os.strerror(ex.errno)}")
    return tree


def writeSerializedMenu(tree: DSABinarySearchTree) -> DSABinarySearchTree:
    print("File name: ")
    try:
        with open(str(input()), 'wb') as f:
            pickle.dump(tree, f)
    except IOError as ex:
        print(f"File could not be written: {os.strerror(ex.errno)}")
    return tree


if __name__ == "__main__":
    treeMenu()
