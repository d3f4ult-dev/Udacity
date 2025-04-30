# Epic Adventure Quest
# Copyright © 2025 Ahmed Shafiq. All rights reserved.
#
# Epic Adventure Quest Proprietary License
#
# This software, including all associated code, documentation, and assets, is
# the exclusive property of Ahmed Shafiq. Only Ahmed Shafiq is permitted to use,
# execute, or access this software. No other individual, entity, or organization
# may use, copy, modify, distribute, sublicense, or create derivative works of
# this software, in whole or in part, without the prior express written
# permission of Ahmed Shafiq.
#
# Any unauthorized use, reproduction, distribution, or modification of this
# software is strictly prohibited and may result in legal action. All rights not
# expressly granted herein are reserved by Ahmed Shafiq.
#
# For permission requests, contact Ahmed Shafiq directly.
#
# Created by: Ahmed Shafiq
# Date: April 2025
# Purpose: A text-based adventure game set in a mystical forest with branching
#          paths, scoring, and colored text output.

# Standard library imports
import random
import time
import json
import os
from datetime import datetime

# Third-party imports
from colorama import init, Fore, Style


# Initialize colorama for cross-platform colored text output
init()


class Inventory:
    def __init__(self):
        self.items = {}
        self.capacity = 10
    
    def add_item(self, item_name, quantity=1):
        if len(self.items) >= self.capacity:
            return False
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
        return True
    
    def remove_item(self, item_name, quantity=1):
        if item_name in self.items:
            if self.items[item_name] >= quantity:
                self.items[item_name] -= quantity
                if self.items[item_name] == 0:
                    del self.items[item_name]
                return True
        return False
    
    def has_item(self, item_name):
        return item_name in self.items
    
    def get_items(self):
        return self.items.copy()


class GameState:
    def __init__(self):
        self.score = 0
        self.turns = 0
        self.max_turns = 10
        self.inventory = Inventory()
        self.achievements = set()
        self.character_stats = {
            "health": 100,
            "strength": 10,
            "magic": 5,
            "luck": 5
        }
    
    def save(self, filename="save_game.json"):
        save_data = {
            "score": self.score,
            "turns": self.turns,
            "max_turns": self.max_turns,
            "inventory": self.inventory.items,
            "achievements": list(self.achievements),
            "character_stats": self.character_stats,
            "save_date": datetime.now().isoformat()
        }
        with open(filename, 'w') as f:
            json.dump(save_data, f)
    
    @classmethod
    def load(cls, filename="save_game.json"):
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            save_data = json.load(f)
        game_state = cls()
        game_state.score = save_data["score"]
        game_state.turns = save_data["turns"]
        game_state.max_turns = save_data["max_turns"]
        game_state.inventory.items = save_data["inventory"]
        game_state.achievements = set(save_data["achievements"])
        game_state.character_stats = save_data["character_stats"]
        return game_state


def print_sleep(message, color=Fore.RESET, sleep_duration=0.5):
    """Print a message with a specified color and pause for a duration.

    This function is used throughout the game to display text with a consistent
    visual style, applying color to enhance the user experience and pausing to
    control the pacing of the narrative. It resets the color after each message
    to prevent color bleed into subsequent outputs.

    Args:
        message (str): The text to display to the player.
        color (str): The colorama color code (e.g., Fore.GREEN). Defaults to
                     Fore.RESET (no color).
        sleep_duration (float): Seconds to pause after printing. Defaults to 0.5.

    Returns:
        None
    """
    print(color + message + Style.RESET_ALL)
    time.sleep(sleep_duration)


