from game import Card, Deck, OfcHand, FrontMidBotHand
from tkinter import *
from re import *
import os
from PIL import Image, ImageTk
from random import choice, randint


class Game:

    def __init__(self, root):
        self.root = root
        self.deck = None
        self.first_player_frame = None
        self.board = None
        self.set_button = None
        self.button_reset = None
        self.switch = None
        self.all_hand_cards = None

        self.board_prepare()
        self.new_hand()

    def create_deck(self):
        self.deck = Deck()
        # creating back card image
        back_card_image = ImageTk.PhotoImage(Image.open("Cards/green_back.png"))
        self.board.create_image(130, 370, image=back_card_image, tags=('card_back', 'this'), state=HIDDEN)
        self.all_hand_cards = [self.deck.get_card() for _ in range(1, 18)]
        self.all_hand_cards.insert(0, back_card_image)

    def board_prepare(self):
        # root config
        self.root.geometry('1000x500')
        self.root.title('OFC v 0.1')
        self.root.configure(background='#222B12')

        # first player frame config
        self.first_player_frame = Frame(root, width=800, height=450)
        self.first_player_frame.configure(background='#3E4D21')
        self.first_player_frame.pack()
        first_player_label = Label(self.first_player_frame, text='PLAYER 1')
        first_player_label.place(x=375, y=0)

        # place Canvas board
        self.board = Canvas(self.first_player_frame, bg='black', width=700, height=420)
        self.board.place(x=50, y=25)

        # creating grid
        self.board.create_line(0, 105, 700, 105, width=3, fill='grey')
        self.board.create_line(0, 210, 700, 210, width=3, fill='grey')
        self.board.create_line(0, 315, 700, 315, width=3, fill='grey')

        self.board.create_line(165, 105, 165, 420, width=3, fill='grey')
        self.board.create_line(235, 0, 235, 420, width=3, fill='grey')
        self.board.create_line(305, 0, 305, 420, width=3, fill='grey')
        self.board.create_line(375, 0, 375, 420, width=3, fill='grey')
        self.board.create_line(445, 0, 445, 420, width=3, fill='grey')
        self.board.create_line(515, 105, 515, 420, width=3, fill='grey')

        # switch to show/hide burned cards
        self.switch = 0

        # create set and reset button
        self.set_button = Button(self.board, text='SET', state=DISABLED)
        self.set_button.place(x=600, y=50)
        self.button_reset = Button(self.board, text='RESET', state=DISABLED)
        self.button_reset.place(x=590, y=15)

    # function to create image on board
    def create_new_card_image(self, card, x_position, y_position):
        self.board.create_image(x_position, y_position, image=card.representation(),
                                tags=('draw', 'bottom_row', 'reset', 'this', 'card' + str(card)))

    # first draw(5 cards)
    def first_draw(self):
        [self.create_new_card_image(self.all_hand_cards[i], (130 + (i * 70)), 370) for i in range(1, 6)]

    # function returning card object of specified card image
    def returning_card_of_image_object(self, image_object):
        image_name = self.board.itemcget(image_object, 'tags')
        result = re.search(r'\d+[A-Z]', image_name)
        card_index = self.all_hand_cards.index(result.group())
        card = self.all_hand_cards[card_index]
        return card

    # setting in order objects in a chosen row
    def row_reload(self, row, x_position, y_position):
        for i in range(0, len(row)):
            self.board.coords(row[i], (x_position + (i * 70)), y_position)

    # setting all cards in all rows in order
    def all_rows_reload(self, bottom_row, row1, row2, row3):
        if len(bottom_row) > 4:
            self.row_reload(bottom_row, 200, 370)
        else:
            self.row_reload(bottom_row, 270, 370)
            self.row_reload(row1, 200, 265)
            self.row_reload(row2, 200, 160)
            self.row_reload(row3, 270, 55)

    # handle reset button
    def reset(self):
        round_cards = self.board.find_withtag('reset')
        for card in round_cards:
            self.board.dtag(card, 'row1')
            self.board.dtag(card, 'row2')
            self.board.dtag(card, 'row3')
            card_tags = self.board.itemcget(card, 'tags') + ' bottom_row'
            self.board.itemconfig(card, tags=card_tags)
        row1 = self.board.find_withtag('row1')
        row2 = self.board.find_withtag('row2')
        row3 = self.board.find_withtag('row3')
        bottom_row = self.board.find_withtag('bottom_row')
        self.all_rows_reload(bottom_row, row1, row2, row3)
        self.button_reset.config(state=DISABLED)

    # creating set button
    def set_position(self):
        self.board.dtag('reset')
        row1 = self.board.find_withtag('row1')
        row2 = self.board.find_withtag('row2')
        row3 = self.board.find_withtag('row3')
        bottom_row = self.board.find_withtag('bottom_row')

        if bottom_row:
            self.board.addtag_withtag('burn', 'bottom_row')
            burned_cards = self.board.find_withtag('burn')
            for i in range(0, len(burned_cards)):
                self.board.itemconfig(burned_cards[i], tag='burn')
                self.board.itemconfig(burned_cards[i], state=HIDDEN)
                self.board.coords(burned_cards[i], (130 - i * 30), 370)

        card_number = len(row1) + len(row2) + len(row3)
        possible_cards_quantity = [5, 7, 9, 11, 13]

        card_back = self.board.find_withtag('card_back')

        if card_number in possible_cards_quantity:
            # placing cards on board
            if card_number == 5:
                self.board.dtag('draw')
                # second draw(3 cards)
                [self.create_new_card_image(self.all_hand_cards[i], (-150 + (i * 70)), 370) for i in range(6, 9)]
            elif card_number == 7:
                self.board.dtag('draw')
                self.board.itemconfig(card_back, state=NORMAL)
                # third draw(3 cards)
                [self.create_new_card_image(self.all_hand_cards[i], (-360 + (i * 70)), 370) for i in range(9, 12)]
            elif card_number == 9:
                self.board.dtag('draw')
                # fourth draw(3 cards)
                [self.create_new_card_image(self.all_hand_cards[i], (-570 + (i * 70)), 370) for i in range(12, 15)]
            elif card_number == 11:
                self.board.dtag('draw')
                # fifth_draw(5 cards)
                [self.create_new_card_image(self.all_hand_cards[i], (-780 + (i * 70)), 370) for i in range(15, 18)]
            elif card_number == 13:
                self.board.dtag('draw')

                top = [self.returning_card_of_image_object(card) for card in row3]
                mid = [self.returning_card_of_image_object(card) for card in row2]
                bottom = [self.returning_card_of_image_object(card) for card in row1]
                new_hand = OfcHand(top=top, bot=bottom, mid=mid)
                print(new_hand)

                self.delete_all_cards()
                self.hand_reset()
                self.new_hand()

            self.set_button.config(state=DISABLED)
        else:
            pass

    def card_move(self, event):
        x = self.board.canvasx(event.x)
        y = self.board.canvasy(event.y)
        this_round_cards = self.board.find_withtag('draw')
        selected_card = self.board.find_closest(x, y)[0]
        blocked_cards = self.board.find_withtag('blocked')
        if selected_card in this_round_cards:
            if selected_card not in blocked_cards:
                self.board.addtag_all('blocked')
                self.board.dtag(selected_card, 'blocked')
                self.board.coords(selected_card, x, y)

    def tag_add(self, event):
        self.board.dtag('blocked')
        x = self.board.canvasx(event.x)
        y = self.board.canvasy(event.y)
        this_round_cards = self.board.find_withtag('draw')
        selected_card = self.board.find_closest(x, y)[0]
        if selected_card in this_round_cards:
            self.board.dtag(selected_card, 'row1')
            self.board.dtag(selected_card, 'row2')
            self.board.dtag(selected_card, 'row3')
            self.board.dtag(selected_card, 'bottom_row')
            self.board.addtag_enclosed('bottom_row', 165, 275, 515, 485)
            self.board.addtag_enclosed('row1', 165, 165, 515, 345)
            self.board.addtag_enclosed('row2', 165, 55, 515, 255)
            self.board.addtag_enclosed('row3', 165, -53, 515, 150)
            row1 = self.board.find_withtag('row1')
            row2 = self.board.find_withtag('row2')
            row3 = self.board.find_withtag('row3')
            bottom_row = self.board.find_withtag('bottom_row')
            if selected_card in row1:
                self.board.coords(selected_card, (130 + len(row1) * 70), 265)
                if len(row1) == 6:
                    self.board.dtag(selected_card, 'row1')
                    selected_card_tags = self.board.itemcget(selected_card, 'tags') + ' bottom_row'
                    self.board.itemconfig(selected_card, tags=selected_card_tags)
                self.row_reload(row1, 200, 265)
            elif selected_card in row2:
                self.board.coords(selected_card, (130 + len(row2) * 70), 160)
                if len(row2) == 6:
                    self.board.dtag(selected_card, 'row2')
                    selected_card_tags = self.board.itemcget(selected_card, 'tags') + ' bottom_row'
                    self.board.itemconfig(selected_card, tags=selected_card_tags)
                self.row_reload(row1, 200, 160)
            elif selected_card in row3:
                self.board.coords(selected_card, (200 + len(row3) * 70), 55)
                if len(row3) == 4:
                    self.board.dtag(selected_card, 'row3')
                    selected_card_tags = self.board.itemcget(selected_card, 'tags') + ' bottom_row'
                    self.board.itemconfig(selected_card, tags=selected_card_tags)
                self.row_reload(row3, 270, 55)
            else:
                self.board.dtag(selected_card, 'row1')
                self.board.dtag(selected_card, 'row2')
                self.board.dtag(selected_card, 'row3')
                selected_card_tags = self.board.itemcget(selected_card, 'tags') + ' bottom_row'
                self.board.itemconfig(selected_card, tags=selected_card_tags)
                self.board.coords(selected_card, (130 + len(bottom_row) * 70), 370)
                self.row_reload(bottom_row, 200, 370)

            self.returning_card_of_image_object(selected_card)

            row1 = self.board.find_withtag('row1')
            row2 = self.board.find_withtag('row2')
            row3 = self.board.find_withtag('row3')
            bottom_row = self.board.find_withtag('bottom_row')

            if (len(row1) + len(row2) + len(row3)) in [5, 7, 9, 11, 13] and len(bottom_row) in [0, 1]:
                self.set_button.config(state=NORMAL)
            else:
                self.set_button.config(state=DISABLED)

            self.all_rows_reload(bottom_row, row1, row2, row3)

            this_round_cards = self.board.find_withtag('reset')

            for card in this_round_cards:
                if card in row1 or card in row2 or card in row3:
                    self.button_reset.config(state=NORMAL)

    def display_burned_cards(self, event):
        self.switch += 1
        # show/hide burned cards:
        burned_cards = self.board.find_withtag('burn')
        if self.switch % 2 == 1:
            if burned_cards:
                for card in burned_cards:
                    self.board.itemconfig(card, state=NORMAL)
        else:
            if burned_cards:
                for card in burned_cards:
                    self.board.itemconfig(card, state=HIDDEN)

    def hand_reset(self):
        previous_round_cards = self.board.find_withtag('this')
        for card in previous_round_cards:
            self.board.dtag('row1')
            self.board.dtag('row2')
            self.board.dtag('row3')
            self.board.dtag('bottom_row')
            self.board.dtag('burn')
            self.board.delete(card)
        self.deck = None
        self.all_hand_cards = None

    def delete_all_cards(self):
        for card in self.all_hand_cards:
            self.board.delete(card)

    def new_hand(self):
        self.hand_reset()
        self.create_deck()

        self.set_button.config(command=self.set_position)
        self.button_reset.config(command=self.reset)

        self.first_draw()

        self.board.bind("<B1-Motion>", self.card_move)
        self.board.bind('<ButtonRelease-1>', self.tag_add)
        self.board.bind('<3>', self.display_burned_cards)


root = Tk()

Game(root)

root.mainloop()
