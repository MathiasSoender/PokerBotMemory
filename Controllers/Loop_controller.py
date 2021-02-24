import multiprocessing as mp
from Misc.Simulator_package import tree_package
from Services.OddsPrecomputedService import pre_computed_service
from Misc.Simulator_package import pre_computed_package
from Services.TreeService import tree_service


class LoopController:
    def __init__(self, cores, target_func, new_tree, tree_path, human_vs_bot = False):
        self.data_comms = []
        self.pre_computed_Q = mp.Queue()
        self.tree_Q = mp.Queue()
        self.result_Q = mp.Queue()
        self.end_Q = mp.Queue()

        self.jobs = []
        self.cores = cores
        self.MAIN = target_func
        self.new_tree = new_tree
        self.tree_path = tree_path

        self.tree_service = None
        self.pre_computed_service = None

        self.human_vs_bot = human_vs_bot



    """ Initial start. """
    def start(self):

        for i in range(0, self.cores):
            Queue = mp.Queue()
            self.data_comms.append(Queue)
            if not self.human_vs_bot:
                self.jobs.append(self.start_proc(i))

        self.pre_computed_service = mp.Process(target = pre_computed_service,
                                               args = (self.pre_computed_Q, self.data_comms))
        self.pre_computed_service.start()
        self.tree_service = mp.Process(target = tree_service,
                                       args = (self.tree_Q, self.data_comms, self.new_tree, self.tree_path))
        self.tree_service.start()

    """ Spins up a process. """
    def start_proc(self, ID):
        p = mp.Process(target=self.MAIN, args=(self.data_comms[ID], self.tree_Q,
                                               self.pre_computed_Q, self.result_Q, self.end_Q, ID))
        p.start()
        return p



    def close_processes(self):
        print("Shutting down processes")
        for _ in range(0, 10):
            self.end_Q.put("stop")

        for j in self.jobs:
            j.join()
        self.tree_Q.put(tree_package(None, None, None, None, "stop", None))
        self.pre_computed_Q.put((pre_computed_package(None, None, None, "stop", None)))
        self.pre_computed_service.join()
        self.tree_service.join()