def display_welcome():
    """Display the game's welcome message and initial forest scene.

    This function sets the stage for the adventure by presenting a vibrant
    welcome message and describing the mystical forest environment. It
    introduces the player's first decision point: whether to follow a glowing
    light or investigate rustling bushes, establishing the interactive nature
    of the game.

    Args:
        None

    Returns:
        None
    """
    print_sleep("🌟 Welcome to the Epic Adventure Quest! 🌟", Fore.YELLOW)
    print_sleep(
        "You wake up in a mystical forest 🌲🌳, the air shimmering with "
        "magic ✨.",
        Fore.GREEN
    )
    print_sleep(
        "A glow in the distance catches your eye, but you hear "
        "rustling nearby 🐾.",
        Fore.GREEN
    )
    print_sleep("Your adventure begins now. Choose wisely!", Fore.YELLOW)


def handle_riddle(score):
    """Manage the wizard's riddle encounter, updating score and game outcome.

    The player arrives at a magical clearing where a wise wizard presents a
    riddle: 'I speak without a mouth and hear without ears. I have no body, but
    I come alive with wind. What am I?' The correct answer is 'echo' (option 2).
    The player selects from three options: ghost (1), echo (2), or bird (3).
    Input is validated to ensure only '1', '2', or '3' is accepted. A correct
    answer awards 50 points and an amulet, allowing the player to continue. An
    incorrect answer deducts 20 points and ends the game with a shadow creature
    attack. Invalid inputs prompt a retry with an error message.

    Args:
        score (int): The player's current score.

    Returns:
        tuple: (game_won, updated_score) where game_won is True if the riddle is
               solved correctly, False otherwise; updated_score is the new score.
    """
    game_state = GameState()
    game_state.score = score
    
    print_sleep(
        "You follow the glowing light to a magical clearing 🌼.",
        Fore.GREEN
    )
    print_sleep(
        "A wise old wizard 🧙‍♂️ appears, his eyes twinkling with mischief.",
        Fore.GREEN
    )
    print_sleep(
        "He says, 'Solve my riddle to gain a magical artifact! 🪄'",
        Fore.GREEN
    )
    print_sleep(
        "Riddle: 'I speak without a mouth and hear without ears. I "
        "have no body, but I come alive with wind. What am I?'",
        Fore.YELLOW
    )
    print_sleep("1️⃣ Answer: A ghost 👻.", Fore.CYAN)
    print_sleep("2️⃣ Answer: An echo 🗣️.", Fore.CYAN)
    print_sleep("3️⃣ Answer: A bird 🐦.", Fore.CYAN)
    
    # Prompt for player's answer and validate input
    while True:
        riddle_choice = input(
            Fore.MAGENTA + "Answer? (1/2/3): " + Style.RESET_ALL
        )
        if riddle_choice in ["1", "2", "3"]:
            break
        print_sleep("Please enter 1, 2, or 3.", Fore.RED)
    
    # Process the riddle answer
    if riddle_choice == "2":
        game_state.score += 50
        print_sleep(
            "'Correct!' the wizard exclaims, handing you a glowing amulet 💎.",
            Fore.GREEN
        )
        print_sleep(
            "The amulet pulses with power, making you feel invincible.",
            Fore.GREEN
        )
        print_sleep(
            "You thank the wizard and prepare to continue your quest.",
            Fore.GREEN
        )
        game_state.inventory.add_item("amulet")
        game_state.achievements.add("Riddle Master")
        return True, game_state.score
    else:
        game_state.score -= 20
        print_sleep(
            "'Wrong!' the wizard says, his voice cold. The clearing fades.",
            Fore.RED
        )
        print_sleep(
            "Shadow creatures attack from the darkness 🌑!",
            Fore.RED
        )
        print_sleep(
            "You barely escape, wounded and defeated. You lose! 😢",
            Fore.RED
        )
        return False, game_state.score


