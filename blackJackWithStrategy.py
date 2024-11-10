import random
# Deck of cards
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
# Strategies for optimal moves
HARD_STRATEGY = {
    17: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 'A': 'S'},
    16: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
    15: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
    12: {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 'A': 'H'},
    # Add more rows as per strategy chart...
}

SOFT_STRATEGY = {
    'A,8': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 'A': 'S'},
    'A,7': {2: 'S', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'S', 8: 'S', 9: 'H', 10: 'H', 'A': 'H'},
    # Add more rows as per strategy chart...
}

PAIR_STRATEGY = {
    'A,A': {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 'A': 'P'},
    '10,10': {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 'A': 'S'},
    # Add more rows as per strategy chart...
}


def adjust_for_ace(cards):
    """Adjust Aces from 11 to 1 to avoid going over 21."""
    while sum(cards) > 21 and 11 in cards:
        cards.remove(11)
        cards.append(1)
    return cards


def get_strategy_action(player_cards, dealer_card):
    """Determine action based on strategy."""
    player_total = sum(player_cards)
    dealer_value = dealer_card if dealer_card != 11 else 'A'

    # Check for soft hand
    if 11 in player_cards and player_total <= 21:
        return SOFT_STRATEGY.get(f"A,{player_total - 11}", {}).get(dealer_value, 'H')

    # Check for pair
    if len(player_cards) == 2 and player_cards[0] == player_cards[1]:
        return PAIR_STRATEGY.get(f"{player_cards[0]},{player_cards[1]}", {}).get(dealer_value, 'H')

    # Hard total strategy
    return HARD_STRATEGY.get(player_total, {}).get(dealer_value, 'H')


def get_final_computer_cards(current_cards):
    """Ensure the computer's cards meet the rules."""
    while sum(current_cards) < 17:
        current_cards.append(random.choice(cards))
        current_cards = adjust_for_ace(current_cards)
    return current_cards


def run_blackjack():
    """Main game function."""
    print("\n" * 5)  # Clear the screen

    user_cards = random.choices(cards, k=2)
    computer_cards = random.choices(cards, k=2)
    user_cards = adjust_for_ace(user_cards)
    computer_cards = adjust_for_ace(computer_cards)

    print(f"    Your cards: {user_cards}, current score: {sum(user_cards)}")
    print(f"    Computer's first card: {computer_cards[0]}")

    # Check for Blackjack
    if sum(computer_cards) == 21:
        print("You lose. The computer has Blackjack!")
        return
    elif sum(user_cards) == 21:
        print("You win with a Blackjack!")
        return

    # User's turn
    while True:
        action = get_strategy_action(user_cards, computer_cards[0])
        print(f"Strategy recommendation: {action}")

        user_choice = input("Type 'y' to get another card, type 'n' to pass: ").strip().lower()
        if user_choice == 'y':
            user_cards.append(random.choice(cards))
            user_cards = adjust_for_ace(user_cards)
            print(f"    Your cards: {user_cards}, current score: {sum(user_cards)}")

            if sum(user_cards) > 21:
                print("You went over. You lose 😭")
                return
        elif user_choice == 'n':
            break
        else:
            print("Invalid input! Please type 'y' or 'n'.")

    # Computer's turn
    computer_cards = get_final_computer_cards(computer_cards)
    print(f"    Your final hand: {user_cards}, final score: {sum(user_cards)}")
    print(f"    Computer's final hand: {computer_cards}, final score: {sum(computer_cards)}")

    # Determine the winner
    if sum(computer_cards) > 21:
        print("Opponent went over. You win 😁")
    elif sum(user_cards) == sum(computer_cards):
        print("It's a draw!")
    elif sum(user_cards) > sum(computer_cards):
        print("You win 😁")
    else:
        print("You lose 😭")


# Game loop
while True:
    run_blackjack()
    play_again = input("Do you want to play again? Type 'y' or 'n': ").strip().lower()
    if play_again != 'y':
        print("Thanks for playing! Goodbye!")
        break