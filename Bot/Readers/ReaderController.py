from Bot.Readers.ReaderActions import ReaderActions
from Bot.Readers.ReaderCommunity import ReaderCommunity
from Bot.Readers.ReaderFolded import ReaderFolded
from Bot.Readers.ReaderHand import ReaderHand
from Bot.Readers.ReaderPosition import ReaderPosition
import multiprocessing as mp


class readerController:
    def __init__(self, ID):
        self.ID = ID
        self.readerHand = ReaderHand(ID)
        self.readerFolded = ReaderFolded(ID)
        self.readerCommunity = ReaderCommunity(ID)
        self.readerPosition = ReaderPosition(ID)
        self.readerActions = ReaderActions(ID)


        self.hand = None
        self.bets = None
        self.position = None
        self.folded = None
        self.order = None

        self.flop = []
        self.turn = []
        self.river = []


    def game_start_read(self, waitLoop):
        self.readerPosition.Read()
        self.position = self.readerPosition.Position
        self.order = self.readerPosition.order
        self.readerFolded.Read(self.order)
        self.folded = self.readerFolded.folded

        RAS, RASQueue = self.__start_RAS()

        self.readerHand.Read()
        self.bets = RASQueue.get()
        RAS.join()

        self.hand = self.readerHand.Hand

        waitLoop.setHand(self.hand, self.readerHand.Conf1, self.readerHand.Conf2)

    def intermediate_reads(self):
        self.readerFolded.Read(self.order)
        self.folded = self.readerFolded.folded
        self.readerActions.Read(self.order, self.folded)

        self.bets = self.readerActions.bets
        print("Intermediate reads done")

    def read_community(self, street):
        self.readerFolded.Read(self.order)
        self.folded = self.readerFolded.folded

        RAS, RASQueue = self.__start_RAS()

        if street == "flop":
            self.readerCommunity.ReadFlop()
            self.flop = self.readerCommunity.Flop
        elif street == "turn":
            self.readerCommunity.ReadTurn()
            self.turn = self.readerCommunity.Turn
        elif street == "river":
            self.readerCommunity.ReadRiver()
            self.river = self.readerCommunity.River

        self.bets = RASQueue.get()
        RAS.join()

    def __start_RAS(self):
        RASQueue = mp.Queue()
        RAS = mp.Process(target=reader_action_service, args=(RASQueue, self.readerActions, self.order,
                                                             self.folded))
        RAS.start()
        return RAS, RASQueue

def reader_action_service(queue, reader, player_order, player_folded):
    reader.Read(player_order, player_folded)
    queue.put(reader.bets)
    return
