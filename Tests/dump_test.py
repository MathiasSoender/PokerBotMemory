import os
from Tree.Tree import Tree
import time

os.chdir("..")
os.chdir("simulator_main")
t1 = time.time()
T = Tree()
print("Time taken for load: " + str(time.time()-t1))

t1 = time.time()
T.to_object("test")
print("Time taken for proto 3: " + str(time.time()-t1))
