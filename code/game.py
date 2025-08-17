import random
from mtg_mill_simulation.code.deck import initialize_deck
from mtg_mill_simulation.code.actions import my_mulligan, my_turn_1, op_turn_1, my_turn_n, op_turn_n



def game(removal_prio:float=0)->dict:
    """Simulates a Modern format Mill Magic the Gathering game.

    Parameters:
        removal_prio: float, default=0

    Returns:
        dict:{
        "game_number": None(inputed in the sim),
        "start": "str",
        "kill_turn": float|None,
        "actions": list
        }"""
    # Check if we are "on the play" or "on the draw"
    coin_toss=random.randint(0,1)
    if coin_toss==1:
        start="On the play!"
    else:
        start="On the draw!"
    # Initialize game variables
    op_grave_size=0
    op_deck_size=53
    board_lands=[]
    board_creatures=[]
    game_actions=[]
    deck=initialize_deck()#Load the deck
    hand=my_mulligan(deck, game_actions)#Mulligan
    if hand is None:#Breaks the game because it mulliganed to many times
        return {
        "game_number": None,
        "start": "On the play!" if coin_toss == 1 else "On the draw!",
        "kill_turn": None,
        "actions": game_actions
        }
    op_turn_count=0
    my_turn_count=0
    #turn loop while "on the play"
    if coin_toss==1:
        my_turn_count, op_deck_size, op_grave_size=my_turn_1(hand, board_lands, board_creatures, game_actions, deck, op_deck_size, op_grave_size)
        op_lost=False
        while not op_lost:
            op_turn_count, op_deck_size, op_grave_size, op_lost=op_turn_n(op_turn_count, game_actions,op_deck_size,op_grave_size)
            if op_lost==True:
                break
            my_turn_count, op_deck_size, op_grave_size=my_turn_n(my_turn_count,hand,board_lands,board_creatures,game_actions,deck,op_deck_size,op_grave_size)
    #turn loop while "on the draw"
    else:
        op_turn_count=op_turn_1(game_actions,op_turn_count)
        op_lost=False
        while not op_lost:
            my_turn_count, op_deck_size, op_grave_size=my_turn_n(my_turn_count,hand,board_lands,board_creatures,game_actions,deck,op_deck_size,op_grave_size)
            op_turn_count, op_deck_size, op_grave_size, op_lost=op_turn_n(op_turn_count, game_actions,op_deck_size,op_grave_size)
            if op_lost==True:
                break
    kill_turn=op_turn_count
    return {
        "game_number": None,
        "start": start,
        "kill_turn": kill_turn,
        "actions": game_actions
    }
