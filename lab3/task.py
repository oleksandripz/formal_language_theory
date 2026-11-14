from collections import deque

def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for nxt in transitions.get((state, ""), set()):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure

def format_state(subset):
    if not subset:
        return "∅"
    return "{" + ",".join(sorted(subset)) + "}"

def nfa_to_dfa(nfa):
    start_set = frozenset(epsilon_closure({nfa["start"]}, nfa["transitions"]))
    queue = deque([start_set])
    visited = {start_set}
    dfa_trans = {}

    while queue:
        curr = queue.popleft()
        curr_name = format_state(curr)
        dfa_trans[curr_name] = {}
        for sym in nfa["alphabet"]:
            move_set = set()
            for s in curr:
                move_set.update(nfa["transitions"].get((s, sym), set()))
            next_set = frozenset(epsilon_closure(move_set, nfa["transitions"]))
            dfa_trans[curr_name][sym] = format_state(next_set)
            if next_set not in visited:
                visited.add(next_set)
                queue.append(next_set)

    dfa_states = [format_state(s) for s in visited]
    dfa_final = [format_state(s) for s in visited if s & set(nfa["final"])]
    return {
        "states": dfa_states,
        "alphabet": nfa["alphabet"],
        "start": format_state(start_set),
        "final": dfa_final,
        "transitions": dfa_trans
    }

def remove_unreachable(dfa):
    reachable = {dfa["start"]}
    queue = deque([dfa["start"]])
    while queue:
        curr = queue.popleft()
        for sym in dfa["alphabet"]:
            nxt = dfa["transitions"][curr][sym]
            if nxt not in reachable:
                reachable.add(nxt)
                queue.append(nxt)

    return {
        "states": [s for s in dfa["states"] if s in reachable],
        "alphabet": dfa["alphabet"],
        "start": dfa["start"],
        "final": [s for s in dfa["final"] if s in reachable],
        "transitions": {s: dfa["transitions"][s] for s in dfa["states"] if s in reachable}
    }

def minimize_dfa(dfa):
    dfa = remove_unreachable(dfa)
    states = sorted(dfa["states"])
    alphabet = dfa["alphabet"]
    final = set(dfa["final"])
    trans = dfa["transitions"]
    n = len(states)

    marked = set()
    for i in range(n):
        for j in range(i + 1, n):
            if (states[i] in final) != (states[j] in final):
                marked.add((states[i], states[j]))

    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                pair = (states[i], states[j])
                if pair in marked:
                    continue
                for sym in alphabet:
                    u = trans[states[i]][sym]
                    v = trans[states[j]][sym]
                    if u != v:
                        next_pair = tuple(sorted((u, v)))
                        if next_pair in marked:
                            marked.add(pair)
                            changed = True
                            break

    visited = set()
    classes = []
    for s in states:
        if s not in visited:
            eq_class = [s]
            visited.add(s)
            for other in states:
                if other not in visited and tuple(sorted((s, other))) not in marked:
                    eq_class.append(other)
                    visited.add(other)
            classes.append(tuple(sorted(eq_class)))

    state_map = {}
    for c in classes:
        label = "[" + ", ".join(c) + "]"
        for s in c:
            state_map[s] = label

    min_states = [state_map[c[0]] for c in classes]
    min_start = state_map[dfa["start"]]
    min_final = [state_map[c[0]] for c in classes if c[0] in final]
    min_trans = {}
    for c in classes:
        rep = c[0]
        cname = state_map[rep]
        min_trans[cname] = {sym: state_map[trans[rep][sym]] for sym in alphabet}

    return {
        "states": min_states,
        "alphabet": alphabet,
        "start": min_start,
        "final": min_final,
        "transitions": min_trans
    }

