# Escape from Blackwood Forest
# A text based adventure game written in Python
#
# This program uses input/output, conditionals, loops, functions, lists,
# tuples, sets, a dictionary for the endings, regular expressions for
# validating the player name and the json module to save the results.

import re
import json
from datetime import datetime

# file where every finished game gets saved
SAVE_FILE = "game_results.json"

# dictionary that maps each possible ending to a title, a message and a score
OUTCOMES = {
    "treasure": {
        "title": "You found the lost treasure!",
        "message": "Inside the chest you find gold coins and an old map that\n"
                   "leads you straight out of the forest. Not a bad day after all.",
        "score": 100
    },
    "escaped": {
        "title": "You escaped the forest",
        "message": "You made it out tired, dirty but alive. Nobody at home is\n"
                   "going to believe this story.",
        "score": 70
    },
    "rescued": {
        "title": "Rescued by the rangers",
        "message": "Just before dark a ranger patrol finds you sitting by the\n"
                   "river. A bit embarrassing, but you are safe.",
        "score": 50
    },
    "lost": {
        "title": "Lost in the forest",
        "message": "You walk in circles for hours until it gets dark. The forest\n"
                   "keeps you for one more night...",
        "score": 20
    },
    "bear": {
        "title": "Eaten by a bear",
        "message": "The cave was not empty. The bear was faster than you.\n"
                   "Game over.",
        "score": 0
    },
    "drowned": {
        "title": "Swept away by the river",
        "message": "The current was a lot stronger than it looked.\n"
                   "Game over.",
        "score": 0
    }
}


def display_title():
    """Prints the welcome message and the instructions of the game."""
    print("=" * 50)
    print("        ESCAPE FROM BLACKWOOD FOREST")
    print("=" * 50)
    print("You wake up alone in the middle of a dark forest.")
    print("You don't remember how you got here. The only thing")
    print("you know is that you have to find a way out.")
    print()
    print("HOW TO PLAY:")
    print(" - Read each situation carefully.")
    print(" - Type the number of your choice and press Enter.")
    print(" - Every decision changes how the story ends.")
    print(" - Your result is saved to a file when the game ends.")
    print("=" * 50)
    print()


def get_player_name():
    """Asks for a name or codename and checks it with a regular expression.
    Rules: 3 to 15 characters, has to start with a letter, and only
    letters, numbers and underscores are allowed."""
    pattern = r"^[A-Za-z][A-Za-z0-9_]{2,14}$"

    while True:
        name = input("Enter your name or codename: ").strip()
        if re.match(pattern, name):
            return name
        else:
            print("Invalid name. Use 3-15 characters, start with a letter")
            print("and only use letters, numbers or underscores.\n")