def handle_squirrel_encounter(score):
    """Handle the squirrel encounter, updating score and game outcome.

    A friendly squirrel appears, offering to guide the player. The player can
    choose to follow the squirrel to a sunny meadow (1), head toward a creepy
    cave (2), or explore a riverbank (3). Input is validated to ensure only
    '1', '2', or '3' is accepted. The meadow leads to a treasure chest and a win
    (+50 points), the cave results in a fall and a loss (-30 points), and the
    riverbank leads to a peaceful village and a win (+40 points). Invalid inputs
    prompt a retry with an error message.

    Args:
        score (int): The player's current score.

    Returns:
        tuple: (game_won, updated_score) where game_won is True for a win,
               False for a loss; updated_score is the new score.
    """
    print_sleep(
        "A friendly squirrel 🐿️ pops out, chattering excitedly.",
        Fore.GREEN
    )
    print_sleep(
        "It seems to offer guidance through the forest.",
        Fore.GREEN
    )
    print_sleep(
        "1️⃣ Follow the squirrel to a sunny meadow 🌞.",
        Fore.CYAN
    )
    print_sleep(
        "2️⃣ Head toward a creepy cave nearby 🕸️.",
        Fore.CYAN
    )
    print_sleep(
        "3️⃣ Decline and explore a riverbank instead 🌊.",
        Fore.CYAN
    )
    
    # Prompt for player's choice and validate input
    while True:
        squirrel_choice = input(
            Fore.MAGENTA + "What do you do? (1/2/3): " + Style.RESET_ALL
        )
        if squirrel_choice in ["1", "2", "3"]:
            break
        print_sleep("Please enter 1, 2, or 3.", Fore.RED)
    
    # Process the squirrel encounter choice
    if squirrel_choice == "1":
        score += 50
        print_sleep(
            "The squirrel leads you to a meadow bathed in sunlight.",
            Fore.GREEN
        )
        print_sleep(
            "You find a hidden treasure chest filled with riches! 🎁",
            Fore.GREEN
        )
        print_sleep(
            "Gold coins and jewels sparkle in your hands. You win! 🎉",
            Fore.GREEN
        )
        return True, score
    elif squirrel_choice == "2":
        score -= 30
        print_sleep(
            "The cave is dark, with eerie whispers echoing around 👻.",
            Fore.RED
        )
        print_sleep(
            "You stumble in the darkness and fall into a deep pit.",
            Fore.RED
        )
        print_sleep(
            "You lose consciousness. You lose! 😱",
            Fore.RED
        )
        return False, score
    else:
        score += 40
        print_sleep(
            "At the riverbank, you find a sturdy boat waiting 🚤.",
            Fore.GREEN
        )
        print_sleep(
            "You sail down the river, arriving at a peaceful village.",
            Fore.GREEN
        )
        print_sleep(
            "The villagers welcome you warmly. You win! 🥳",
            Fore.GREEN
        )
        return True, score


