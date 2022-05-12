from collections import defaultdict


def rate_symbols(filename):
    with open(filename, encoding='utf8') as file:
        text = file.read()

    symbol_counter = defaultdict(int)
    total_symbols = 0
    for char in text:
        if char != ' ':
            symbol_counter[char.lower()] += 1
            total_symbols += 1

    result = {}
    for char, number in symbol_counter.items():
        result[char] = round((number / total_symbols) * 100, 2)

    for char, rating in sorted(result.items(), key=lambda x: x[0]):
        print(f'{char} - {rating}%')


if __name__ == '__main__':
    rate_symbols('war and peace.txt')
