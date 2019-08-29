#

# pylint: disable = unused-wildcard-import
from simpleir.instr import *
from simpleir.prog import Prog
from simpleir.target import Compiler


class PyStat(Stat):
    def gen_stat(self, compiler):
        raise NotImplementedError()


class PyExpr(Expr):
    def gen_expr(self, compiler):
        raise NotImplementedError()


class PyCompiler(Compiler):
    def __init__(self, prog, name):
        super().__init__(prog)
        self.name = name
        self.var_map = {}
        var_count = 0
        for var in prog.var_list:
            self.var_map[var] = f'var_{var_count}'
            var_count += 1

    def get_var(self, var):
        return self.var_map[var]

    def compile(self):
        return '\n'.join([
            f'def {self.name}(input):',
            self.indent('output = {}', 4),
            self.indent(self.prog.stat.gen_stat(self), 4),
            self.indent('return output', 4),
        ])


class PyInput(Input, PyExpr):
    def gen_expr(self, compiler):
        return f"input['{self.name}']"


class PyOutput(Output, PyStat):
    def gen_stat(self, compiler):
        return f"output['{self.name}'] = {self.expr.gen_expr(compiler)}"


class PyLoad(Load, PyExpr):
    def gen_expr(self, compiler):
        return compiler.get_var(self.var)


class PyAssign(Assign, PyStat):
    def gen_stat(self, compiler):
        return f'{compiler.get_var(self.var)} = {self.expr.gen_expr(compiler)}'


class PyEnd(End, PyStat):
    def gen_stat(self, compiler):
        return f'return output'


class PyOp(Op, PyExpr):
    def gen_expr(self, compiler):
        binary_map = {
            'add': '+',
            'sub': '-',
            'mul': '*',
            'div': '/',
            'le': '<=',
        }
        if self.ty in binary_map:
            return self.gen_binary(binary_map[self.ty], compiler)
        else:
            assert False

    def gen_binary(self, op, compiler):
        assert isinstance(self.operand_list[0], PyExpr)
        assert isinstance(self.operand_list[1], PyExpr)
        return (
            '(' +
            self.operand_list[0].gen_expr(compiler) +
            ' ' + op + ' ' +
            self.operand_list[1].gen_expr(compiler) +
            ')'
        )


class PyConst(Const, PyExpr):
    def gen_expr(self, compiler):
        return str(self.value)


class PySeq(Seq, PyStat):
    def gen_stat(self, compiler):
        return '\n'.join([stat.gen_stat(compiler) for stat in self.stat_list])


class PyIfElse(IfElse, PyStat):
    def gen_stat(self, compiler):
        return '\n'.join([
            f'if {self.guard.gen_expr(compiler)}:',
            Compiler.indent(self.true.gen_stat(compiler), 4),
            'else:',
            Compiler.indent(self.false.gen_stat(compiler), 4),
        ])


class PyWhileDo(WhileDo, PyStat):
    def gen_stat(self, compiler):
        return '\n'.join([
            f'while {self.guard.gen_expr(compiler)}:',
            Compiler.indent(self.do.gen_stat(compiler), 4),
        ])


class PyNop(Nop, PyStat):
    def gen_stat(self, compiler):
        return '# nop'
