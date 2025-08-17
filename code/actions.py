import random
from collections import Counter
from mtg_mill_simulation.code.cards import card
from itertools import combinations
import mtg_mill_simulation.code.game_params as game_params
from typing import Optional

###############################################################################
#                               GENERAL ACTIONS
###############################################################################
def untap_all_lands(board_lands: list[card], game_actions:list)->None:
    """Untaps all lands on the battlefield,
    making their attribute card.tapped=False.

    Parameters:
        board_lands: list[card]
        game_actions: list

    """
    for land in board_lands:
        setattr(land, "tapped", False)
    game_actions.append("Untapped all lands.")

###############################################################################

def exile_from_deck(op_deck_size:int,n:int)->int:
    """Exiles n cards from the top of the oponent's deck
    updating his/her deck size.

    Parameters:
        op_deck_size: int
        n: int

    Returns:
        op_deck_size: int"""
    op_deck_size -= n
    return op_deck_size

###############################################################################

def mill(op_deck_size:int, n:int, op_grave_size:int)-> tuple[int,int]:
    """Mills n cards from the top of the oponent's deck
    updating his/her deck size and graveyard size.

    Parameters:
        op_deck_size: int
        n: int
        op_grave_size: int
    Returns:
        tuple:
        (op_deck_size: int, op_grave_size: int)

        """
    op_deck_size -= n
    op_grave_size += n
    return op_deck_size, op_grave_size

##############################################################################

def removal(n:int, op_grave_size:int)->int:
    """Removes a card from the opponents board/stack
    updating his/her graveyard size.

    Parameters:
        n: int
        op_grave_size: int

    Returns:
        op_grave_size: int
        """
    op_grave_size += n
    return op_grave_size

#############################################################################

def filter_cards(cards:list[card],attribute_name:str,value:bool)->list[card]:
    """Filters a list of cards by a specific boolean attribute.

    Parameters:
        cards: list[card]
        attribute_name: str
        value: bool

    Returns:
        list[card]
        """
    return [card for card in cards if getattr(card, attribute_name, value) == value]

#############################################################################

def draw(n:int, hand:list[card],
         deck:list[card],
         game_actions:list,
         log_actions:bool = True)->None:
    """Draw n cards from the top of the deck to the end of the hand

    Parameters:
        n: int
        hand: list[card]
        game_actions: list
        log_actions: bool, logs draws into game_actions, default=True

    """

    for _ in range(min(n, len(deck))):
        if log_actions == True:
            game_actions.append(f"Draw {deck[0].name}.")
        hand.append(deck.pop(0))

###############################################################################
#                               GAME/TURN ACTIONS
###############################################################################

