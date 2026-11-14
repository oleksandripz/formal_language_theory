alphabet = set(str(i) for i in range(10))

def check_symbol(symbol):
    return symbol in alphabet

def check_word(word):
    if word == "":
        return True
    return all(check_symbol(char) for char in word)

if __name__ == "__main__":
    print("Завдання 1. Створення алфавіту")
    print(f"Алфавіт Σ: {alphabet}")
    print(f"Символ '5' належить алфавіту: {check_symbol('5')}")
    print(f"Символ 'a' належить алфавіту: {check_symbol('a')}")
    print(f"Рядок '123' є словом: {check_word('123')}")
    print(f"Порожній рядок є словом: {check_word('')}")