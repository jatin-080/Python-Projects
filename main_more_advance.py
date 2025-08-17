import random
import json
import os
import time
import sys

# Choices and rules
choices = ["snake", "water", "gun"]
rules = {
    "snake": "water",  # Snake drinks water
    "water": "gun",    # Water damages gun
    "gun": "snake"     # Gun kills snake
}

# Profile directory
PROFILE_DIR = "profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

# Fancy delay print
def delay_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

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
        win_rate = (self.stats["wins"] / total) * 100 if total else 0
        return f"Wins: {self.stats['wins']} | Losses: {self.stats['losses']} | Draws: {self.stats['draws']} | Win Rate: {win_rate:.2f}%"

class AIMode:
    def __init__(self, mode='random'):
        self.mode = mode
        self.user_history = []

    def choose(self):
        if self.mode == 'random' or not self.user_history:
            return random.choice(choices)
        else:
            freq = {c: self.user_history.count(c) for c in choices}
            most_common = max(freq, key=freq.get)
            for ai_choice in choices:
                if rules[ai_choice] == most_common:
                    return ai_choice
            return random.choice(choices)

    def update_user_choice(self, user_choice):
        self.user_history.append(user_choice)

def print_header(title):
    delay_print("\n" + "=" * 40)
    delay_print(f"{title.center(40)}")
    delay_print("=" * 40)

def game_loop(player, ai, rounds=5):
    user_score = 0
    computer_score = 0

    for i in range(1, rounds + 1):
        print_header(f"Round {i} of {rounds}")
        delay_print("Choices: Snake  | Water  | Gun ")
        user_input = input("Your move: ").lower().strip()

        if user_input not in choices:
            delay_print("❌ Invalid input! Try again.")
            continue

        computer_input = ai.choose()
        ai.update_user_choice(user_input)

        delay_print(f"🤖 Computer chose: {computer_input.capitalize()}")

        if user_input == computer_input:
            delay_print("⚖️ It's a Draw!")
            player.update_stats("draws")
        elif rules[user_input] == computer_input:
            delay_print("✅ You Won this round!")
            player.update_stats("wins")
            user_score += 1
        else:
            delay_print("❌ You Lost this round.")
            player.update_stats("losses")
            computer_score += 1

        delay_print(f"🔢 Score: You {user_score} - {computer_score} Computer")

    print_header("🏁 Final Result")
    if user_score > computer_score:
        delay_print("🎉 You won the game!")
    elif user_score < computer_score:
        delay_print("💻 Computer won the game!")
    else:
        delay_print("🤝 The game is a draw!")

    delay_print(player.summary())
    player.save()

def main():
    print_header("🐍 Snake-Water-Gun Game (Advanced)")
    name = input("Enter your name: ").strip().capitalize()
    player = Player(name)
    player.load()

    delay_print(f"Welcome back, {player.name}!")
    delay_print(player.summary())

    while True:
        delay_print("\nChoose AI mode:")
        delay_print("1. Random Mode")
        delay_print("2. Smart AI (learns your pattern)")
        mode = input("Enter 1 or 2: ").strip()
        ai_mode = 'random' if mode == '1' else 'smart'
        ai = AIMode(ai_mode)

        rounds = input("How many rounds do you want to play? (Default: 5): ").strip()
        rounds = int(rounds) if rounds.isdigit() else 5

        game_loop(player, ai, rounds)

        again = input("\n🔁 Play again? (y/n): ").strip().lower()
        if again != 'y':
            delay_print("👋 Thanks for playing!")
            break

if __name__ == "__main__":
    main()