def my_mulligan(deck:list[card],game_actions:list[str])->Optional[list[card]]:
    """Mulligan logic for a deck of cards. Returns a hand with 2-3 lands and
    the rest non-lands with card loss due to mulligans. This function simulates
    the mulligan process, ensuring that the player has a playable hand with a
    reasonable number of lands. If the hand isn't playable after four
    mulligans, the game is forfeit and the function returns None.

    Parameters:
        deck: list[card]
        game_actions: list

    Returns:
        hand: (list[card]|None)
    """
    hand=[]
    random.shuffle(deck)
    draw(7,hand,deck,game_actions,log_actions=False)
    lands_in_hand=filter_cards(hand,"land",True)
    if 2 <= len(lands_in_hand) <=3:
        cards_in_hand=[card.name for card in hand]
        game_actions.append(
            f"""{len(lands_in_hand)} Lands in hand(
                {[land.name for land in lands_in_hand]}).
                Kept hand with {cards_in_hand}.""")
        return hand
    else:
        deck.extend(hand)
        hand.clear()
        random.shuffle(deck)
        draw(7,hand,deck,game_actions,log_actions=False)
        lands_in_hand=filter_cards(hand,"land",True)
        if len(lands_in_hand)==4:
            lands_in_hand=filter_cards(hand,"land",True)
            deck.append(lands_in_hand[0])
            hand.remove(lands_in_hand[0])
            cards_in_hand=[card.name for card in hand]
            lands_in_hand=filter_cards(hand,"land",True)
            game_actions.append(
                f"""{len(lands_in_hand)} Lands in hand(
                    {[land.name for land in lands_in_hand]}).
                    Mulliganed once, kept hand with {cards_in_hand}.""")
        elif 2<=len(lands_in_hand)<=3:
            nonlands_in_hand=filter_cards(hand,"land",False)
            nonlands_in_hand.sort(key=lambda card: card.prio_nat)
            deck.append(nonlands_in_hand[0])
            hand.remove(nonlands_in_hand[0])
            lands_in_hand=filter_cards(hand,"land",True)
            cards_in_hand=[card.name for card in hand]
            game_actions.append(
                f"""{len(lands_in_hand)} Lands in hand(
                    {[land.name for land in lands_in_hand]}).
                    Mulliganed once, kept hand with {cards_in_hand}.""")
        else:
            deck.extend(hand)
            hand.clear()
            random.shuffle(deck)
            draw(7,hand,deck,game_actions,log_actions=False)
            lands_in_hand=filter_cards(hand,"land",True)
            if 4<=len(lands_in_hand)<=5:
                deck.append(lands_in_hand[0])
                hand.remove(lands_in_hand[0])
                lands_in_hand=filter_cards(hand,"land",True)
                deck.append(lands_in_hand[0])
                hand.remove(lands_in_hand[0])
                lands_in_hand=filter_cards(hand,"land",True)
                cards_in_hand=[card.name for card in hand]
                game_actions.append(
                    f"""{len(lands_in_hand)} Lands in hand(
                        {[land.name for land in lands_in_hand]}).
                        Mulliganed twice, kept hand with {cards_in_hand}.""")
            elif len(lands_in_hand)==3:
                nonlands_in_hand=filter_cards(hand,"land",False)
                nonlands_in_hand.sort(key=lambda card: card.prio_nat)
                deck.append(nonlands_in_hand[0])
                hand.remove(nonlands_in_hand[0])
                lands_in_hand=filter_cards(hand,"land",True)
                deck.append(lands_in_hand[0])
                hand.remove(lands_in_hand[0])
                lands_in_hand=filter_cards(hand,"land",True)
                cards_in_hand=[card.name for card in hand]
                game_actions.append(
                    f"""{len(lands_in_hand)} Lands in hand(
                        {[land.name for land in lands_in_hand]}).
                        Mulliganed twice, kept hand with {cards_in_hand}.""")
            elif len(lands_in_hand)==2:
                nonlands_in_hand=filter_cards(hand,"land",False)
                nonlands_in_hand.sort(key=lambda card: card.prio_nat)
                deck.append(nonlands_in_hand[0])
                hand.remove(nonlands_in_hand[0])
                nonlands_in_hand=filter_cards(hand,"land",False)
                nonlands_in_hand.sort(key=lambda card: card.prio_nat)
                deck.append(nonlands_in_hand[0])
                hand.remove(nonlands_in_hand[0])
                lands_in_hand=filter_cards(hand,"land",True)
                cards_in_hand=[card.name for card in hand]
                game_actions.append(
                    f"""{len(lands_in_hand)} Lands in hand(
                        {[land.name for land in lands_in_hand]}).
                        Mulliganed twice, kept hand with {cards_in_hand}.""")
            else:
                deck.extend(hand)
                hand.clear()
                random.shuffle(deck)
                draw(7,hand,deck,game_actions,log_actions=False)
                lands_in_hand=filter_cards(hand,"land",True)
                if 5<=len(lands_in_hand)<=6:
                    deck.append(lands_in_hand[0])
                    hand.remove(lands_in_hand[0])
                    lands_in_hand=filter_cards(hand,"land",True)
                    deck.append(lands_in_hand[0])
                    hand.remove(lands_in_hand[0])
                    lands_in_hand=filter_cards(hand,"land",True)
                    deck.append(lands_in_hand[0])
                    hand.remove(lands_in_hand[0])
                    lands_in_hand=filter_cards(hand,"land",True)
                    cards_in_hand=[card.name for card in hand]
                    game_actions.append(
                        f"""{len(lands_in_hand)} Lands in hand(
                            {[land.name for land in lands_in_hand]}).
                            Mulliganed trice,
                            kept hand with {cards_in_hand}.""")
                elif len(lands_in_hand)==4:
                    deck.append(lands_in_hand[0])
                    hand.remove(lands_in_hand[0])
                    lands_in_hand=filter_cards(hand,"land",True)
                    deck.append(lands_in_hand[0])
                    hand.remove(lands_in_hand[0])
                    nonlands_in_hand=filter_cards(hand,"land",False)
                    nonlands_in_hand.sort(key=lambda card: card.prio_nat)
                    deck.append(nonlands_in_hand[0])
                    hand.remove(nonlands_in_hand[0])
                    lands_in_hand=filter_cards(hand,"land",True)
                    cards_in_hand=[card.name for card in hand]
                    game_actions.append(
                        f"""{len(lands_in_hand)} Lands in hand(
                            {[land.name for land in lands_in_hand]}).
                            Mulliganed trice,
                            kept hand with {cards_in_hand}.""")
                elif len(lands_in_hand)==2:
                    nonlands_in_hand=filter_cards(hand,"land",False)
                    nonlands_in_hand.sort(key=lambda card: card.prio_nat)
                    deck.append(nonlands_in_hand[0])
                    hand.remove(nonlands_in_hand[0])
                    nonlands_in_hand=filter_cards(hand,"land",False)
                    nonlands_in_hand.sort(key=lambda card: card.prio_nat)
                    deck.append(nonlands_in_hand[0])
                    hand.remove(nonlands_in_hand[0])
                    nonlands_in_hand=filter_cards(hand,"land",False)
                    nonlands_in_hand.sort(key=lambda card: card.prio_nat)
                    deck.append(nonlands_in_hand[0])
                    hand.remove(nonlands_in_hand[0])
                    lands_in_hand=filter_cards(hand,"land",True)
                    cards_in_hand=[card.name for card in hand]
                    game_actions.append(
                        f"""{len(lands_in_hand)} Lands in hand(
                            {[land.name for land in lands_in_hand]}).
                            Mulliganed trice,
                            kept hand with {cards_in_hand}.""")
                else:
                    game_actions.append(f"""Mulliganed four times and
                                        forfit the game.""")
                    return None
    lands_in_hand=filter_cards(hand,"land",True)
    if len(lands_in_hand) <2:
        print("ERROR")
    return hand

