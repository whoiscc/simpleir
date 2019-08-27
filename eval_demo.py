#

from simpleir.prog import Prog
# pylint: disable = unused-wildcard-import
from simpleir.eval import *

prog = Prog()
var_x = prog.create_var()
prog.set_stat(EvalSeq([
    EvalAssign(var_x, EvalInput('x')),
    EvalAssign(var_x, EvalOp('mul', [EvalLoad(var_x), EvalConst(2)])),
    EvalOutput('y', EvalLoad(var_x)),
]))

x = 42
evaluator = Evaluator()
evaluator.set_env('x', x)
evaluator.eval(prog)
y = evaluator.get_env('y')
print(f'{x} * 2 = {y}')
