import pickle
some = pickle.load(open(r"C:\Users\Mathi\Desktop\cards7_memory\Simulator_main\model\nodes\nodes7706", "rb"))

node = some[1]

print(node.data.find_split(0.5))


