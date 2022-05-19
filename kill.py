import subprocess
import test_main as tm

cma = 'pkill master_main'
cmd = 'ssh grasure@node{:0>2d} "pkill node_main"'

subprocess.call(cma, shell=True)
for i in range(1, tm.nodes_num+1):
    subprocess.call(cmd.format(i), shell=True)
