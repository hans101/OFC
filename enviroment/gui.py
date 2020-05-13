from game import Card, Deck, OfcHand, FrontMidBotHand
from tkinter import *
from re import *
import os
from PIL import Image, ImageTk
from random import choice, randint

root = Tk()

deck = Deck()

# root config
root.geometry('1000x500')
root.title('OFC v 0.1')
root.configure(background='#222B12')

# first player frame config
first_player_frame = Frame(root, width=800, height=450)
first_player_frame.configure(background='#3E4D21')
first_player_frame.pack()
first_player_label = Label(first_player_frame, text='PLAYER 1')
first_player_label.place(x=375, y=0)

# place Canvas board
board = Canvas(first_player_frame, bg='black', width=700, height=420)
board.place(x=50, y=25)

# creating grid
board.create_line(0, 105, 700, 105, width=3, fill='grey', tag='linia')
board.create_line(0, 210, 700, 210, width=3, fill='grey')
board.create_line(0, 315, 700, 315, width=3, fill='grey')

board.create_line(165, 105, 165, 420, width=3, fill='grey')
board.create_line(235, 0, 235, 420, width=3, fill='grey')
board.create_line(305, 0, 305, 420, width=3, fill='grey')
board.create_line(375, 0, 375, 420, width=3, fill='grey')
board.create_line(445, 0, 445, 420, width=3, fill='grey')
board.create_line(515, 105, 515, 420, width=3, fill='grey')

# creating back card image
back_card_image = ImageTk.PhotoImage(Image.open("Cards/green_back.png"))
board.create_image(130, 370, image=back_card_image, tag='card_back', state=HIDDEN)
all_hand_cards = [deck.get_card() for card in range(1, 18)]
all_hand_cards.insert(0, back_card_image)

# switch to show/hide burned cards
switch = 0

# create set and reset button
button = Button(board, text='SET', state=DISABLED)
button.place(x=600, y=50)
button_reset = Button(board, text='RESET', state=DISABLED)
button_reset.place(x=590, y=15)


# function to create image on board
def create_new_card_image(card, x_position, y_position):
    board.create_image(x_position, y_position, image=card.representation(),
                       tags=('draw', 'bottom_row', 'reset', 'card' + str(card)))


# first draw(5 cards)
def first_draw():
    [create_new_card_image(all_hand_cards[i], (130 + (i * 70)), 370) for i in range(1, 6)]


# function returning card object of specified card image
def returning_card_of_image_object(image_object):
    image_name = board.itemcget(image_object, 'tags')
    result = re.search(r'\d+[A-Z]', image_name)
    card_index = all_hand_cards.index(result.group())
    card = all_hand_cards[card_index]
    return card


# setting in order objects in a chosen row
def row_reload(row, x_position, y_position):
    for i in range(0, len(row)):
        board.coords(row[i], (x_position + (i * 70)), y_position)


# setting all cards in all rows in order
def all_rows_reload(bottom_row, row1, row2, row3):
    if len(bottom_row) > 4:
        row_reload(bottom_row, 200, 370)
    else:
        row_reload(bottom_row, 270, 370)
    row_reload(row1, 200, 265)
    row_reload(row2, 200, 160)
    row_reload(row3, 270, 55)


# handle reset button
def reset():
    round_cards = board.find_withtag('reset')
    for card in round_cards:
        board.dtag(card, 'row1')
        board.dtag(card, 'row2')
        board.dtag(card, 'row3')
        card_tags = board.itemcget(card, 'tags') + ' bottom_row'
        board.itemconfig(card, tags=card_tags)
    row1 = board.find_withtag('row1')
    row2 = board.find_withtag('row2')
    row3 = board.find_withtag('row3')
    bottom_row = board.find_withtag('bottom_row')
    all_rows_reload(bottom_row, row1, row2, row3)
    button_reset.config(state=DISABLED)


