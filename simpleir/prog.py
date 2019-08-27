#


class Prog:
    def __init__(self):
        self.var_list = []
        self.stat = None

    def create_var(self):
        var = Var(self)
        self.var_list.append(var)
        return var

    def set_stat(self, stat):
        assert self.stat is None
        self.stat = stat


class Var:
    def __init__(self, prog):
        self.prog = prog