##############################################################################

def parse_mana_cost(cost_str: str| None) -> dict[str, int]:
    """
    Parses something like "1UB" into {'U':1, 'B':1, 'generic':1}.
    Generic (including numeric) goes under 'generic'.

    Parameters:
        cost_str: str|None

    Returns:
        dict:{str: int}
    """
    if cost_str==None:
        return {'generic':90}
    result = Counter()
    digits = ''
    for c in cost_str:
        if c.isdigit():
            digits += c
        else:
            if digits:
                result['generic'] += int(digits)
                digits = ''
            result[c] += 1
    if digits:
        result['generic'] += int(digits)
    return dict(result)

##############################################################################

def can_pay_cost(mana_pool:list[str], mana_cost: dict[str, int]) -> bool:
    """Checks if mana_pool can pay mana_cost.
    'ANY' is wildcard usable for colored or generic.

    Parameters:
        mana_pool: list[str]
        mana_cost: dict:{str: int}

    Returns:
        bool
    """
    pool = Counter(mana_pool)
    wild = pool.pop('ANY', 0)
    need = mana_cost.copy()

    # Pay colored symbols first
    for symbol, required in list(need.items()):
        if symbol == 'generic':
            continue
        available = pool.get(symbol, 0)
        use = min(available, required)
        pool[symbol] -= use
        need[symbol] -= use
        if need[symbol] > 0 and wild > 0:
            take = min(need[symbol], wild)
            need[symbol] -= take
            wild -= take

    # If any colored remains, fail
    for sym, remaining in need.items():
        if sym != 'generic' and remaining > 0:
            return False

    # Pay generic
    generic_needed = need.get('generic', 0)
    leftover_specific = sum(v for v in pool.values() if v > 0)
    return leftover_specific + wild >= generic_needed