def handle_monster_encounter(score):
    """Handle the monster encounter, updating score and game outcome.

    A ferocious monster emerges, forcing the player to choose between fighting
    with a stick (1), running away (2), or hiding behind a tree (3). Input is
    validated to ensure only '1', '2', or '3' is accepted. Fighting has a random
    outcome: win (+60 points) or lose (-40 points). Running leads to a safe
    village (+30 points). Hiding has a random outcome: success (+30 points) or
    failure (-30 points). Invalid inputs prompt a retry.

    Args:
        score (int): The player's current score.

    Returns:
        tuple: (game_won, updated_score) where game_won is True for a win,
               False for a loss; updated_score is the new score.
    """
    print_sleep(
        "A monster 🐺 bursts from the bushes, growling fiercely!",
        Fore.RED
    )
    print_sleep(
        "Its eyes glow with menace as it charges toward you!",
        Fore.RED
    )
    print_sleep(
        "1️⃣ Fight the monster with a nearby stick 🪵.",
        Fore.CYAN
    )
    print_sleep(
        "2️⃣ Run away as fast as you can 🏃‍♂️.",
        Fore.CYAN
    )
    print_sleep(
        "3️⃣ Try to hide behind a tree 🌳.",
        Fore.CYAN
    )
    
    # Prompt for player's choice and validate input
    while True:
        monster_choice = input(
            Fore.MAGENTA + "What do you do? (1/2/3): " + Style.RESET_ALL
        )
        if monster_choice in ["1", "2", "3"]:
            break
        print_sleep("Please enter 1, 2, or 3.", Fore.RED)
    
    # Process the monster encounter choice
    if monster_choice == "1":
        fight_result = random.choice(["win", "lose"])
        if fight_result == "win":
            score += 60
            print_sleep(
                "You swing the stick with all your might!",
                Fore.GREEN
            )
            print_sleep(
                "The monster falls, defeated by your bravery! 💪",
                Fore.GREEN
            )
            print_sleep(
                "You find a map 🗺️ on the monster, leading to a castle.",
                Fore.GREEN
            )
            print_sleep(
                "At the castle, you're crowned a hero! You win! 👑",
                Fore.GREEN
            )
            return True, score
        else:
            score -= 40
            print_sleep(
                "The monster overpowers you, its claws slashing.",
                Fore.RED
            )
            print_sleep(
                "You collapse, defeated. You lose! 😵",
                Fore.RED
            )
            return False, score
    elif monster_choice == "2":
        score += 30
        print_sleep(
            "You sprint away, heart pounding, and escape! 🏃‍♂️💨",
            Fore.GREEN
        )
        print_sleep(
            "You stumble upon a friendly village, safe at last.",
            Fore.GREEN
        )
        print_sleep(
            "The villagers offer you shelter. You win! 🏡",
            Fore.GREEN
        )
        return True, score
    else:
        hide_result = random.choice(["success", "fail"])
        if hide_result == "success":
            score += 30
            print_sleep(
                "You hide silently behind the tree, holding your breath.",
                Fore.GREEN
            )
            print_sleep(
                "The monster leaves, and you find a safe path.",
                Fore.GREEN
            )
            print_sleep(
                "You reach a village and are welcomed. You win! 🥰",
                Fore.GREEN
            )
            return True, score
        else:
            score -= 30
            print_sleep(
                "The monster sniffs you out and attacks! 😱",
                Fore.RED
            )
            print_sleep(
                "You try to flee but are overwhelmed. You lose!",
                Fore.RED
            )
            return False, score


def handle_final_path(score):
    """Handle the final path choice for riddle solvers, updating score and outcome.

    After solving the riddle, the player faces a fork in the path: a bridge over
    a roaring river (1) or a mountain trail (2). Input is validated to ensure
    only '1' or '2' is accepted. The bridge has a random outcome: safe crossing
    to a kingdom (+50 points) or collapse into the river (-40 points). The
    mountain leads to a dragon's lair and a win (+60 points). Invalid inputs
    prompt a retry.

    Args:
        score (int): The player's current score.

    Returns:
        tuple: (game_won, updated_score) where game_won is True for a win,
               False for a loss; updated_score is the new score.
    """
    print_sleep(
        "With the amulet's power, you venture deeper into the forest.",
        Fore.GREEN
    )
    print_sleep(
        "The path splits, presenting a crucial choice:",
        Fore.GREEN
    )
    print_sleep(
        "1️⃣ A rickety bridge over a roaring river 🌉.",
        Fore.CYAN
    )
    print_sleep(
        "2️⃣ A narrow trail leading to a towering mountain ⛰️.",
        Fore.CYAN
    )
    
    # Prompt for player's choice and validate input
    while True:
        final_choice = input(
            Fore.MAGENTA + "Which path? (1/2): " + Style.RESET_ALL
        )
        if final_choice in ["1", "2"]:
            break
        print_sleep("Please enter 1 or 2.", Fore.RED)
    
    # Process the final path choice
    if final_choice == "1":
        bridge_result = random.choice(["safe", "break"])
        if bridge_result == "safe":
            score += 50
            print_sleep(
                "You carefully cross the bridge, which holds strong.",
                Fore.GREEN
            )
            print_sleep(
                "Beyond lies a grand kingdom, its gates open wide! 🏰",
                Fore.GREEN
            )
            print_sleep(
                "The king rewards your bravery. You win! 🎊",
                Fore.GREEN
            )
            return True, score
        else:
            score -= 40
            print_sleep(
                "The bridge creaks and snaps beneath you!",
                Fore.RED
            )
            print_sleep(
                "You fall into the raging river below. 🌊",
                Fore.RED
            )
            print_sleep(
                "You're swept away, defeated. You lose! 😢",
                Fore.RED
            )
            return False, score
    else:
        score += 60
        print_sleep(
            "You climb the steep trail, reaching a dragon's lair! 🐉",
            Fore.GREEN
        )
        print_sleep(
            "The dragon, awed by your amulet, bows respectfully.",
            Fore.GREEN
        )
        print_sleep(
            "It offers you a hoard of treasure. You win! 💰🎉",
            Fore.GREEN
        )
        return True, score


