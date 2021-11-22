from bj.classes import Deck, Card


player_money = 100  # Деньги игрока
rate_value = 10  # Размер ставки

deck = Deck()
""""" попробуй через !!go to!!"""

def sum_points(cards):
    """
    Напишите отдельную функцию для нахождения суммы очков всех карт в списке
    :param cards: список карт(рука игрока или диллера)
    :return: сумму очков
    """
    sum_points = 0
    for card in cards:
        sum_points += card.points
    # Если сумма > 21, то перечитываем сумму, считая ТУЗ за 1(единицу)
    if sum_points > 21:
        sum_points = 0
        for card in cards:
            if card.value == 'A':
                card.points = 1
            sum_points += card.points
    return sum_points


def game(player_money):
    # 0. Игрок делает ставку
    player_money -= rate_value
    # 1. В начале игры перемешиваем колоду
    deck.shuffle()
    # 2. Игроку выдаем две карты
    player_cards = deck.draw(2)
    # 3. Дилер берет одну карту
    dealer_cards = deck.draw(1)
    # 4. Отображаем в консоли карты игрока и дилера
    print(f'Player cards: {player_cards}')
    print(f'Dealer cards: {dealer_cards}')
    # 5. Проверяем нет ли у игрока блэкджека (21 очко)

    while True:
        if sum_points(player_cards) > 21:
            print(f"Перебор: {sum_points(player_cards)} очков \n Casino wins {player_money=}")
            return
        elif sum_points(player_cards) == 21:
            player_money += rate_value * 1.5
            print(f"Black Jack!!! Игрок победил \n {player_money=}")
            return
        else:
            player_choice = input("еще(1)/достаточно(0): ")
            if player_choice == "1":
                # Раздаем еще одну карту
                player_cards += deck.draw(1)
                print(f'Player cards  now: {player_cards}')
            elif player_choice == "0":
                # Заканчиваем добирать карты
                break
            else:
                print(f'не допустимое действие')

    print("Диллер добирает карты")
    while True:  # дилер начинает набирать карты.
        if sum_points(dealer_cards) < 17:
            dealer_cards += deck.draw(1)
            print("Dealer cards now:", dealer_cards)
        else:
            break

    if sum_points(player_cards) > sum_points(dealer_cards):
        player_money += rate_value * 1.5
        print(f"Black Jack!!! Игрок победил {player_money=}")
    elif sum_points(player_cards) == sum_points(dealer_cards):
        player_money += rate_value
        print(f"There is a draw {player_money=}")
    else:
        print("You've lost your money, Casino wins")
    return


def start_menu(player_money):
    while True:
        print("What's next?")
        print("To see your wallet press 1")
        print("To insert money on your wallet press 2")
        print("To play again press 3")
        print("To leave the game press 4")

        choice = input("Your choice: ")

        if choice == '1':
            print(f"On your account {player_money} $")
        if choice == '2':
            amount = input("Enter amount: ")
            player_money += amount
            print(f"On your account {player_money} $")
        if choice == '3':
            print("play")
            game(player_money)
        if choice == '4':
            print("Good buy!")
            break

if __name__ == "__main__":
    start_menu(player_money)