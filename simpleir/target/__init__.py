#


class Compiler:
    def __init__(self, prog):
        self.prog = prog

    def compile(self):
        raise NotImplementedError()

    @staticmethod
    def indent(code, level=2):
        result = []
        for line in code.split('\n'):
            result.append(' ' * level + line)
        return '\n'.join(result)