def handle_treasure_vault(score):
    """Handle a new treasure vault encounter, adding depth to the game.

    The player discovers a hidden vault guarded by a magical lock. They must
    choose to pick the lock (1), search for a key (2), or use a spell (3). Input
    is validated to ensure only '1', '2', or '3' is accepted. Picking the lock
    has a random outcome: success (+70 points) or trap activation (-50 points).
    Finding the key leads to a win (+60 points). Using a spell may fail (-40
    points) or succeed (+80 points). Invalid inputs prompt a retry.

    Args:
        score (int): The player's current score.

    Returns:
        tuple: (game_won, updated_score) where game_won is True for a win,
               False for a loss; updated_score is the new score.
    """
    print_sleep(
        "You stumble upon a hidden vault, its door glowing with runes.",
        Fore.GREEN
    )
    print_sleep(
        "A magical lock bars your entry, pulsing with energy.",
        Fore.GREEN
    )
    print_sleep(
        "1️⃣ Try to pick the lock with your skills 🔓.",
        Fore.CYAN
    )
    print_sleep(
        "2️⃣ Search the area for a hidden key 🗝️.",
        Fore.CYAN
    )
    print_sleep(
        "3️⃣ Attempt to cast a spell to unlock it 🪄.",
        Fore.CYAN
    )
    
    # Prompt for player's choice and validate input
    while True:
        vault_choice = input(
            Fore.MAGENTA + "What do you do? (1/2/3): " + Style.RESET_ALL
        )
        if vault_choice in ["1", "2", "3"]:
            break
        print_sleep("Please enter 1, 2, or 3.", Fore.RED)
    
    # Process the vault encounter choice
    if vault_choice == "1":
        lock_result = random.choice(["success", "trap"])
        if lock_result == "success":
            score += 70
            print_sleep(
                "Your nimble fingers unlock the vault with a click!",
                Fore.GREEN
            )
            print_sleep(
                "Inside, you find piles of gold and gems! 💎",
                Fore.GREEN
            )
            print_sleep(
                "You're now a legend of wealth. You win! 🎉",
                Fore.GREEN
            )
            return True, score
        else:
            score -= 50
            print_sleep(
                "A trap springs! Darts shoot from the walls! 🏹",
                Fore.RED
            )
            print_sleep(
                "You're wounded and retreat in defeat. You lose! 😢",
                Fore.RED
            )
            return False, score
    elif vault_choice == "2":
        score += 60
        print_sleep(
            "You search carefully and find a golden key hidden nearby.",
            Fore.GREEN
        )
        print_sleep(
            "The key unlocks the vault, revealing treasures galore!",
            Fore.GREEN
        )
        print_sleep(
            "You claim the riches and win! 💰",
            Fore.GREEN
        )
        return True, score
    else:
        spell_result = random.choice(["success", "fail"])
        if spell_result == "success":
            score += 80
            print_sleep(
                "Your spell glows brightly, and the lock melts away!",
                Fore.GREEN
            )
            print_sleep(
                "The vault opens, filled with magical artifacts! 🪄",
                Fore.GREEN
            )
            print_sleep(
                "You're hailed as a master mage. You win! 🎉",
                Fore.GREEN
            )
            return True, score
        else:
            score -= 40
            print_sleep(
                "The spell backfires, zapping you with energy! ⚡",
                Fore.RED
            )
            print_sleep(
                "You collapse, defeated by your own magic. You lose!",
                Fore.RED
            )
            return False, score


