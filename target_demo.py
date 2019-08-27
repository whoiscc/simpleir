#

from simpleir.target.js import *
from simpleir.prog import Prog

prog = Prog()
var_sum = prog.create_var()
var_i = prog.create_var()
var_n = prog.create_var()
prog.set_stat(JsSeq([
    JsAssign(var_n, JsInput('n')),
    JsAssign(var_sum, JsConst(0)),
    JsAssign(var_i, JsConst(1)),
    JsWhileDo(JsOp('le', [JsLoad(var_i), JsLoad(var_n)]), JsSeq([
        JsAssign(var_sum, JsOp('add', [JsLoad(var_sum), JsLoad(var_i)])),
        JsAssign(var_i, JsOp('add', [JsLoad(var_i), JsConst(1)])),

    ])),
    JsOutput('sum', JsLoad(var_sum)),
]))

compiler = JsCompiler(prog, 'acc')
print(compiler.compile())
print('console.log(acc({n: 100}))')
