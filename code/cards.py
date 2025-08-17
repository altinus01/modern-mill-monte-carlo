from mtg_mill_simulation.code.game_params import removal_prio

def parse_cmc_int(cost_str:str|None)->int:
    """Parses a mana cost.

    Parameters:
        cost_str: string|None, Ex: '1UB'

    Returns:
        total: int
        """
    if cost_str == 0:
        return 0
    if cost_str == None:
        return 0
    total = 0
    digits = ''
    for c in cost_str:
        if c.isdigit():
            digits += c
        else:
            if digits:
                total += int(digits)
                digits = ''
            total += 1  # Each symbol like U, B, G adds 1
    if digits:
        total += int(digits)
    return total

class card:
  def __init__(self,
               name:str,#card name
               copy_number:int,#what copy of the card is this
               draw_card:int=0,#how many cards this card draws as a main effect
               draw_card_alt:int=0,#how many cards this card draws as an alternative effect
               mana_cost:str="0",#mana cost of the card in symbolic form E.g. "1UB" for 1 generic, 1 blue mana znd 1 black mana
               mana_cost_alt=None,#alternative mana cost of the card in symbolic form, baseline None for no alt mode
               mill_nat:int=0,#how many cards this card mills as a main effect
               mill_alt:int=0,#how many cards this card mills as an alternative effect
               mana_gen:list[str]=[],#list of possible mana generation effects and ANY for all colours in the deck
               land:bool=False,#is this a land card
               sac:bool=False,#can this card be sacrificed
               sac_cost:int=0,#how much mana this card costs to sacrifice
               tapped:bool=False,#is this card tapped when played
               creature:bool=False,#is this a creature card
               removal:int=0,#is this card a removal spell (0=no, 1=yes)
               deck_exile:int=0#number of cards this card exiles from the top of op deck
               ):
    self.name=name
    self.copy_number=copy_number
    self.removal=removal
    self.draw_card=draw_card
    self.draw_card_alt=draw_card_alt
    self.mana_cost=mana_cost
    self.mana_cost_alt=mana_cost_alt
    self.mill_nat=mill_nat
    self.mill_alt=mill_alt
    self.mana_gen=mana_gen
    self.land=land
    self.sac=sac
    self.sac_cost=sac_cost
    self.tapped=tapped
    self.creature=creature
    self.deck_exile=deck_exile
    self.cmc = parse_cmc_int(mana_cost)
    self.cmc_alt = parse_cmc_int(mana_cost_alt)
    self.prio_nat=(self.mill_nat+self.deck_exile)/(1+self.cmc)+(10*removal_prio*removal)
    self.prio_alt=(self.mill_alt)/(1+self.cmc_alt)+(10*removal_prio*removal)