def handle_ghostly_encounter(score):
    """Handle a new ghostly encounter, adding a supernatural element.

    A ghostly figure appears, offering a cryptic challenge. The player can
    answer a question (1), offer a tribute (2), or flee (3). Input is validated
    to ensure only '1', '2', or '3' is accepted. Answering correctly earns
    +65 points and a win, while a wrong answer deducts -45 points. Offering a
    tribute leads to a win (+55 points). Fleeing has a random outcome: escape
    (+35 points) or capture (-35 points). Invalid inputs prompt a retry.

    Args:
        score (int): The player's current score.

    Returns:
        tuple: (game_won, updated_score) where game_won is True for a win,
               False for a loss; updated_score is the new score.
    """
    print_sleep(
        "A ghostly figure 👻 materializes, its voice echoing eerily.",
        Fore.CYAN
    )
    print_sleep(
        "It offers a challenge to prove your worth.",
        Fore.CYAN
    )
    print_sleep(
        "1️⃣ Answer its cryptic question.",
        Fore.CYAN
    )
    print_sleep(
        "2️⃣ Offer a tribute to appease it.",
        Fore.CYAN
    )
    print_sleep(
        "3️⃣ Flee from the ghostly presence.",
        Fore.CYAN
    )
    
    # Prompt for player's choice and validate input
    while True:
        ghost_choice = input(
            Fore.MAGENTA + "What do you do? (1/2/3): " + Style.RESET_ALL
        )
        if ghost_choice in ["1", "2", "3"]:
            break
        print_sleep("Please enter 1, 2, or 3.", Fore.RED)
    
    # Process the ghostly encounter choice
    if ghost_choice == "1":
        question_result = random.choice(["correct", "wrong"])
        if question_result == "correct":
            score += 65
            print_sleep(
                "You answer wisely: 'The moon guides the lost.'",
                Fore.GREEN
            )
            print_sleep(
                "The ghost nods and grants you passage to a shrine.",
                Fore.GREEN
            )
            print_sleep(
                "You're blessed with wisdom. You win! 🌟",
                Fore.GREEN
            )
            return True, score
        else:
            score -= 45
            print_sleep(
                "Your answer falters, angering the ghost!",
                Fore.RED
            )
            print_sleep(
                "It curses you, draining your strength. You lose! 😢",
                Fore.RED
            )
            return False, score
    elif ghost_choice == "2":
        score += 55
        print_sleep(
            "You offer a shiny trinket, and the ghost accepts.",
            Fore.GREEN
        )
        print_sleep(
            "It vanishes, leaving a path to a sacred grove.",
            Fore.GREEN
        )
        print_sleep(
            "You're honored as a peacemaker. You win! 🌿",
            Fore.GREEN
        )
        return True, score
    else:
        flee_result = random.choice(["escape", "capture"])
        if flee_result == "escape":
            score += 35
            print_sleep(
                "You run swiftly, evading the ghost's grasp!",
                Fore.GREEN
            )
            print_sleep(
                "You find a safe haven in a nearby village.",
                Fore.GREEN
            )
            print_sleep(
                "You're safe at last. You win! 🏡",
                Fore.GREEN
            )
            return True, score
        else:
            score -= 35
            print_sleep(
                "The ghost catches you, its touch freezing!",
                Fore.RED
            )
            print_sleep(
                "You're trapped in its realm. You lose! 👻",
                Fore.RED
            )
            return False, score


