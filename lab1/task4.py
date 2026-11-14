alphabet = set(str(i) for i in range(10))
V = {"S", "C", "E"}
T = alphabet.copy()
start_symbol = "S"
P = {
    "S": [["C", "S"], ["E"]],
    "C": [[str(i)] for i in range(10)],
    "E": [["0"], ["2"], ["4"], ["6"], ["8"]]
}


def check_grammar():
    if V & T:
        return False, "V і T перетинаються"
    if start_symbol not in V:
        return False, "S не належить V"

    V_union_T = V | T
    for left, rights in P.items():
        if left not in V_union_T:
            return False, f"Символ {left} не в V ∪ T"
        for right in rights:
            for symbol in right:
                if symbol not in V_union_T:
                    return False, f"Символ {symbol} не в V ∪ T"
    return True, "Граматика коректна"


if __name__ == "__main__":
    print("Завдання 4. Граматика")
    for left, rights in P.items():
        rhs = " | ".join("".join(r) for r in rights)
        print(f"{left} -> {rhs}")

    is_valid, msg = check_grammar()
    print(f"Перевірка: {msg}")