##############################################################################

def land_flexibility(land:card)->int:
    """Calculates the number of different colors of mana a land can produce.

    Parameters:
        land: card

    Returns:
        int
        """
    return len(set(land.mana_gen))

#############################################################################

def find_best_land_combination(
    available_lands: list[card],
    mana_cost: dict[str, int]
) -> Optional[list[card]]:
    """Finds the best land combination to cast a spell by prefering
    smallest combo size; among ties, maximizes leftover land flexibility.
    Only considers untapped lands with .land == True.

    Parameters:
        available_lands: list[card],
        mana_cost: dict[str, int]

    Returns:
    (best_combo, leftover_types_score)|None.

    """
    untapped = [l for l in available_lands if getattr(l,
                'land', False) and not getattr(l, 'tapped', True)]
    best_combo = None
    best_score = -1

    for size in range(1, len(untapped) + 1):
        for combo in combinations(untapped, size):
            pool = []
            for land in combo:
                pool.extend(getattr(land, 'mana_gen', []))
            if can_pay_cost(pool, mana_cost):
                score = -sum(land_flexibility(l) for l in combo)
                if best_combo is None or score > best_score:
                    best_combo = list(combo)
                    best_score = score
        if best_combo:
            break

    if best_combo:
        return best_combo
    return None

###############################################################################

def resolve_fetch_land(card:card,
                       board_lands:list[card],
                       deck:list[card],
                       game_actions:list[str])-> bool:
    """
    Resolves a fetch land (fetch) and fetching a
    land from the deck in priority order.

    Parameters:
        card: card
        board_lands: list[card]
        deck: list[card]
        game_actions: list
    Returns:
        bool: True if a land was fetched and sacrificed, False otherwise.
    """
    fetch_priority=["Watery Grave", "Island", "Swamp","Undercity Sewers"]

    # Sacrifice the land
    if card in board_lands:
        board_lands.remove(card)

    # Search the deck for a land by priority
    for name in fetch_priority:
        for i, deck_card in enumerate(deck):
            if deck_card.name == name and deck_card.land:
                # Put into play tapped
                fetched = deck.pop(i)
                board_lands.append(fetched)
                game_actions.append(f"Sacrificed {card.name}.")
                game_actions.append(f"Put {fetched.name} into play.")
                random.shuffle(deck)
                return True  # Successfully fetched

    return False  # No target found

##########################################################################

def play_land_sac_if_fetch(card:card,
                           hand:list[card],
                           board_lands:list[card],
                           board_creatures:list[card],
                           deck:list[card],
                           game_actions:list,
                           op_deck_size:int,
                           op_grave_size:int)->tuple[int,int]:
    """
    Plays a land and triggers any landfall effects. Sac if it's a fetch,
    then trigger landfall effects if fetching resolved fully.

    Parameters:
        card: card
        hand: list[card]
        board_lands: list[card]
        board_creatures: list[card]
        deck: list[card]
        game_actions: list
        op_deck_size:int
        op_grave_size:int

    Returns:
        (
            op_deck_size:int,
            op_grave_size:int)
    """
    board_lands.append(card)  # Add the land to the battlefield
    game_actions.append(f"Played {card.name}.")
    hand.pop(hand.index(card))  # Remove the land from hand
    creature_count= len(board_creatures)
    if creature_count > 0:
        game_actions.append(f"""Landfall triggers
                            milled {creature_count*3} cards.""")
    # Mill 3 cards for each creature on the board
    op_deck_size, op_grave_size=mill(op_deck_size,
                                     3 * creature_count,
                                     op_grave_size)
    if card.sac and card.sac_cost == 0:
        # Resolve any sac land effects
        if resolve_fetch_land(card,
                              board_lands,
                              deck,
                              game_actions):
            # Land was successfully fetched and sacrificed
            creature_count= len(board_creatures)
            if creature_count > 0:
                game_actions.append(f"""Landfall triggers
                                    milled {creature_count*3} cards.""")
                # Mill 3 cards for each creature on the board
            op_deck_size, op_grave_size=mill(op_deck_size,
                                             3 * creature_count,
                                             op_grave_size)
    return op_deck_size, op_grave_size