def play_game(score, turns, max_turns):
    """Run the main game, presenting initial choices and directing the flow.

    This function orchestrates the game by displaying the welcome scene and
    offering three initial paths: follow the glowing light (riddle), investigate
    rustling bushes (squirrel or monster), or explore a faint trail (vault or
    ghost). Input is validated to ensure only '1', '2', or '3' is accepted. The
    score is updated (+10 for a valid choice), and the game directs to the
    appropriate encounter. Random encounters add variety to the bush and trail
    paths.

    Args:
        score (int): The player's current score.
        turns (int): The current number of turns taken.
        max_turns (int): The maximum number of turns allowed.

    Returns:
        tuple: (game_won, updated_score, updated_turns) where game_won is True for a win,
               False for a loss; updated_score is the new score; updated_turns is the new turn count.
    """
    game_state = GameState()
    game_state.score = score
    game_state.turns = turns
    game_state.max_turns = max_turns
    
    display_welcome()
    print_sleep(
        f"⏳ You have {game_state.max_turns - game_state.turns} turns remaining.",
        Fore.YELLOW
    )
    print_sleep(
        "1️⃣ Follow the glowing light to the west 🌅.",
        Fore.CYAN
    )
    print_sleep(
        "2️⃣ Investigate the rustling in the bushes to the east 🐿️.",
        Fore.CYAN
    )
    print_sleep(
        "3️⃣ Explore a faint trail to the north 🛤️.",
        Fore.CYAN
    )
    
    # Prompt for player's initial choice and validate input
    while True:
        choice = input(
            Fore.MAGENTA + "What will you do? (1/2/3): " + Style.RESET_ALL
        )
        if choice in ["1", "2", "3"]:
            break
        print_sleep("Please enter 1, 2, or 3.", Fore.RED)
    
    game_state.turns += 1
    
    if game_state.turns >= game_state.max_turns:
        print_sleep(
            "⏳ Time runs out! The forest's magic fades.",
            Fore.RED
        )
        print_sleep(
            "You're lost in the woods forever. You lose! 😢",
            Fore.RED
        )
        return False, game_state.score, game_state.turns
    
    if choice == "1":
        game_state.score += 10
        print_sleep(
            "You head toward the glowing light, feeling drawn to it.",
            Fore.GREEN
        )
        result, game_state.score = handle_riddle(game_state.score)
        if result:
            game_state.inventory.add_item("amulet")
            game_state.achievements.add("Riddle Master")
            game_state.score += 20
            print_sleep(
                "The amulet guides you to a final challenge.",
                Fore.GREEN
            )
            game_state.turns += 1
            if game_state.turns >= game_state.max_turns:
                print_sleep(
                    "⏳ Time runs out! The forest's magic fades.",
                    Fore.RED
                )
                print_sleep(
                    "You're lost in the woods forever. You lose! 😢",
                    Fore.RED
                )
                return False, game_state.score, game_state.turns
            result, game_state.score = handle_final_path(game_state.score)
            if result:
                game_state.achievements.add("Forest Explorer")
            return result, game_state.score, game_state.turns
        return result, game_state.score, game_state.turns
    elif choice == "2":
        game_state.score += 10
        print_sleep(
            "You cautiously approach the rustling bushes.",
            Fore.GREEN
        )
        encounter = random.choice(["friend", "monster"])
        if encounter == "friend":
            print_sleep(
                "The bushes part to reveal a friendly creature!",
                Fore.GREEN
            )
            result, game_state.score = handle_squirrel_encounter(
                game_state.score
            )
            if result:
                game_state.achievements.add("Friend of the Forest")
            return result, game_state.score, game_state.turns
        else:
            print_sleep(
                "A terrifying roar echoes from the bushes!",
                Fore.RED
            )
            result, game_state.score = handle_monster_encounter(
                game_state.score
            )
            if result:
                game_state.achievements.add("Monster Slayer")
            return result, game_state.score, game_state.turns
    else:
        game_state.score += 10
        print_sleep(
            "You follow the faint trail, curious about its secrets.",
            Fore.GREEN
        )
        encounter = random.choice(["vault", "ghost"])
        if encounter == "vault":
            print_sleep(
                "The trail leads to a mysterious structure!",
                Fore.GREEN
            )
            result, game_state.score = handle_treasure_vault(
                game_state.score
            )
            if result:
                game_state.achievements.add("Treasure Hunter")
            return result, game_state.score, game_state.turns
        else:
            print_sleep(
                "A chill runs down your spine as the air grows cold.",
                Fore.CYAN
            )
            result, game_state.score = handle_ghostly_encounter(
                game_state.score
            )
            if result:
                game_state.achievements.add("Ghost Whisperer")
            return result, game_state.score, game_state.turns


