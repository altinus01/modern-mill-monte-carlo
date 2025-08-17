from mtg_mill_simulation.code.cards import card, lands_in, creatures_in, inst_sorc_in, planeswalkers_in


def initialize_deck()->list[card]: #DONE
    """Initializes the deck with lands, creatures, instants, sorceries, and planeswalkers.

    Returns:
    deck: list[card]
    """

    deck = []
    lands_in(deck)
    creatures_in(deck)
    inst_sorc_in(deck)
    planeswalkers_in(deck)
    if len(deck) != 60:
        raise ValueError("Deck must contain exactly 60 cards, currently has {}".format(len(deck)))
    return deck