############################################################################

def resolve_field_sac(board_lands:list[card],
                      board_creatures:list[card],
                      deck: list[card], game_actions: list)->bool:
    """Resolves a Field of Ruin activation:
        - Requires 3 untapped lands (2 to pay, 1 is Field itself)
        - Fetches a basic land into play tapped
        - Removes Field of Ruin from board
    Parameters:
        board_lands: list[card]
        board_creatures: list[card]
        deck: list[card]
        game_actions: list

    Returns:
        bool: True if resolved successfully, else False.
    """

    fetch_priority = ["Island", "Swamp"]

    # Find untapped Field of Ruin
    field_land = None
    for land in board_lands:
        if land.name == "Field of Ruin" and not getattr(land, 'tapped', True):
            field_land = land
            break
    if not field_land:
        return False

    # Check for at least 3 untapped lands (including Field itself)
    untapped_count = sum(
        1 for l in board_lands if not getattr(l, 'tapped', True))
    if untapped_count < 3:
        game_actions.append("""Not enough untapped
                            lands to activate Field of Ruin.""")
        return False

    # Remove Field of Ruin from board (sacrifice it)
    board_lands.remove(field_land)
    game_actions.append("Sacrificed Field of Ruin.")

    # Search for a basic land to fetch
    for name in fetch_priority:
        for i, card in enumerate(deck):
            if card.name == name and getattr(card, 'land', False):
                fetched = deck.pop(i)
                board_lands.append(fetched)
                game_actions.append(f"Fetched {fetched.name}.")
                random.shuffle(deck)
                return True
    game_actions.append("No valid land found to fetch.")
    return False

###############################################################################

def play_creature_if_possible(hand:list[card],
                              board_lands:list[card],
                              board_creatures:list[card],
                              game_actions:list)-> None:
    """ Plays creatures from hand if possible, using available lands for mana.
    Parameters:
        hand: list[card]
        board_lands: list[card]
        board_creatures: list[card]
        game_actions: list
    """
    creatures_in_hand = list(filter_cards(hand, "creature", True))
    untapped_lands = [land for land in board_lands if not land.tapped]

    while creatures_in_hand:
        card = creatures_in_hand[0]
        mana_cost = parse_mana_cost(card.mana_cost)
        lands_to_tap = find_best_land_combination(untapped_lands, mana_cost)

        if lands_to_tap:
            # Play creature
            board_creatures.append(card)
            for land in lands_to_tap:
                land.tapped = True
                untapped_lands.remove(land)
                game_actions.append(f"Tapped {land.name} for mana.")

            game_actions.append(f"Played {card.name}.")
            hand.remove(card)
            creatures_in_hand.pop(0)
        else:
            break  # Cannot play any more creatures

###############################################################################

