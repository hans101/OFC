from game import Card, Deck, OfcHand
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

# first round/dealing 5 cards
all_hand_cards = [deck.get_card() for card in range(1, 18)]

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

# placing cards on board
board.create_image(200, 370, image=all_hand_cards[0].representation(), tags=('draw',))
board.create_image(270, 370, image=all_hand_cards[1].representation(), tags=('draw',))
board.create_image(340, 370, image=all_hand_cards[2].representation(), tags=('draw',))
board.create_image(410, 370, image=all_hand_cards[3].representation(), tags=('draw',))
board.create_image(480, 370, image=all_hand_cards[4].representation(), tags=('draw',))


def returning_card_of_image_object(image_object):
    image_name = board.itemcget(image_object, 'image')
    result = re.search(r'\d+', image_name)
    card = all_hand_cards[int(result.group())-1]
    return card

for cardd in board.find_withtag('draw'):
    print(returning_card_of_image_object(cardd))

# creating set button
def set_position():
    row1 = board.find_withtag('row1')
    row2 = board.find_withtag('row2')
    row3 = board.find_withtag('row3')

    card_number = len(row1) + len(row2) + len(row3)

    # placing cards on board
    if card_number == 5:
        board.dtag('draw')
        board.create_image(200, 365, image=all_hand_cards[5].representation(), tags=('draw',))
        board.create_image(270, 365, image=all_hand_cards[6].representation(), tags=('draw',))
        board.create_image(340, 365, image=all_hand_cards[7].representation(), tags=('draw',))
    elif card_number == 7:
        board.dtag('draw')
        board.create_image(200, 365, image=all_hand_cards[8].representation(), tags=('draw',))
        board.create_image(270, 365, image=all_hand_cards[9].representation(), tags=('draw',))
        board.create_image(340, 365, image=all_hand_cards[10].representation(), tags=('draw',))
    elif card_number == 9:
        board.dtag('draw')
        board.create_image(200, 365, image=all_hand_cards[11].representation(), tags=('draw',))
        board.create_image(270, 365, image=all_hand_cards[12].representation(), tags=('draw',))
        board.create_image(340, 365, image=all_hand_cards[13].representation(), tags=('draw',))
    elif card_number == 11:
        board.dtag('draw')
        board.create_image(200, 365, image=all_hand_cards[14].representation(), tags=('draw',))
        board.create_image(270, 365, image=all_hand_cards[15].representation(), tags=('draw',))
        board.create_image(340, 365, image=all_hand_cards[16].representation(), tags=('draw',))
    elif card_number == 13:
        board.dtag('draw')

        top = [returning_card_of_image_object(card) for card in row3]
        mid = [returning_card_of_image_object(card) for card in row2]
        bottom = [returning_card_of_image_object(card) for card in row1]
        new_hand = OfcHand(top=top, bot=bottom, mid=mid)
        print(new_hand)


button = Button(board, text='SET', command=set_position)
button.place(x=600, y=50)


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
        board.addtag_enclosed('row1', 165, 165, 515, 350)
        board.addtag_enclosed('row2', 165, 75, 515, 250)
        board.addtag_enclosed('row3', 165, 0, 515, 150)
        row1 = board.find_withtag('row1')
        row2 = board.find_withtag('row2')
        row3 = board.find_withtag('row3')
        drew_row = board.find_withtag('drew')
        if selected_card in row1:
            board.coords(selected_card, (130 + len(row1) * 70), 265)
        elif selected_card in row2:
            board.coords(selected_card, (130 + len(row2) * 70), 160)
        elif selected_card in row3:
            board.coords(selected_card, (200 + len(row3) * 70), 55)
        else:
            board.coords(selected_card, (130 + len(drew_row) * 70), 370)


board.bind("<B1-Motion>", card_move)
board.bind('<ButtonRelease-1>', tag_add)

root.mainloop()
