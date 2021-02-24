import keyboard
import time

from Poker.Deck import Deck
from Misc.Timer import timer
from Misc.Logger import loggerNonStatic
from Misc.Simulator_package import package
from Controllers.Game_controller import game_controller
from Controllers.Loop_controller import LoopController



def sim(rounds, new_tree = False,  tree_name = "model", cores = 2):
    t1 = time.time()

    LoopCont = LoopController(cores, main_loop, new_tree, tree_name)

    # Start the | cores | processes:
    LoopCont.start()


    epoch = 0
    while epoch <= rounds:
        if epoch % 75 == 0:
            if keyboard.is_pressed('q'):
                break
            print("rounds done: " + str(epoch) + " time: " + str(time.time()-t1))
            t1 = time.time()


        # One processor is finished.
        LoopCont.result_Q.get()
        epoch += 1


    LoopCont.close_processes()









def main_loop(P, tree_Q, pre_computed_Q, result_Q = None, end_Q = None, ID = 0):
    Timer = timer(["odds"])
    logger = loggerNonStatic(ID)
    stop = False

    while not stop:
        deck = Deck()
        controller = game_controller()
        players = controller.start_game(deck)
        current_player = players.find_player("UTG")
        current_node = None
        logger.new_round()


        while not controller.game_ended:
            current_node = controller.request_node(current_node, tree_Q, P, current_player, players, ID)
            controller.new_street = [False, ""]
            # Find odds
            Timer.start_timer("odds")
            current_player.determine_odds(players, controller, pre_computed_Q, ID = ID, channel=P)
            Timer.end_timer("odds")
            logger.log("current player: " + str(current_player) + ", odds: " + str(current_player.win_odds))

            # Do action
            current_node = controller.do_action(current_node, current_player, players, LOG=logger)
            logger.log("Selected node: " + str(current_node.identifier.find_current_street()[-1]) + "\n")

            # Next player's turn
            current_player = controller.find_next_player(current_player, players)

            # Game ended + new street.
            controller.check_if_game_ended(players)

            if controller.check_if_street_ended(players) and not controller.game_ended:
                current_player = controller.update_street(deck, players)
                logger.log("street updated to: " + str(controller.street))

                # Do another check, to avoid "end" error:
                controller.check_if_game_ended(players)

        pot = players.pot_size()
        winner = controller.find_winner(players, deck)

        # Sends the information regarding each round back to master.
        tree_Q.put(package(controller.selected_nodes, controller.community, players.players, pot, winner, "backprop"))
        if result_Q is not None:
            result_Q.put(1)

        try:
            end_Q.get(timeout = 0.01)
            stop = True
            print("should stop")
        except:
            stop = False

    print(Timer)






if __name__ == "__main__":
    # multiprocessing.freeze_support()

    total = time.time()
    sim(rounds=5, new_tree=False, cores=6)
    print("total time taken: " + str(time.time()-total))
    



