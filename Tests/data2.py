from Tree.data2 import Data
import random
D = Data()
for i in range(0,100000):
    D.update(random.randint(30,100)*0.01, 1)
print(D.all_probabilities)
print(len(D.all_probabilities))

print(D)


def checkNodes():
    import pickle
    nodes = pickle.load(open(r"C:\Users\Mathi\Desktop\cards7_memory\Simulator_main\model5799999\nodes\nodes199999", "rb"))
    i = 0
    for n in nodes:
        if sum(n.data.N) > 50:
            print(n.data.N)
            i += 1
    print(i)

