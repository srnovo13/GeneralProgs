
HARD_STRATEGY = {
    # total: [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A']
    8: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
    9: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
    11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],
    12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'R', 'H'],
    16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'R', 'R', 'R'],
    17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
}

SOFT_STRATEGY = {
    # Soft hand = Ace + X (X is the value below)
    # e.g. key 2 means Ace+2 = soft 13
    2: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    3: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    4: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    5: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    6: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    7: ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'],
    8: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    9: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
}

PAIR_STRATEGY = {
    # Pair rank: 2–10 and A
    '2': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
    '3': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
    '4': ['H', 'H', 'H', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
    '5': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
    '6': ['P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
    '7': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
    '8': ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    '9': ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],
    '10': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    'A': ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
}

DEALER_INDEX = {
    '2': 0, '3': 1, '4': 2, '5': 3, '6': 4,
    '7': 5, '8': 6, '9': 7, '10': 8, 'J': 8,
    'Q': 8, 'K': 8, 'A': 9
}


ACTION_LABELS = {
    'H': 'Hit',
    'S': 'Stand',
    'D': 'Double Down',
    'P': 'Split',
    'R': 'Surrender (If not allowed, Hit)',
}


def card_value(card):
    card = card.upper()
    if card == ('J', 'Q', 'K',):
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)


def classify_hand(card1, card2):
    c1 = card1.upper()
    c2 = card2.upper()

    if c1 == c2:
        return 'pair', c1

    if 'A' in (c1, c2):
        other = c2 if c1 == 'A' else c1
        return 'soft', card_value(other)

    total = card_value(c1) + card_value(c2)
    return 'hard', total

    # Dealer upcard index: 2,3,4,5,6,7,8,9,10,A
    # Each row is your hand, mapped to: H=Hit, S=Stand, D=Double, P=Split, R=Surrender


def dealer_col(dealer_card):
    return DEALER_INDEX[dealer_card.upper()]


def get_recommendation(card1, card2, dealer_card):
    hand_type, hand_val = classify_hand(card1, card2)
    col = dealer_col(dealer_card)

    if hand_type == 'pair':
        row = PAIR_STRATEGY.get(hand_val)
    elif hand_type == 'soft':
        row = SOFT_STRATEGY.get(hand_val)
    else:
        if hand_val <= 8:
            return 'Hit'
        if hand_val >= 18:
            return 'Stand'
        row = HARD_STRATEGY.get(hand_val)

    if row is None:
        return 'Stand'

    action_code = row[col]
    return ACTION_LABELS[action_code]


def main():
    print("=== Blackjack Basic Strategy Tool ===")
    print("Dealer hits on soft 17. Enter cards as: 2-9, 10, J, Q, K, A\n")

    while True:
        try:
            card1 = input("Your first card: ").strip()
            card2 = input("Your second card: ").strip()
            dealer = input("Dealer's upcard: ").strip()

            recommendation = get_recommendation(card1, card2, dealer)
            print(f"\n>> Recommendation: {recommendation}\n")
            print("-" * 40)

        except (KeyError, ValueError) as e:
            print(f"Invalid input: {e}. Please re-enter.\n")

if __name__ == "__main__":
    main()



