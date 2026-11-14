tree = {
    "S": [
        {"C": ["1"]},
        {"S": [
            {"C": ["2"]},
            {"S": [
                {"C": ["3"]},
                {"S": [
                    {"E": ["4"]}
                ]}
            ]}
        ]}
    ]
}

def print_tree(node, depth=0):
    indent = "    " * depth
    if isinstance(node, str):
        print(f"{indent}|-- {node}")
    elif isinstance(node, dict):
        for key, children in node.items():
            print(f"{indent}|-- {key}")
            for child in children:
                print_tree(child, depth + 1)

if __name__ == "__main__":
    print("Завдання 6. Дерево виведення для слова w = 1234")
    print_tree(tree)