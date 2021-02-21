from Controllers.Game_controller import game_controller
from Controllers.Loop_controller import LoopController
from Misc.Precomputed import precomputed_odds
from Poker.Deck import Deck
from Tree.Tree import Tree
import os
from Human_vs_bot.Display import Display

def main():
    os.chdir("..")
    os.chdir("Simulator_main")
    display = Display()
    display.start_print()
    loopC = LoopController(1, "", False, "model", human_vs_bot=True)

    loopC.start()
    game(loopC.tree_Q, loopC.pre_computed_Q, loopC.data_comms[0])
    loopC.close_processes()




def game(tree_Q, pre_computed_Q,P):
    display = Display()
    hands_played = 0
    winnings = 0
    positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
    hero_position = "UTG"

    while not display.exit:
        hands_played += 1
        deck = Deck()
        controller = game_controller()
        players = controller.start_game(deck)
        current_player = players.find_player("UTG")
        players.find_player(hero_position).hero = True
        current_node = None

        display.new_hand(players.find_player(hero_position))


        while not controller.game_ended:
            current_node = controller.request_node(current_node, tree_Q, P, current_player, players, 0)
            controller.new_street = [False, ""]

            if current_player.hero:
                display.print_state(controller, players)
                current_node = display.actions(current_node)
                controller.do_action(current_node, current_player, players, Human=True)
            else:
                current_player.determine_odds(players, controller, pre_computed_Q, ID=0, channel=P)
                current_node = controller.do_action(current_node, current_player, players)

            current_player = controller.find_next_player(current_player, players)

            controller.check_if_game_ended(players)

            if controller.check_if_street_ended(players) and not controller.game_ended:
                current_player = controller.update_street(deck, players, current_node)

        pot = players.pot_size()
        winner = controller.find_winner(players, deck)

        display.showdown(winner, pot, controller.community, players)

        if players.find_player(hero_position) in winner:
            winnings += (1/len(winner) * (pot - (100-players.find_hero().chips)))
        else:
            winnings -= 100 - players.find_hero().chips


        if hero_position == "BB":
            hero_position = "UTG"
        else:
            hero_position = positions[positions.index(hero_position)+1]
        display.new_round(winnings, hands_played)





if __name__ == "__main__":
    main()