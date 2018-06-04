from .python_parser import Parser, a, anyof, maybe, skip, someof

tokens = (
    (r'[a-zA-z0-9-\.]+', 'VALUE'),
    (r'".*"', 'STRING'),
    (r'\(', 'L_BRACE'),
    (r'\)', 'R_BRACE'),
)

grammar = {
    'ROOT': maybe('NODES'),
    'NODES': maybe('NODE', maybe(someof('NODE'))),
    'VAL': anyof('STRING', 'VALUE', 'NODE'),
    'NODE': a(
        skip('L_BRACE'),
        maybe('VAL', maybe(someof('VAL'))),
        skip('R_BRACE')
    ),
}

__parser__ = Parser(tokens, grammar)

def parse(text):

    def node(n):
        return list(map(val, n.items))

    def val(n):
        i = n.items[0]
        return {
            'STRING': lambda t: t.value[1: -1],
            'VALUE': lambda t: str(t.value),
            'NODE': lambda t: node(t)
        }[i.name](i)

    def nodes(n):
        return list(map(node, n.items))

    ast = __parser__.parse('ROOT', text)
    root = ast.items[0]
    return locals()[root.name.lower()](root)
