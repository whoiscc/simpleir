#

# pylint: disable = unused-wildcard-import
from simpleir.target.py import *
from simpleir.prog import Prog

prog = Prog()
var_sum = prog.create_var()
var_i = prog.create_var()
var_n = prog.create_var()
prog.set_stat(PySeq([
    PyAssign(var_n, PyInput('n')),
    PyAssign(var_sum, PyConst(0)),
    PyAssign(var_i, PyConst(1)),
    PyWhileDo(PyOp('le', [PyLoad(var_i), PyLoad(var_n)]), PySeq([
        PyAssign(var_sum, PyOp('add', [PyLoad(var_sum), PyLoad(var_i)])),
        PyAssign(var_i, PyOp('add', [PyLoad(var_i), PyConst(1)])),
    ])),
    PyOutput('sum', PyLoad(var_sum)),
]))

compiler = PyCompiler(prog, 'acc')
print(compiler.compile())
print("print(acc({'n': 100}))")
