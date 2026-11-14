alphabet = set(str(i) for i in range(10))
L1 = {"1", "12", "123"}
L2 = {"9", "98", "987"}


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


def concat_languages(A, B):
    return set(a + b for a in A for b in B)


def complement_language(A, max_length):
    all_words_leq_k = set()
    for i in range(max_length + 1):
        all_words_leq_k.update(generate_words(i))
    return all_words_leq_k - A


if __name__ == "__main__":
    print("Завдання 3. Операції над мовами")
    print(f"L1 = {L1}")
    print(f"L2 = {L2}")
    print(f"L1 ∪ L2: {L1 | L2}")
    print(f"L1 ∩ L2: {L1 & L2}")
    print(f"L1 \\ L2: {L1 - L2}")
    print(f"L1L2: {concat_languages(L1, L2)}")

    comp = complement_language(L1, 2)
    print(f"Доповнення L1 (довжина <= 2): {list(comp)[:10]}...")

    L2_2 = concat_languages(L2, L2)
    L2_3 = concat_languages(L2_2, L2)
    print(f"Степінь мови L2^3:\n{L2_3}")