def my_turn_1(hand:list[card],
              board_lands: list[card],
              board_creatures: list[card],
              game_actions: list,
              deck:list[card],
              op_deck_size: int,
              op_grave_size: int)->tuple[int,int,int]:
    """Simulates the first turn of the player, playing lands,
    and casting spells.
    Parameters:
        hand: list[card]
        board_lands: list[card]
        board_creatures: list[card]
        game_actions: list
        deck: list[card]
        op_deck_size: int
        op_grave_size: int

    Return:
        (my_turn_count:int, op_deck_size:int, op_grave_size:int)
    """
    game_actions.append("Starting the game on the play.")
    my_turn_count = 1
    game_actions.append(f"My turn {my_turn_count}.")

    # Play a land if available
    lands_in_hand = filter_cards(hand, "land", True)
    if lands_in_hand:
        op_deck_size, op_grave_size = play_land_sac_if_fetch(
            choose_land_to_play(hand),
            hand,
            board_lands,
            board_creatures,
            deck,
            game_actions,
            op_deck_size,
            op_grave_size)

    # Attempt to cast creature if more than 1
    creatures_in_hand = filter_cards(hand, "creature", True)
    if len(creatures_in_hand)>1:
        play_creature_if_possible(hand,
                                  board_lands,
                                  board_creatures,
                                  game_actions)
    op_deck_size, op_grave_size = play_non_creature_if_possible(
        hand,
        board_lands,
        game_actions,
        deck,
        op_deck_size,
        op_grave_size)
    game_actions.append(f"End of my turn {my_turn_count}.")
    return my_turn_count, op_deck_size, op_grave_size

#############################################################################

def play_non_creature_if_possible(hand:list[card],
                                  board_lands:list[card],
                                  game_actions:list,
                                  deck:list[card],
                                  op_deck_size:int,
                                  op_grave_size:int)->tuple[int,int]:
    """Plays noncreatures from hand if possible,
    using available lands for mana and resolves their effects.

    Parameters:
        hand: list[card]
        board_lands: list[card]
        game_actions: list
        deck: list[card]
        op_deck_size: int
        op_grave_size: int

    Return:
        (op_deck_size:int, op_grave_size:int)
    """
    non_creatures = [
    c for c in hand
    if not getattr(c, "creature", False) and not getattr(c, "land", False)
]

    while non_creatures:
        best_choice = None
        best_priority = -999

        for c in non_creatures:
            if c.name == "Visions of Beyond":
                visions_condition = op_grave_size >= 20
            else:
                visions_condition = True

            # Check mana for natural mode
            lands_nat = None
            if c.mana_cost != "0":
                lands_nat = find_best_land_combination(
                    board_lands,parse_mana_cost(c.mana_cost))

            # Check mana for alt mode
            lands_alt = None
            if getattr(c, "mana_cost_alt", None) and visions_condition:
                if c.mana_cost_alt != "0":
                    lands_alt = find_best_land_combination(
                        board_lands, parse_mana_cost(c.mana_cost_alt))
                else:
                    lands_alt = []  # zero-cost, playable without tapping

            # Pick the best playable mode
            if (lands_nat is not None) and c.prio_nat > best_priority:
                best_priority = c.prio_nat
                best_choice = (c, "nat", lands_nat)

            if (lands_alt is not None) and c.prio_alt > best_priority:
                best_priority = c.prio_alt
                best_choice = (c, "alt", lands_alt)

        if not best_choice:
            break

        card, mode, lands_to_tap = best_choice

        # Tap only if lands are needed
        if lands_to_tap:
            for land in lands_to_tap:
                land.tapped = True
                game_actions.append(f"Tapped {land.name} for mana.")
        if mode=="alt":
            game_actions.append(f"Played {card.name} ({mode} mode).")
        else:
            game_actions.append(f"Played {card.name}.")
        # Resolve effects
        if mode == "nat":
            if getattr(card, "mill_nat", 0) > 0:
                op_deck_size, op_grave_size = mill(
                    op_deck_size, card.mill_nat, op_grave_size)
            if getattr(card, "draw_card", 0) > 0:
                draw(card.draw_card, hand, deck, game_actions)
            if getattr(card, "removal", 0) > 0:
                op_grave_size = removal(card.removal, op_grave_size)
            if getattr(card, "deck_exile", 0) > 0:
                op_deck_size = exile_from_deck(op_deck_size,card.deck_exile)
        elif mode == "alt":
            if getattr(card, "mill_alt", 0) > 0:
                op_deck_size, op_grave_size = mill(
                    op_deck_size, card.mill_alt, op_grave_size)
            if getattr(card, "draw_card_alt", 0) > 0:
                draw(card.draw_card_alt, hand, deck, game_actions)
        hand.remove(card)
        non_creatures.remove(card)
    return op_deck_size, op_grave_size