def get_choice(prompt, options):
    """Keeps asking until the player types one of the valid options.
    options is a tuple like ("1", "2", "3")."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print("Please type one of these: " + ", ".join(options))


def forest_path(decisions):
    """First part of the story. Returns the next scene or an ending."""
    print("\nYou stand up and look around. There are three ways to go:")
    print("  1) Follow the sound of running water")
    print("  2) Walk towards a dark cave in the hillside")
    print("  3) Push straight through the thick bushes")

    choice = get_choice("What do you do? (1/2/3): ", ("1", "2", "3"))

    if choice == "1":
        decisions.append("followed the sound of water")
        print("\nYou follow the sound and soon reach a fast flowing river.")
        return "river"
    elif choice == "2":
        decisions.append("went up to the cave")
        print("\nYou climb the hill and stop in front of the cave entrance.")
        print("It is pitch black inside and smells like wet fur.")
        return "cave"
    else:
        decisions.append("pushed through the bushes")
        print("\nThe bushes get thicker and thicker. Every tree looks the same.")
        return "lost"


def cave_scene(decisions, inventory):
    """Cave part of the story. Can end the game or send the player to the river."""
    print("\nWhat do you want to do at the cave?")
    print("  1) Walk straight into the dark")
    print("  2) Search around the entrance first")
    print("  3) Forget the cave and walk downhill")

    choice = get_choice("What do you do? (1/2/3): ", ("1", "2", "3"))

    if choice == "1":
        decisions.append("walked into the dark cave")
        print("\nYou take a few steps inside. Something big is breathing...")
        return "bear"

    elif choice == "2":
        decisions.append("searched the cave entrance")
        # a set is used for the inventory so an item can't be added twice
        inventory.add("rope")
        inventory.add("lantern")
        print("\nBehind a rock you find an old rope and a rusty lantern.")
        print("The lantern still works! Now you can see a bit inside the cave.")
        print("  1) Go deeper with the lantern")
        print("  2) Take the stuff and walk down to the river")

        choice = get_choice("What do you do? (1/2): ", ("1", "2"))

        if choice == "1":
            decisions.append("explored the cave with the lantern")
            print("\nWith the light you spot a huge bear sleeping in the corner.")
            print("You sneak past it very slowly... and find an old wooden chest.")
            return "treasure"
        else:
            decisions.append("took the items and left the cave")
            print("\nYou walk downhill with your new gear and reach a wide river.")
            return "river"

    else:
        decisions.append("skipped the cave")
        print("\nYou walk downhill and after a while you reach a wide river.")
        return "river"


def river_scene(decisions, inventory):
    """River part of the story. Always ends the game."""
    print("\nThe river is wide and the water looks freezing. On the other")
    print("side you can see what looks like a hiking trail.")
    print("  1) Swim across")
    print("  2) Walk along the bank and look for a bridge")
    print("  3) Sit down and wait for help")

    choice = get_choice("What do you do? (1/2/3): ", ("1", "2", "3"))

    if choice == "1":
        decisions.append("tried to swim across the river")
        # the rope from the cave saves the player here
        if "rope" in inventory:
            print("\nYou tie the rope around a tree, pull yourself across and")
            print("follow the trail out of the forest.")
            return "escaped"
        else:
            print("\nHalfway across the current grabs your legs...")
            return "drowned"
    elif choice == "2":
        decisions.append("looked for a bridge")
        print("\nAfter twenty minutes you find an old wooden bridge. It creaks,")
        print("but it holds. The trail on the other side leads you out.")
        return "escaped"
    else:
        decisions.append("waited for help by the river")
        print("\nYou sit down by the river. Hours pass...")
        return "rescued"


def show_results(name, decisions, outcome_key):
    """Prints the ending, the list of decisions and the score."""
    result = OUTCOMES[outcome_key]

    print("\n" + "*" * 50)
    print("  " + result["title"].upper())
    print("*" * 50)
    print(result["message"])
    print()
    print(f"{name}, this is the path you took:")
    for number, decision in enumerate(decisions, start=1):
        print(f"  {number}. You {decision}")
    print(f"\nFinal score: {result['score']} / 100")


def save_game_data(player_data):
    """Adds the player's data to the JSON file. Creates the file if needed."""
    try:
        with open(SAVE_FILE, "r") as file:
            all_results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # first time playing or the file is broken, start with an empty list
        all_results = []

    all_results.append(player_data)

    with open(SAVE_FILE, "w") as file:
        json.dump(all_results, file, indent=4)

    print(f"Your result was saved to {SAVE_FILE} ({len(all_results)} games saved in total)")


def main():
    """Controls the flow of the whole game."""
    display_title()
    name = get_player_name()

    games_played = 0
    play_again = "y"

    # the player can keep playing as long as they answer 'y'
    while play_again == "y":
        games_played += 1
        decisions = []      # every choice the player makes goes in here
        inventory = set()   # items the player picks up

        print(f"\n--- Game {games_played} --- Good luck, {name}! ---")

        scene = forest_path(decisions)

        if scene == "cave":
            scene = cave_scene(decisions, inventory)
        if scene == "river":
            scene = river_scene(decisions, inventory)

        # at this point 'scene' is one of the keys in OUTCOMES
        show_results(name, decisions, scene)

        player_data = {
            "name": name,
            "game_number": games_played,
            "decisions": decisions,
            "items_found": sorted(inventory),   # json can't store a set directly
            "outcome": OUTCOMES[scene]["title"],
            "score": OUTCOMES[scene]["score"],
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_game_data(player_data)

        play_again = get_choice("\nDo you want to play again? (y/n): ", ("y", "n"))

    print(f"\nThanks for playing, {name}! You played {games_played} game(s). Goodbye!")


if __name__ == "__main__":
    main()