def main():
    """Control the game loop, managing score and replay functionality.

    This function initializes the player's score, runs the game, displays the
    outcome (win or loss with the final score), and prompts for replay. The
    replay input is validated to accept only 'yes' or 'no'. If the player
    chooses to replay, the score is reset to 0, and a decorative separator is
    displayed. The game continues until the player chooses not to replay.
    """
    print_sleep("Welcome to Epic Adventure Quest! 🎮", Fore.YELLOW)
    
    # Check for existing save file
    game_state = GameState.load()
    if game_state:
        print_sleep(
            "A saved game was found. Would you like to load it? (yes/no): ",
            Fore.YELLOW
        )
        load_choice = input().lower()
        if load_choice == "yes":
            print_sleep("Game loaded successfully! 🎮", Fore.GREEN)
        else:
            game_state = GameState()
            print_sleep("Starting a new game! 🎮", Fore.GREEN)
    else:
        game_state = GameState()
        print_sleep("Starting a new game! 🎮", Fore.GREEN)
    
    while True:
        result, game_state.score, game_state.turns = play_game(
            game_state.score, 
            game_state.turns, 
            game_state.max_turns
        )
        
        # Display the game outcome
        print_sleep(
            f"🎮 Game Over! You {'won 🎉' if result else 'lost 😢'}. "
            f"Your score: {game_state.score}, Turns taken: {game_state.turns}",
            Fore.YELLOW
        )
        
        # Display inventory and achievements
        if game_state.inventory.items:
            print_sleep("\nInventory:", Fore.CYAN)
            for item, quantity in game_state.inventory.items.items():
                print_sleep(f"- {item}: {quantity}", Fore.CYAN)
        
        if game_state.achievements:
            print_sleep("\nAchievements:", Fore.YELLOW)
            for achievement in game_state.achievements:
                print_sleep(f"- {achievement}", Fore.YELLOW)
        
        # Prompt for next action
        print_sleep("\nWhat would you like to do?", Fore.YELLOW)
        print_sleep("1️⃣ Play again", Fore.CYAN)
        print_sleep("2️⃣ Save game", Fore.CYAN)
        print_sleep("3️⃣ Quit", Fore.CYAN)
        
        while True:
            choice = input(
                Fore.MAGENTA + "Choose (1/2/3): " + Style.RESET_ALL
            )
            if choice in ["1", "2", "3"]:
                break
            print_sleep("Please enter 1, 2, or 3.", Fore.RED)
        
        if choice == "1":
            game_state = GameState()  # Reset for new game
            print_sleep("\n" + "🌟" * 15 + "\n", Fore.YELLOW)
            print_sleep("A new quest awaits you!", Fore.YELLOW)
        elif choice == "2":
            game_state.save()
            print_sleep("Game saved successfully! 💾", Fore.GREEN)
            print_sleep(
                "Thanks for playing! Come back for another adventure! 👋",
                Fore.YELLOW
            )
            break
        else:
            print_sleep(
                "Thanks for playing! Come back for another adventure! 👋",
                Fore.YELLOW
            )
            break


if __name__ == "__main__":
    main()