#############################################################################

def op_turn_1(game_actions: list,op_turn_count:int=1)->int:
    """Simulates the first turn of the op.
    Parameters:
        game_actions: list
        op_turn_count: int

    Return:
        op_turn_count: int
    """
    game_actions.append("Starting op turn 1.")
    game_actions.append(f"Op turn {op_turn_count}.")
    game_actions.append(f"End of op turn {op_turn_count}.")
    return op_turn_count

###########################################################################

def op_turn_n(op_turn_count:int,
              game_actions: list,
              op_deck_size:int,
              op_grave_size:int)->tuple[int, int, int, bool]:
    """Simulates the N turn of the op and
    checks if he/she lost the game.

    Parameters:
        op_turn_count: int
        game_actions: list
        op_deck_size:int
        op_grave_size:int
    Return:
        (op_turn_count:int, op_deck_size:int, op_grave_size:int, op_lost:bool)
    """
    op_turn_count += 1
    op_lost=False
    game_actions.append(f"Starting op turn {op_turn_count}.")
    if op_deck_size<1:
        game_actions.append("Op loses from deck out.")
        op_lost=True
    else:
        game_actions.append("Op draws for turn.")
        op_deck_size -=1
        game_actions.append(f"End of op turn {op_turn_count}.")
    return op_turn_count, op_deck_size, op_grave_size, op_lost

#############################################################################

def my_turn_n(my_turn_count:int,
              hand: list[card],
              board_lands: list[card],
              board_creatures: list[card],
              game_actions: list,
              deck:list[card],
              op_deck_size: int,
              op_grave_size: int)->tuple[int, int, int]:
    """Simulates the n-th turn of the player, playing lands,
    and casting spells.

    Parameters:
        my_turn_count: int
        hand: list[card]
        board_lands: list[card]
        board_creatures: list[card]
        game_actions: list
        deck: list[card]
        op_deck_size: int
        op_grave_size: int

    Return:
        (my_turn_count:int, op_deck_size:int, op_grave_size:int)"""
    my_turn_count += 1
    played_land=False
    game_actions.append(f"My turn {my_turn_count}.")
    untap_all_lands(board_lands,game_actions)
    draw(1, hand, deck, game_actions)
    play_creature_if_possible(hand, board_lands, board_creatures, game_actions)
    play_creature_if_possible(hand, board_lands, board_creatures, game_actions)
    play_creature_if_possible(hand, board_lands, board_creatures, game_actions)
    lands_in_hand = filter_cards(hand, "land", True)
    if lands_in_hand:
        op_deck_size, op_grave_size=play_land_sac_if_fetch(
            choose_land_to_play(hand),
            hand, board_lands, board_creatures,
            deck, game_actions, op_deck_size, op_grave_size)
        played_land=True
    play_creature_if_possible(hand, board_lands, board_creatures, game_actions)
    op_deck_size, op_grave_size = play_non_creature_if_possible(
        hand, board_lands,game_actions, deck, op_deck_size, op_grave_size)

    if played_land == False:
        lands_in_hand = filter_cards(hand, "land", True)
        if lands_in_hand:
            op_deck_size, op_grave_size = play_land_sac_if_fetch(
                choose_land_to_play(hand), hand, board_lands,
                board_creatures, deck, game_actions,
                op_deck_size, op_grave_size)
            play_creature_if_possible(hand, board_lands,
                                      board_creatures, game_actions)
            op_deck_size, op_grave_size = play_non_creature_if_possible(
                hand, board_lands,game_actions,
                deck, op_deck_size, op_grave_size)
    f_o_r=resolve_field_sac(board_lands, board_creatures, deck, game_actions)
    if f_o_r==True:
        op_deck_size, op_grave_size = mill(
            op_deck_size,3*len(board_creatures)+1,op_grave_size)
        game_actions.append(
            f"""Landfall triggers milled {3*len(board_creatures)} cards.""")
    op_deck_size, op_grave_size=oboro_landfall_trick(
        played_land, hand, board_lands, board_creatures,
        game_actions, op_deck_size, op_grave_size)
    game_actions.append(f"End of my turn {my_turn_count}.")
    return my_turn_count, op_deck_size, op_grave_size

