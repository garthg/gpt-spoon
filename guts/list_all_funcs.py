import ast
import os

def extract_top_level_functions(filename):
    top_level_functions = set()

    with open(filename, 'r') as file:
        tree = ast.parse(file.read(), filename=filename)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not hasattr(node, "parent"):
            top_level_functions.add(node.name)

    return top_level_functions

def get_top_level_functions(folder_path):
    functions_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                top_level_functions = extract_top_level_functions(file_path)
                for function in top_level_functions:
                    functions_list.append((file, function))

    return functions_list

if __name__ == "__main__":
    folder_path = "/path/to/your/folder"  # Replace with the path to your folder
    top_level_functions_list = get_top_level_functions(folder_path)

    print("List of top-level functions:")
    for file, function in top_level_functions_list:
        print(f"File: {file}, Function: {function}")
