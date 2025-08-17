import random
import json
import os
import time
# For tkinter GUI version
from tkinter import *

# Build buttons for Snake, Water, Gun
# Show results and score in labels

# Choices and rules
choices = ["snake", "water", "gun"]
rules = {
    "snake": "water",  # Snake drinks water
    "water": "gun",    # Water damages gun
    "gun": "snake"     # Gun kills snake
}
def delay_print(s):
    for c in s:
        print(c, end='', flush=True)
        time.sleep(0.01)
    print()

# Profile directory
PROFILE_DIR = "profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)


class Player:
    def __init__(self, name):
        self.name = name
        self.stats = {"wins": 0, "losses": 0, "draws": 0, "total": 0}

    def load(self):
        try:
            with open(f"{PROFILE_DIR}/{self.name}.json", "r") as f:
                self.stats = json.load(f)
        except FileNotFoundError:
            pass  # New player

    def save(self):
        with open(f"{PROFILE_DIR}/{self.name}.json", "w") as f:
            json.dump(self.stats, f)

    def update_stats(self, result):
        self.stats[result] += 1
        self.stats["total"] += 1

    def summary(self):
        total = self.stats["total"]
        if total == 0:
            win_rate = 0
        else:
            win_rate = (self.stats["wins"] / total) * 100
        return f"Wins: {self.stats['wins']} | Losses: {self.stats['losses']} | Draws: {self.stats['draws']} | Win Rate: {win_rate:.2f}%"

class AIMode:
    def __init__(self, mode='random'):
        self.mode = mode
        self.user_history = []

    def choose(self):
        if self.mode == 'random' or not self.user_history:
            return random.choice(choices)
        else:
            # Frequency analysis: counter most used user move, counter it
            freq = {c: self.user_history.count(c) for c in choices}
            most_common = max(freq, key=freq.get)
            # Counter strategy
            for ai_choice in choices:
                if rules[ai_choice] == most_common:
                    return ai_choice
            return random.choice(choices)  # Fallback

    def update_user_choice(self, user_choice):
        self.user_history.append(user_choice)


def print_header(title):
    print("\n" + "=" * 40)
    print(f"{title.center(40)}")
    print("=" * 40)


def game_loop(player, ai, rounds=5):
    user_score = 0
    computer_score = 0

    for i in range(1, rounds + 1):
        print_header(f"Round {i} of {rounds}")
        print("Choices: Snake 🐍 | Water 💧 | Gun 🔫")
        user_input = input("Your move: ").lower().strip()

        if user_input not in choices:
            print("❌ Invalid input! Try again.")
            continue

        computer_input = ai.choose()
        ai.update_user_choice(user_input)
        print(f"🤖 Computer chose: {computer_input.capitalize()}")

        if user_input == computer_input:
            print("⚖️ It's a Draw!")
            player.update_stats("draws")
        elif rules[user_input] == computer_input:
            print("✅ You Won this round!")
            player.update_stats("wins")
            user_score += 1
        else:
            print("❌ You Lost this round.")
            player.update_stats("losses")
            computer_score += 1

        print(f"🔢 Score: You {user_score} - {computer_score} Computer")

    print_header("🏁 Final Result")
    if user_score > computer_score:
        print("🎉 You won the game!")
    elif user_score < computer_score:
        print("💻 Computer won the game!")
    else:
        print("🤝 The game is a draw!")

    print(player.summary())
    player.save()


def main():
    print_header("🐍 Snake-Water-Gun Game (Advanced)")

    name = input("Enter your name: ").strip().capitalize()
    player = Player(name)
    player.load()
    print(f"Welcome back, {player.name}!")
    print(player.summary())

    while True:
        print("\nChoose AI mode:")
        print("1. Random Mode")
        print("2. Smart AI (learns your pattern)")
        mode = input("Enter 1 or 2: ").strip()
        ai_mode = 'random' if mode == '1' else 'smart'

        ai = AIMode(ai_mode)
        rounds = input("How many rounds do you want to play? (Default: 5): ").strip()
        rounds = int(rounds) if rounds.isdigit() else 5

        game_loop(player, ai, rounds)

        again = input("\n🔁 Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("👋 Thanks for playing!")
            break


if __name__ == "__main__":
    main()
