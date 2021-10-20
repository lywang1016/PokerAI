from deckofcards import Deck

class Croupier(object):
    def __init__(self):
        self.player_num_total = 0
        self.current_player_num = 0
        self.seats = {}
        self.button_idx = 0
        self.player_queue = []
        self.deck = None

    def open_table(self, table_size):
        self.table_size = table_size
        self.current_player_num = 0
        self.button_idx = 0
        self.seats = {}
        for i in range(table_size):
            if i not in self.seats:
                self.seats[i] = None

    def get_first_available_seat(self):
        for seat_number in range(self.table_size):
            if self.seats[seat_number] == None:
                return seat_number
        return -1


    def add_player(self, player):
        if self.current_player_num < self.table_size:
            available_seat = self.get_first_available_seat()
            self.seats[available_seat] = player.name
            self.current_player_num += 1
            self.button_idx = 0
            player.seat_num = available_seat

    def drop_player(self, player):
        self.seats[player.seat_num] = None
        self.current_player_num -= 1
        self.button_idx = 0
        player.seat_num = -1

    def prepare_deck(self):
        self.deck = Deck()
        self.deck.shuffle()

    def asign_player_position(self):
        self.player_queue = []
        for seat_number in range(self.table_size):
            if self.seats[seat_number] != None:
                self.player_queue.append(self.seats[seat_number])

        if len(self.player_queue) == self.current_player_num:
            self.button_idx += 1
            if self.button_idx == self.current_player_num:
                self.button_idx = 0

            if self.current_player_num == 2:
                if self.button_idx == 0:
                    b_idx = 0
                    sb_idx = 0
                    bb_idx = 1
                else:
                    b_idx = 1
                    sb_idx = 1
                    bb_idx = 0
                return b_idx, sb_idx, bb_idx
            else:
                for i in range(self.current_player_num):
                    b_idx = self.button_idx+i
                    sb_idx = self.button_idx+i+1
                    bb_idx = self.button_idx+i+2
                    if b_idx > self.current_player_num-1:
                        b_idx -= self.current_player_num
                    if sb_idx > self.current_player_num-1:
                        sb_idx -= self.current_player_num
                    if bb_idx > self.current_player_num-1:
                        bb_idx -= self.current_player_num
                return b_idx, sb_idx, bb_idx

    def deal_hand_cards(self):
        self.prepare_deck()
        b_idx, sb_idx, bb_idx = self.asign_player_position()
        player_cards = {}
        bfo = []    # before flop action order
        afo = []    # after flop action order
        if b_idx == sb_idx: # 2 players
            sbb_name = self.player_queue[sb_idx]
            bb_name = self.player_queue[bb_idx]
            bfo = [sbb_name, bb_name]
            afo = [bb_name, sbb_name]
            for deal_round in range(2):
                card = self.deck.draw()
                if sbb_name not in player_cards:
                    player_cards[sbb_name] = [card]
                else:
                    player_cards[sbb_name].append(card)
                card = self.deck.draw()
                if bb_name not in player_cards:
                    player_cards[bb_name] = [card]
                else:
                    player_cards[bb_name].append(card)
        else:
            for deal_round in range(2):
                for i in range(sb_idx, sb_idx+self.current_player_num):
                    idx = i
                    if idx > self.current_player_num-1:
                        idx -= self.current_player_num
                    name = self.player_queue[idx]
                    if deal_round == 0:
                        afo.append(name)
                    card = self.deck.draw()
                    if name not in player_cards:
                        player_cards[name] = [card]
                    else:
                        player_cards[name].append(card)  
            for i in range(len(afo)-2):
                bfo.append(afo[i+2])
            bfo.append(afo[0])
            bfo.append(afo[1])
        return player_cards, bfo, afo

    def burn_card(self):
        self.deck.draw()
    
    def deal_flop(self):
        self.burn_card()
        flop_cards = []
        card = self.deck.draw()
        flop_cards.append(card)
        card = self.deck.draw()
        flop_cards.append(card)
        card = self.deck.draw()
        flop_cards.append(card)
        return flop_cards

    def deal_turn(self):
        self.burn_card()
        return self.deck.draw()

    def deal_river(self):
        self.burn_card()
        return self.deck.draw()
                        
                

                


    

    

    