def lands_in(deck:list[card]):
    """Inserts lands into the deck.

    Parameters:
        deck: list[card]

        """
    Swamp1=card(name="Swamp",copy_number=1,mana_gen=["B"],land=True)
    deck.append(Swamp1)
    Island1=card(name="Island",copy_number=1,mana_gen=["U"],land=True)
    deck.append(Island1)
    Island2=card(name="Island",copy_number=2,mana_gen=["U"],land=True)
    deck.append(Island2)
    Island3=card(name="Island",copy_number=3,mana_gen=["U"],land=True)
    deck.append(Island3)
    Cephalid1=card(name="Cephalid Coliseum",copy_number=1,mana_gen=["U"],land=True)
    deck.append(Cephalid1)
    Otawara1=card(name="Otawara, Soaring City",copy_number=1,mana_gen=["U"],land=True)
    deck.append(Otawara1)
    Field_of_Ruin1=card(name="Field of Ruin",copy_number=1,mana_gen=["C"],land=True,sac=True,sac_cost=2)
    deck.append(Field_of_Ruin1)
    Field_of_Ruin2=card(name="Field of Ruin",copy_number=2,mana_gen=["C"],land=True,sac=True,sac_cost=2)
    deck.append(Field_of_Ruin2)
    Field_of_Ruin3=card(name="Field of Ruin",copy_number=3,mana_gen=["C"],land=True,sac=True,sac_cost=2)
    deck.append(Field_of_Ruin3)
    Flooded_Strand1=card(name="Flooded Strand",copy_number=1,land=True,sac=True)
    deck.append(Flooded_Strand1)
    Flooded_Strand2=card(name="Flooded Strand",copy_number=2,land=True,sac=True)
    deck.append(Flooded_Strand2)
    Flooded_Strand3=card(name="Flooded Strand",copy_number=3,land=True,sac=True)
    deck.append(Flooded_Strand3)
    Watery_Grave1=card(name="Watery Grave",copy_number=1,mana_gen=["ANY"],land=True)
    deck.append(Watery_Grave1)
    Watery_Grave2=card(name="Watery Grave",copy_number=2,mana_gen=["ANY"],land=True)
    deck.append(Watery_Grave2)
    Oboro1=card(name="Oboro, Palace in the Clouds",copy_number=1,mana_gen=["U"],land=True)
    deck.append(Oboro1)
    Polluted_Delta1=card(name="Polluted Delta",copy_number=1,land=True,sac=True)
    deck.append(Polluted_Delta1)
    Polluted_Delta2=card(name="Polluted Delta",copy_number=2,land=True,sac=True)
    deck.append(Polluted_Delta2)
    Polluted_Delta3=card(name="Polluted Delta",copy_number=3,land=True,sac=True)
    deck.append(Polluted_Delta3)
    Polluted_Delta4=card(name="Polluted Delta",copy_number=4,land=True,sac=True)
    deck.append(Polluted_Delta4)
    Shelldock1=card(name="Shelldock Isle",copy_number=1,mana_gen=["U"],land=True,tapped=True)
    deck.append(Shelldock1)
    Undercity1=card(name="Undercity Sewers",copy_number=1,mana_gen=["ANY"],land=True,tapped=True)
    deck.append(Undercity1)
    Undercity2=card(name="Undercity Sewers",copy_number=2,mana_gen=["ANY"],land=True,tapped=True)
    deck.append(Undercity2)


def creatures_in(deck:list[card]):
    """Inserts creatures into the deck.

    Parameters:
        deck: list[card]

        """

    Hedron1=card(name="Hedron Crab",copy_number=1,creature=True,mana_cost="U")
    deck.append(Hedron1)
    Hedron2=card(name="Hedron Crab",copy_number=2,creature=True,mana_cost="U")
    deck.append(Hedron2)
    Hedron3=card(name="Hedron Crab",copy_number=3,creature=True,mana_cost="U")
    deck.append(Hedron3)
    Hedron4=card(name="Hedron Crab",copy_number=4,creature=True,mana_cost="U")
    deck.append(Hedron4)
    Ruin1=card(name="Ruin Crab",copy_number=1,creature=True,mana_cost="U")
    deck.append(Ruin1)
    Ruin2=card(name="Ruin Crab",copy_number=2,creature=True,mana_cost="U")
    deck.append(Ruin2)
    Ruin3=card(name="Ruin Crab",copy_number=3,creature=True,mana_cost="U")
    deck.append(Ruin3)
    Ruin4=card(name="Ruin Crab",copy_number=4,creature=True,mana_cost="U")
    deck.append(Ruin4)