##############################################################################

def choose_land_to_play(hand: list[card]) -> card:
    """
    Chooses a land from hand based on the number of creatures
    in hand and a priority list.
    Returns the chosen land object if no land is found.

    Parameters:
        hand: list[card]

    Return:
        card

    """
    # Priority lists — can share land names
    priority_if_0_creatures = [
         "Flooded Strand", "Polluted Delta","Shelldock Isle","Undercity Sewers",
         "Watery Grave","Island","Oboro, Palace in the Clouds",
         "Cephalid Coliseum","Otawara, Soaring City","Swamp", "Field of Ruin"]
    priority_if_1_creature = [
        "Undercity Sewers","Watery Grave","Shelldock Isle","Island",
        "Oboro, Palace in the Clouds","Cephalid Coliseum",
        "Otawara, Soaring City",
        "Flooded Strand","Polluted Delta","Swamp", "Field of Ruin"]
    priority_if_more_creatures = [
        "Island","Oboro, Palace in the Clouds","Watery Grave",
        "Otawara, Soaring City", "Cephalid Coliseum""Flooded Strand",
        "Polluted Delta", "Swamp", "Shelldock Isle", "Undercity Sewers",
        "Field of Ruin"]
    # Count creatures
    creatures_in_hand = filter_cards(hand, "creature", True)
    creature_count = len(creatures_in_hand)
    # Pick the right priority list
    if creature_count == 0:
        priority_list = priority_if_0_creatures
    elif creature_count == 1:
        priority_list = priority_if_1_creature
    else:
        priority_list = priority_if_more_creatures

    # Get lands in hand
    lands_in_hand = filter_cards(hand, "land", True)

    # Find first match from the chosen priority list
    for priority_land in priority_list:
        for land in lands_in_hand:
            if land.name == priority_land:
                return land  # First match wins

    return lands_in_hand[0]

##############################################################################

def oboro_landfall_trick(played_land: bool,
                         hand: list,
                         board_lands: list,
                         board_creatures: list,
                         game_actions: list,
                         op_deck_size: int,
                         op_grave_size: int) -> tuple[int, int]:
    """Performs the Oboro, Palace in the Clouds landfall
    bounce trick if conditions are met.

    Parameters:
        played_land: bool
        hand: list[card]
        board_lands: list[card]
        board_creatures: list[card]
        game_actions: list
        op_deck_size: int
        op_grave_size: int

    Returns:
        (
            op_deck_size:int, op_grave_size:int)"""
    if played_land:
        return op_deck_size, op_grave_size  # Already played a land

    # Find Oboro on board
    oboro = next((land for land in board_lands if land.name == "Oboro, Palace in the Clouds"), None)
    if not oboro:
        return op_deck_size, op_grave_size  # No Oboro present

    # Find untapped lands
    untapped_lands = [land for land in board_lands if not getattr(land, "tapped", False)]
    if not untapped_lands:
        return op_deck_size, op_grave_size  # No untapped mana available

    # Choose land to tap — prefer Oboro
    land_to_tap = oboro if oboro in untapped_lands else untapped_lands[0]
    land_to_tap.tapped = True
    game_actions.append(f"Tapped {land_to_tap.name} for mana.")

    # Untap Oboro
    oboro.tapped = False
    game_actions.append("Returned Oboro, Palace in the Clouds to hand and replayed it untapped.")

    # Landfall trigger: mill opponent equal to creature count
    mill_amount = len(board_creatures)
    if mill_amount > 0:
        op_deck_size -= mill_amount
        op_grave_size += mill_amount
        game_actions.append(f"Landfall triggers milled {mill_amount} cards.")

    return op_deck_size, op_grave_size