if __name__ == "__main__":
    nfa_var9 = {
        "states": ["A", "B", "C"],
        "alphabet": ["0", "1"],
        "start": "A",
        "final": ["C"],
        "transitions": {
            ("A", "0"): {"A", "B"},
            ("B", "0"): {"C"},
            ("B", "1"): {"B"},
            ("C", "0"): {"C"},
            ("C", "1"): {"C"}
        }
    }

    dfa_var9 = nfa_to_dfa(nfa_var9)
    print("ДСА після детермінізації (Варіант 9):")
    print(f"Кількість станів: {len(dfa_var9['states'])}")
    print(f"Фінальні стани: {dfa_var9['final']}")
    for st, row in dfa_var9["transitions"].items():
        print(f"  {st}: 0 -> {row['0']}, 1 -> {row['1']}")

    min_dfa_var9 = minimize_dfa(dfa_var9)
    print("\nМінімальний ДСА:")
    print(f"Кількість станів: {len(min_dfa_var9['states'])}")
    print(f"Початковий стан: {min_dfa_var9['start']}")
    print(f"Фінальні стани: {min_dfa_var9['final']}")
    for st, row in min_dfa_var9["transitions"].items():
        print(f"  {st}: 0 -> {row['0']}, 1 -> {row['1']}")

    test_automata = [
        ("Автомат 1 (базовий)", {
            "states": ["q0", "q1", "q2"],
            "alphabet": ["0", "1"],
            "start": "q0",
            "final": ["q1", "q2"],
            "transitions": {
                "q0": {"0": "q0", "1": "q1"},
                "q1": {"0": "q0", "1": "q2"},
                "q2": {"0": "q0", "1": "q1"}
            }
        }),
        ("Автомат 2 (завдання 3)", {
            "states": ["D0", "D1", "D2", "D3", "D4"],
            "alphabet": ["0", "1"],
            "start": "D0",
            "final": ["D3", "D4"],
            "transitions": {
                "D0": {"0": "D1", "1": "D1"},
                "D1": {"0": "D2", "1": "D2"},
                "D2": {"0": "D3", "1": "D3"},
                "D3": {"0": "D4", "1": "D4"},
                "D4": {"0": "D4", "1": "D4"}
            }
        }),
        ("Автомат 3 (парні нулі)", {
            "states": ["A", "B", "C", "D", "E", "F"],
            "alphabet": ["0", "1"],
            "start": "A",
            "final": ["A", "C", "E"],
            "transitions": {
                "A": {"0": "B", "1": "C"},
                "B": {"0": "C", "1": "D"},
                "C": {"0": "D", "1": "E"},
                "D": {"0": "E", "1": "F"},
                "E": {"0": "F", "1": "A"},
                "F": {"0": "A", "1": "B"}
            }
        }),
        ("Автомат 4 (варіант 9)", dfa_var9),
        ("Автомат 5 (розширений)", {
            "states": ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
            "alphabet": ["0", "1"],
            "start": "S0",
            "final": ["S4", "S5", "S8"],
            "transitions": {
                "S0": {"0": "S1", "1": "S2"},
                "S1": {"0": "S3", "1": "S4"},
                "S2": {"0": "S3", "1": "S5"},
                "S3": {"0": "S6", "1": "S7"},
                "S4": {"0": "S4", "1": "S4"},
                "S5": {"0": "S5", "1": "S5"},
                "S6": {"0": "S8", "1": "S7"},
                "S7": {"0": "S6", "1": "S8"},
                "S8": {"0": "S8", "1": "S8"}
            }
        })
    ]

    print("\nПорівняльна таблиця результатів мінімізації:")
    print(f"{'Назва автомата':<25} | {'N':<4} | {'T':<4} | {'Nmin':<5} | {'K (%)':<8}")
    print("-" * 58)
    for name, dfa_item in test_automata:
        n_orig = len(dfa_item["states"])
        t_orig = n_orig * len(dfa_item["alphabet"])
        minimized = minimize_dfa(dfa_item)
        n_min = len(minimized["states"])
        k_red = ((n_orig - n_min) / n_orig) * 100
        print(f"{name:<25} | {n_orig:<4} | {t_orig:<4} | {n_min:<5} | {k_red:<8.2f}")