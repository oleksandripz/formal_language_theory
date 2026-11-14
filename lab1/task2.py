alphabet = set(str(i) for i in range(10))


def generate_words(n):
    words = []

    def generate(current_word):
        if len(current_word) == n:
            words.append(current_word)
            return
        for char in sorted(alphabet):
            generate(current_word + char)

    generate("")
    return words


if __name__ == "__main__":
    n = 3
    print(f"Завдання 2. Генерація слів (довжина n={n})")
    all_words = generate_words(n)
    valid_words = []

    for w in all_words:
        if w.startswith("0") and len(w) > 1:
            continue
        if int(w) % 5 == 0:
            valid_words.append(w)

    print("Слова, що є десятковим записом числа, кратного 5:")
    print(", ".join(valid_words))
    print(f"Загальна кількість: {len(valid_words)}")