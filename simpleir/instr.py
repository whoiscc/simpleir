#

from simpleir.prog import Var


class Stat:
    pass


class Expr:
    pass


class Seq(Stat):
    def __init__(self, stat_list):
        assert all(isinstance(stat, Stat) for stat in stat_list)
        self.stat_list = stat_list


class Op(Expr):
    def __init__(self, ty, operand_list):
        assert isinstance(ty, str)
        assert all(isinstance(operand, Expr) for operand in operand_list)
        self.ty = ty
        self.operand_list = operand_list


class Const(Expr):
    def __init__(self, value):
        self.value = value


class Assign(Stat):
    def __init__(self, var, expr):
        assert isinstance(var, Var)
        assert isinstance(expr, Expr)
        self.var = var
        self.expr = expr


class Load(Expr):
    def __init__(self, var):
        assert isinstance(var, Var)
        self.var = var


class End(Stat):
    pass


class IfElse(Stat):
    def __init__(self, guard, true, false):
        assert isinstance(guard, Expr)
        assert isinstance(true, Stat)
        assert isinstance(false, Stat)
        self.guard = guard
        self.true = true
        self.false = false


class WhileDo(Stat):
    def __init__(self, guard, do):
        assert isinstance(guard, Expr)
        assert isinstance(do, Stat)
        self.guard = guard
        self.do = do


class Input(Expr):
    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name


class Output(Stat):
    def __init__(self, name, expr):
        assert isinstance(name, str)
        assert isinstance(expr, Expr)
        self.name = name
        self.expr = expr


class Nop(Stat):
    pass