def inst_sorc_in(deck:list[card]):
    """Inserts instants and sorceries into the deck.

    Parameters:
        deck: list[card]

        """

    Archive1=card(name="Archive Trap",copy_number=1,mana_cost="3UU",mana_cost_alt="0",mill_nat=13,mill_alt=13)
    deck.append(Archive1)
    Archive2=card(name="Archive Trap",copy_number=2,mana_cost="3UU",mana_cost_alt="0",mill_nat=13,mill_alt=13)
    deck.append(Archive2)
    Archive3=card(name="Archive Trap",copy_number=3,mana_cost="3UU",mana_cost_alt="0",mill_nat=13,mill_alt=13)
    deck.append(Archive3)
    Archive4=card(name="Archive Trap",copy_number=4,mana_cost="3UU",mana_cost_alt="0",mill_nat=13,mill_alt=13)
    deck.append(Archive4)
    Baleful1=card(name="Baleful Mastery",copy_number=1,mana_cost="1B", deck_exile=1)
    deck.append(Baleful1)
    Crypt1=card(name="Crypt Incursion",copy_number=1,mana_cost="2B")
    deck.append(Crypt1)
    Drown1=card(name="Drown in the Loch",copy_number=1,mana_cost="UB",removal=1)
    deck.append(Drown1)
    Drown2=card(name="Drown in the Loch",copy_number=2,mana_cost="UB",removal=1)
    deck.append(Drown2)
    Drown3=card(name="Drown in the Loch",copy_number=3,mana_cost="UB",removal=1)
    deck.append(Drown3)
    Fatal1=card(name="Fatal Push",copy_number=1,mana_cost="B",removal=1)
    deck.append(Fatal1)
    Fatal2=card(name="Fatal Push",copy_number=2,mana_cost="B",removal=1)
    deck.append(Fatal2)
    Fatal3=card(name="Fatal Push",copy_number=3,mana_cost="B",removal=1)
    deck.append(Fatal3)
    Fatal4=card(name="Fatal Push",copy_number=4,mana_cost="B",removal=1)
    deck.append(Fatal4)
    Fractured1=card(name="Fractured Sanity",copy_number=1,mill_nat=14,mana_cost="UUU",mill_alt=4,mana_cost_alt="1U",draw_card_alt=1)
    deck.append(Fractured1)
    Fractured2=card(name="Fractured Sanity",copy_number=2,mill_nat=14,mana_cost="UUU",mill_alt=4,mana_cost_alt="1U",draw_card_alt=1)
    deck.append(Fractured2)
    Fractured3=card(name="Fractured Sanity",copy_number=3,mill_nat=14,mana_cost="UUU",mill_alt=4,mana_cost_alt="1U",draw_card_alt=1)
    deck.append(Fractured3)
    Fractured4=card(name="Fractured Sanity",copy_number=4,mill_nat=14,mana_cost="UUU",mill_alt=4,mana_cost_alt="1U",draw_card_alt=1)
    deck.append(Fractured4)
    Glimpse1=card(name="Glimpse the Unthinkable",copy_number=1,mill_nat=10,mana_cost="UB")
    deck.append(Glimpse1)
    Glimpse2=card(name="Glimpse the Unthinkable",copy_number=2,mill_nat=10,mana_cost="UB")
    deck.append(Glimpse2)
    Surgical1=card(name="Surgical Extraction",copy_number=1,mill_nat=2)
    deck.append(Surgical1)
    Surgical2=card(name="Surgical Extraction",copy_number=2,mill_nat=2)
    deck.append(Surgical2)
    Surgical3=card(name="Surgical Extraction",copy_number=3,mill_nat=2)
    deck.append(Surgical3)
    Tasha1=card(name="Tasha's Hideous Laughter",copy_number=1,deck_exile=13,mana_cost="1UU")
    deck.append(Tasha1)
    Tasha2=card(name="Tasha's Hideous Laughter",copy_number=2,deck_exile=13,mana_cost="1UU")
    deck.append(Tasha2)
    Tasha3=card(name="Tasha's Hideous Laughter",copy_number=3,deck_exile=13,mana_cost="1UU")
    deck.append(Tasha3)
    Tasha4=card(name="Tasha's Hideous Laughter",copy_number=4,deck_exile=13,mana_cost="1UU")
    deck.append(Tasha4)
    Visions1=card(name="Visions of Beyond",copy_number=1,mana_cost="U",draw_card=1,draw_card_alt=3,mana_cost_alt="U")
    deck.append(Visions1)
    Visions2=card(name="Visions of Beyond",copy_number=2,mana_cost="U",draw_card=1,draw_card_alt=3,mana_cost_alt="U")
    deck.append(Visions2)
    Visions3=card(name="Visions of Beyond",copy_number=3,mana_cost="U",draw_card=1,draw_card_alt=3,mana_cost_alt="U")
    deck.append(Visions3)

def planeswalkers_in(deck:list[card]):
    """Inserts planeswalkers into the deck.

    Parameters:
        deck: list[card]

        """
    Jace1=card(name="Jace, the Perfect Mind",copy_number=1,mana_cost="2UU",mill_nat=15,mana_cost_alt="2U",mill_alt=9)
    deck.append(Jace1)
