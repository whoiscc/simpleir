#

# pylint: disable = unused-wildcard-import
from simpleir.instr import *
from simpleir.prog import Prog


prog = Prog()
var_a = prog.create_var()
var_b = prog.create_var()
prog.set_stat(Seq([
    Assign(var_a, Const(42)),
    Assign(var_b, Input('offset')),
    Assign(var_a, Op('add', [Load(var_a), Load(var_b)])),
    IfElse(
        Op('gt', [Load(var_a), Input('threshold')]),
        Assign(var_a, Op('sub', [Load(var_a), Load(var_b)])),
        Nop(),
    ),
    Output('result', Load(var_a)),
]))
