from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Колода карт (с учетом мастей для Blackjack)
cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10,
         10, 10, 11]  # Туз может стоить 1 или 11


def calculate_score(hand):
    """Считает сумму очков в руке с учетом туза."""
    score = sum(hand)
    # Обработка тузов
    aces = hand.count(11)
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score


@app.route('/alice', methods=['POST'])
def handle_alice():
    data = request.json
    command = data['request']['command'].lower()
    session = data['session']
    user_id = session['user_id']

    # Инициализация игры (если её нет в сессии)
    if 'game' not in session:
        session['game'] = {
            'player_hand': [],
            'dealer_hand': [],
            'game_over': False
        }

    game = session['game']

    # Обработка команд
    if "старт" in command or "начать" in command:
        # Раздача первых двух карт
        game['player_hand'] = [random.choice(cards), random.choice(cards)]
        game['dealer_hand'] = [random.choice(cards), random.choice(cards)]
        game['game_over'] = False

        response_text = (
            f"Игра началась! Ваши карты: {game['player_hand']} (сумма: {calculate_score(game['player_hand'])}). "
            f"Карты дилера: {game['dealer_hand'][0]} и ?. "
            "Скажите 'ещё карту' или 'пас'?"
        )

    elif "ещё" in command and not game['game_over']:
        game['player_hand'].append(random.choice(cards))
        player_score = calculate_score(game['player_hand'])

        if player_score > 21:  # Игрок проигрывает при превышении 21
            game['game_over'] = True
            response_text = f"Ваши карты: {game['player_hand']} (сумма: {player_score}). Вы проиграли! 😢"
        else:
            response_text = f"Ваши карты: {game['player_hand']} (сумма: {player_score}). Пас или ещё?"

    elif "пас" in command and not game['game_over']:
        # Дилер добирает карты по правилам Blackjack
        player_score = calculate_score(game['player_hand'])
        dealer_score = calculate_score(game['dealer_hand'])

        while dealer_score < 17:
            game['dealer_hand'].append(random.choice(cards))
            dealer_score = calculate_score(game['dealer_hand'])

        game['game_over'] = True

        # Определение победителя
        if player_score > 21:
            result = "Вы проиграли! 😢"
        elif dealer_score > 21 or player_score > dealer_score:
            result = "Вы выиграли! 🎉"
        elif player_score < dealer_score:
            result = "Дилер выиграл. 😢"
        else:
            result = "Ничья!"

        response_text = (
            f"Ваши карты: {game['player_hand']} ({player_score}). "
            f"Карты дилера: {game['dealer_hand']} ({dealer_score}). {result}"
        )

    else:
        response_text = "Не поняла. Скажите 'начать игру', 'ещё карту' или 'пас'."

    # Формируем ответ
    response = {
        "version": data["version"],
        "session": session,
        "response": {
            "text": response_text,
            "end_session": game['game_over']
        }
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run()
