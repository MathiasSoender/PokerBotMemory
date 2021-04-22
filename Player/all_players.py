# from Poker.ranking.hand_ranking import rank_hand
#from Poker.ranking.high_cards import HighCard
from Cython_pack.hand_rankings import rank_hand
from Cython_pack.highcards import HighCard
from Player.player_types import CO, BTN, MP, SB, BB, UTG
from Poker.ranking.hand_ranking import  find_rank_jit
from Poker.ranking.high_cards import toJitInputFindRank, HighCard_jit


class Players:
    def __init__(self, utg: UTG.UTG, bb: BB.BB, sb: SB.SB, mp: MP.MP, btn: BTN.BTN, co: CO.CO):
        self.UTG = utg
        self.BB = bb
        self.SB = sb
        self.MP = mp
        self.BTN = btn
        self.CO = co

        self.min_position = dict()
        self.min_position["preflop"] = 1
        self.min_position["postflop"] = 1

        self.max_position = dict()
        self.max_position["preflop"] = 6
        self.max_position["postflop"] = 6

        self.players = [self.SB, self.BB, self.UTG, self.MP, self.CO, self.BTN]

    def find_hero(self):
        if self.BB.hero:
            return self.BB
        if self.SB.hero:
            return self.SB
        if self.CO.hero:
            return self.CO
        if self.BTN.hero:
            return self.BTN
        if self.UTG.hero:
            return self.UTG
        if self.MP.hero:
            return self.MP


    def update_remaining(self):
        remain_players = []
        for player in self.players:
            if not player.folded:
                remain_players.append(player)

        self.min_position["preflop"] = 10
        self.min_position["postflop"] = 10
        self.max_position["preflop"] = 0
        self.max_position["postflop"] = 0
        for player in remain_players:
            self.min_position["preflop"] = min(player.position_preflop, self.min_position["preflop"])
            self.min_position["postflop"] = min(player.position_postflop, self.min_position["postflop"])

            self.max_position["preflop"] = max(player.position_preflop, self.max_position["preflop"])
            self.max_position["postflop"] = max(player.position_postflop, self.max_position["postflop"])

        self.players = remain_players

    def remaining_length(self):
        self.update_remaining()
        return len(self.players)

    def pot_size(self):
        pot = 0
        for player in [self.SB, self.BB, self.UTG, self.MP, self.CO, self.BTN]:
            pot += 100 - player.chips

        return pot

    def find_max_bet_player(self):
        self.update_remaining()

        m = -10
        m_player = None
        for player in self.players:
            if m < player.bet:
                m = player.bet
                m_player = player
        return m_player

    """ BB cannot open """
    def has_opened(self):
        for player in self.players:
            if player.name != "BB":
                if player.name == "SB":
                    if player.bet != 0.5:
                        return True
                else:
                    if player.bet != 0:
                        return True
        return False


    def find_player(self, name=None, position=None, preflop=False):
        self.update_remaining()

        if name is not None:
            for player in self.players:
                if player.name == name:
                    return player

        elif position is not None:
            for player in self.players:
                if preflop:
                    if player.position_preflop == position:
                        return player
                else:
                    if player.position_postflop == position:
                        return player

        return None

    def set_done_actions(self, val=False, reset_bets = False):
        self.update_remaining()
        for player in self.players:
            player.action_done = val
        if reset_bets:
            for player in self.players:
                player.bet = 0

    def done_actions(self):
        self.update_remaining()
        for player in self.players:
            if not player.action_done:
                return False
        return True

    def multiway(self):
        if self.remaining_length() > 2:
            return True


    def determine_winner(self, community=[]):

        max_rank = -1
        winning_players = []
        # Find rank of players hands
        for player in self.players:
            com, suits = toJitInputFindRank(player.hand, community)
            rank = find_rank_jit(com, suits)

            if rank > max_rank:
                winning_players = [player]

            elif rank == max_rank:
                winning_players.append(player)

            max_rank = max(rank, max_rank)

        # More players with same rank, find high cards combinations:
        if len(winning_players) > 1:
            highest_card_winning_players = [winning_players[0]]

            com, suits = toJitInputFindRank(winning_players[0].hand, community)
            max_cards = list(HighCard_jit(max_rank, com, suits))
            for player in winning_players[1:]:

                com, suits = toJitInputFindRank(player.hand, community)
                high_cards = list(HighCard_jit(max_rank, com, suits))
                # Same hand strength:
                if high_cards == max_cards:
                    highest_card_winning_players.append(player)

                else:
                    for i in range(0, len(max_cards)):
                        # Better high cards:
                        if high_cards[i] > max_cards[i]:
                            max_cards = high_cards
                            highest_card_winning_players = [player]
                            break
                        # Worse, skip:
                        elif high_cards[i] < max_cards[i]:
                            break

            return highest_card_winning_players

        return winning_players

    def __str__(self):
        out = []
        self.update_remaining()
        for player in self.players:
            out.append(str(player))
        return str(out)
