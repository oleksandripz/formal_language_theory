import re

TOKEN_TYPES = [
    ('IDENT', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('NUM', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.')
]


def lex(expr):
    tokens = []
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)
    for match in re.finditer(tok_regex, expr):
        kind = match.lastgroup
        value = match.group()
        start_pos = match.start()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Лексична помилка: невідомий символ '{value}' на позиції {start_pos}")
        tokens.append((kind, value, start_pos))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type):
        tok = self.current_token()
        if tok and tok[0] == expected_type:
            self.pos += 1
            return tok
        actual = tok[0] if tok else "КІНЕЦЬ РЯДКА"
        pos = tok[2] if tok else "кінці"
        raise SyntaxError(
            f"Синтаксична помилка: очікувався токен {expected_type}, але знайдено {actual} на позиції {pos}")

    def parse_expr(self):
        node = self.parse_term()
        while self.current_token() and self.current_token()[0] == 'PLUS':
            op = self.consume('PLUS')
            right = self.parse_term()
            node = {'type': 'BinOp', 'op': op[1], 'left': node, 'right': right}
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token() and self.current_token()[0] == 'TIMES':
            op = self.consume('TIMES')
            right = self.parse_factor()
            node = {'type': 'BinOp', 'op': op[1], 'left': node, 'right': right}
        return node

    def parse_factor(self):
        tok = self.current_token()
        if not tok:
            raise SyntaxError("Синтаксична помилка: неочікуваний кінець виразу")
        if tok[0] == 'IDENT':
            self.consume('IDENT')
            return {'type': 'IDENT', 'value': tok[1]}
        elif tok[0] == 'NUM':
            self.consume('NUM')
            return {'type': 'NUM', 'value': tok[1]}
        elif tok[0] == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_expr()
            self.consume('RPAREN')
            return node
        else:
            raise SyntaxError(f"Синтаксична помилка: неочікуваний токен {tok[0]} '{tok[1]}' на позиції {tok[2]}")


def print_ast(node, indent=""):
    if node['type'] in ('IDENT', 'NUM'):
        print(f"{indent}|-- {node['type']}: {node['value']}")
    elif node['type'] == 'BinOp':
        print(f"{indent}|-- Операція: {node['op']}")
        print_ast(node['left'], indent + "    ")
        print_ast(node['right'], indent + "    ")


if __name__ == "__main__":
    expr_valid = "value + 0"
    print(f"Аналіз виразу: '{expr_valid}'")
    tokens = lex(expr_valid)
    print("Список утворених токенів:")
    for t in tokens:
        print(f"  ({t[0]}, '{t[1]}')")

    print("\nДерево розбору (AST):")
    parser = Parser(tokens)
    ast = parser.parse_expr()
    print_ast(ast)

    expr_invalid = "value + (0"
    print(f"\nАналіз помилкового виразу: '{expr_invalid}'")
    tokens_err = lex(expr_invalid)
    parser_err = Parser(tokens_err)
    try:
        parser_err.parse_expr()
        if parser_err.pos < len(tokens_err):
            raise SyntaxError("Синтаксична помилка: зайві символи наприкінці виразу")
    except SyntaxError as e:
        print(f"Зловлено виняток: {e}")