# creating set button
def set_position():
    board.dtag('reset')
    row1 = board.find_withtag('row1')
    row2 = board.find_withtag('row2')
    row3 = board.find_withtag('row3')
    bottom_row = board.find_withtag('bottom_row')

    if bottom_row:
        board.addtag_withtag('burn', 'bottom_row')
        burned_cards = board.find_withtag('burn')
        for i in range(0, len(burned_cards)):
            board.itemconfig(burned_cards[i], tag='burn')
            board.itemconfig(burned_cards[i], state=HIDDEN)
            board.coords(burned_cards[i], (130 - i * 30), 370)

    card_number = len(row1) + len(row2) + len(row3)
    possible_cards_quantity = [5, 7, 9, 11, 13]

    card_back = board.find_withtag('card_back')

    if card_number in possible_cards_quantity:
        # placing cards on board
        if card_number == 5:
            board.dtag('draw')
            # second draw(3 cards)
            [create_new_card_image(all_hand_cards[i], (-150 + (i * 70)), 370) for i in range(6, 9)]
        elif card_number == 7:
            board.dtag('draw')
            board.itemconfig(card_back, state=NORMAL)
            # third draw(3 cards)
            [create_new_card_image(all_hand_cards[i], (-360 + (i * 70)), 370) for i in range(9, 12)]
        elif card_number == 9:
            board.dtag('draw')
            # fourth draw(3 cards)
            [create_new_card_image(all_hand_cards[i], (-570 + (i * 70)), 370) for i in range(12, 15)]
        elif card_number == 11:
            board.dtag('draw')
            # fifth_draw(5 cards)
            [create_new_card_image(all_hand_cards[i], (-780 + (i * 70)), 370) for i in range(15, 18)]
        elif card_number == 13:
            board.dtag('draw')

            top = [returning_card_of_image_object(card) for card in row3]
            mid = [returning_card_of_image_object(card) for card in row2]
            bottom = [returning_card_of_image_object(card) for card in row1]
            new_hand = OfcHand(top=top, bot=bottom, mid=mid)
            print(new_hand)
        button.config(state=DISABLED)
    else:
        pass


def card_move(event):
    x = board.canvasx(event.x)
    y = board.canvasy(event.y)
    lista = board.find_withtag('draw')
    selected_card = board.find_closest(x, y)[0]
    blocked_cards = board.find_withtag('blocked')
    if selected_card in lista:
        if selected_card not in blocked_cards:
            board.addtag_all('blocked')
            board.dtag(selected_card, 'blocked')
            board.coords(selected_card, x, y)


def tag_add(event):
    board.dtag('blocked')
    x = board.canvasx(event.x)
    y = board.canvasy(event.y)
    lista = board.find_withtag('draw')
    selected_card = board.find_closest(x, y)[0]
    if selected_card in lista:
        board.dtag(selected_card, 'row1')
        board.dtag(selected_card, 'row2')
        board.dtag(selected_card, 'row3')
        board.dtag(selected_card, 'bottom_row')
        board.addtag_enclosed('row1', 165, 165, 515, 350)
        board.addtag_enclosed('row2', 165, 75, 515, 250)
        board.addtag_enclosed('row3', 165, 0, 515, 150)
        board.addtag_enclosed('bottom_row', 165, 285, 515, 500)
        row1 = board.find_withtag('row1')
        row2 = board.find_withtag('row2')
        row3 = board.find_withtag('row3')
        bottom_row = board.find_withtag('bottom_row')
        if selected_card in row1 and len(row1) < 6:
            board.coords(selected_card, (130 + len(row1) * 70), 265)
            row_reload(row1, 200, 265)
        elif selected_card in row2 and len(row2) < 6:
            board.coords(selected_card, (130 + len(row2) * 70), 160)
            row_reload(row2, 200, 160)
        elif selected_card in row3 and len(row3) < 4:
            board.coords(selected_card, (200 + len(row3) * 70), 55)
            row_reload(row3, 270, 55)
        else:
            selected_card_tags = board.itemcget(selected_card, 'tags') + ' bottom_row'
            board.itemconfig(selected_card, tags=selected_card_tags)
            board.coords(selected_card, (130 + len(bottom_row) * 70), 370)
            row_reload(bottom_row, 200, 370)

        returning_card_of_image_object(selected_card)

        if (len(row1) + len(row2) + len(row3)) in [5, 7, 9, 11, 13] and len(bottom_row) in [0, 1]:
            button.config(state=NORMAL)
        else:
            button.config(state=DISABLED)

        row1 = board.find_withtag('row1')
        row2 = board.find_withtag('row2')
        row3 = board.find_withtag('row3')
        bottom_row = board.find_withtag('bottom_row')

        all_rows_reload(bottom_row, row1, row2, row3)

        this_round_cards = board.find_withtag('reset')

        for card in this_round_cards:
            if card in row1 or card in row2 or card in row3:
                button_reset.config(state=NORMAL)


def display_burned_cards(event):
    global switch
    switch += 1
    # show/hide burned cards:
    burned_cards = board.find_withtag('burn')
    if switch % 2 == 1:
        if burned_cards:
            for card in burned_cards:
                board.itemconfig(card, state=NORMAL)
    else:
        if burned_cards:
            for card in burned_cards:
                board.itemconfig(card, state=HIDDEN)


button.config(command=set_position)
button_reset.config(command=reset)

first_draw()

board.bind("<B1-Motion>", card_move)
board.bind('<ButtonRelease-1>', tag_add)
board.bind('<3>', display_burned_cards)

root.mainloop()
