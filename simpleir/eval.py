#

from simpleir.prog import Prog
# pylint: disable = unused-wildcard-import
from simpleir.instr import *


class EvalExpr(Expr):
    def eval_expr(self, runtime):
        raise NotImplementedError()


class EvalStat(Stat):
    def eval_stat(self, runtime):
        raise NotImplementedError()


class Evaluator:
    def __init__(self):
        self.env = {}

    def set_env(self, name, value):
        self.env[name] = value

    def get_env(self, name):
        return self.env[name]

    def eval(self, prog):
        assert isinstance(prog, Prog)
        runtime = Runtime(self)
        runtime.eval(prog)


class Runtime:
    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.mem = {}

    def set_env(self, name, value):
        self.evaluator.set_env(name, value)

    def get_env(self, name):
        return self.evaluator.get_env(name)

    def set_var(self, var, value):
        self.mem[var] = value

    def get_var(self, var):
        return self.mem[var]

    class Terminate(Exception):
        pass

    def terminate(self):
        raise Runtime.Terminate()

    def eval(self, prog):
        assert isinstance(prog.stat, EvalStat)
        try:
            prog.stat.eval_stat(self)
        except Runtime.Terminate:
            pass


class EvalInput(Input, EvalExpr):
    def eval_expr(self, runtime):
        return runtime.get_env(self.name)


class EvalOutput(Output, EvalStat):
    def eval_stat(self, runtime):
        assert isinstance(self.expr, EvalExpr)
        runtime.set_env(self.name, self.expr.eval_expr(runtime))


class EvalAssign(Assign, EvalStat):
    def eval_stat(self, runtime):
        assert isinstance(self.expr, EvalExpr)
        runtime.set_var(self.var, self.expr.eval_expr(runtime))


class EvalLoad(Load, EvalExpr):
    def eval_expr(self, runtime):
        return runtime.get_var(self.var)


class EvalEnd(End, EvalStat):
    def eval_stat(self, runtime):
        runtime.terminate()


class EvalConst(Const, EvalExpr):
    def eval_expr(self, runtime):
        return self.value


class EvalOp(Op, EvalExpr):
    def eval_expr(self, runtime):
        from operator import add, sub, mul, truediv
        binary_map = {
            'add': add,
            'sub': sub,
            'mul': mul,
            'div': truediv,
        }
        if self.ty in binary_map:
            return self.binary(binary_map[self.ty], runtime)
        else:
            assert False

    def binary(self, proc, runtime):
        assert isinstance(self.operand_list[0], EvalExpr)
        assert isinstance(self.operand_list[1], EvalExpr)
        return proc(
            self.operand_list[0].eval_expr(runtime),
            self.operand_list[1].eval_expr(runtime),
        )


class EvalIfElse(IfElse, EvalStat):
    def eval_stat(self, runtime):
        if self.guard.eval_expr(runtime):
            self.true.eval_stat(runtime)
        else:
            self.false.eval_stat(runtime)


class EvalWhileDo(WhileDo, EvalStat):
    def eval_stat(self, runtime):
        while self.guard.eval_expr(runtime):
            self.do.eval_stat(runtime)


class EvalSeq(Seq, EvalStat):
    def eval_stat(self, runtime):
        for stat in self.stat_list:
            assert isinstance(stat, EvalStat)
            stat.eval_stat(runtime)


class EvalNop(Nop, EvalStat):
    def eval_stat(self, runtime):
        pass
