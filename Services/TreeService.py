import copy
import os
import sys
import traceback

from Controllers.Game_controller import game_controller
from Misc.Logger import loggerNonStatic
from Tree.Tree import Tree
from pympler import asizeof


def tree_service(tree_Q, channels, new_tree, path, is_bot=False):
    try:
        os.chdir("..")
        if is_bot:
            os.chdir("..")
        os.chdir("Simulator_main")
        T = Tree(new_tree=new_tree, path=path)

        if is_bot:
            tree_Q.put(1)

        logger = loggerNonStatic("master")

        while True:
            res = tree_Q.get()

            if res.request == "process":
                current_node = T.nodes[res.current_node_name]
                if not res.is_bot:
                    T.expand_tree(res.current_player, res.all_players, current_node, res.controller)
                channels[res.ID].put(current_node.local_node())

            elif res.request == "root":
                T.rounds_trained += 1
                current_node = T.root
                if not res.is_bot:
                    T.expand_tree(res.current_player, res.all_players, current_node, res.controller)
                channels[res.ID].put(T.root.local_node())

            elif res.request == "backprop":
                nodes_for_update = []
                for iden, odds, player in res.selected_nodes:
                    # Finds the correct node for update
                    node_ = T.nodes[iden.name]
                    nodes_for_update.append((node_, odds, player))

                g_controller = game_controller()
                g_controller.selected_nodes = nodes_for_update
                logger.end_log(res.players, res.winner, res.community, res.pot)
                logger.nodes_log(g_controller.selected_nodes)

                g_controller.back_prop(res.pot, res.winner)

                logger.nodes_log(g_controller.selected_nodes, "After")


            elif res.request == "getSubtree":
                if res.current_node_name[-2:] in ["F:", "T:", "R:"]:
                    res.current_node_name = res.current_node_name[:-2]
                sub_tree = T.nodes[res.current_node_name].subtree()
                channels[res.ID].put(sub_tree)
                print("done fetching subtree")


            elif res.request == "updateSubtree":
                print("getting subtree")
                sub_tree = res.current_player
                print("Gotten subtree")
                for node in sub_tree.nodes.values():
                    print(node)
                    if node.identifier.name in T.nodes:
                        T.nodes[node.identifier.name].data = node.data
                    else:
                        T.add_node(node.identifier, node.data, parent=T.nodes[node.parent.identifier.name])



            elif res.request == "stop":
                break

            if ((T.rounds_trained + 1) % 150000 == 0) and is_bot is False:
                print("intermediate save of model")
                rt = "model" + str(T.rounds_trained)
                T.to_object(rt)
                del T
                T = Tree(path=rt)

                T.rounds_trained += 1

        print("size: " + str(asizeof.asizeof(T)))
        T.to_object("model")
        print("Tree service shutdown")
        print("Len: " + str(len(T.nodes)))
        print("rounds trained: " + str(T.rounds_trained))

    except SystemExit:
        raise
    except:
        traceback.print_exc(file=sys.stdout)