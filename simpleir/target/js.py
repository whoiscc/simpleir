#

# pylint: disable = unused-wildcard-import
from simpleir.instr import *
from simpleir.prog import Prog
from simpleir.target import Compiler


class JsStat(Stat):
    def gen_stat(self, compiler):
        raise NotImplementedError()


class JsExpr(Expr):
    def gen_expr(self, compiler):
        raise NotImplementedError()


class JsCompiler(Compiler):
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
        var_str = ', '.join(self.var_map.values())
        return '\n'.join([
            f'function {self.name}(input) {{',
            self.indent('let output = {};'),
            self.indent(f'let {var_str};'),
            self.indent(self.prog.stat.gen_stat(self)),
            self.indent('return output;'),
            '}',
        ])


class JsInput(Input, JsExpr):
    def gen_expr(self, compiler):
        return f'input.{self.name}'


class JsOutput(Output, JsStat):
    def gen_stat(self, compiler):
        return f'output.{self.name} = {self.expr.gen_expr(compiler)};'


class JsLoad(Load, JsExpr):
    def gen_expr(self, compiler):
        return compiler.get_var(self.var)


class JsAssign(Assign, JsStat):
    def gen_stat(self, compiler):
        return f'{compiler.get_var(self.var)} = {self.expr.gen_expr(compiler)};'


class JsEnd(End, JsStat):
    def gen_stat(self, compiler):
        return f'return output;'


class JsOp(Op, JsExpr):
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
        assert isinstance(self.operand_list[0], JsExpr)
        assert isinstance(self.operand_list[1], JsExpr)
        return (
            '(' +
            self.operand_list[0].gen_expr(compiler) +
            ' ' + op + ' ' +
            self.operand_list[1].gen_expr(compiler) +
            ')'
        )


class JsConst(Const, JsExpr):
    def gen_expr(self, compiler):
        return str(self.value)


class JsSeq(Seq, JsStat):
    def gen_stat(self, compiler):
        return '\n'.join([stat.gen_stat(compiler) for stat in self.stat_list])


class JsIfElse(IfElse, JsStat):
    def gen_stat(self, compiler):
        return '\n'.join([
            f'if ({self.guard.gen_expr(compiler)}) {{',
            Compiler.indent(self.true.gen_stat(compiler)),
            '} else {{',
            Compiler.indent(self.false.gen_stat(compiler)),
            '}',
        ])


class JsWhileDo(WhileDo, JsStat):
    def gen_stat(self, compiler):
        return '\n'.join([
            f'while ({self.guard.gen_expr(compiler)}) {{',
            Compiler.indent(self.do.gen_stat(compiler)),
            '}',
        ])
