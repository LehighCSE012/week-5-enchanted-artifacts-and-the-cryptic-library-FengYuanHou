'''Enhance your text-based adventure game by using dictionaries to manage enchanted artifacts \
    and sets to handle unique clues in a cryptic library.'''
import random

def display_player_status(player_stats):
    """Displays the player's current health and attack power."""
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")

def acquire_item(inventory, item):
    """Adds an item to the inventory and returns the updated inventory."""
    inventory.append(item)
    print(f"You acquired a {item}!")
    return inventory

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discovers an artifact and updates player stats based on its effect."""
    artifact = artifacts.get(artifact_name)
    if artifact:
        print(f"You found the {artifact_name}: {artifact['description']}")
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"Your health increased by {artifact['power']}!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"Your attack increased by {artifact['power']}!")
        del artifacts[artifact_name]
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Finds a new clue and adds it to the set if unique."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """Explore dungeon rooms, collect items, and face challenges."""
    for room in dungeon_rooms:
        desc, item, challenge_type, outcome = room
        print(f"\nYou enter: {desc}")
        if item:
            inventory = acquire_item(inventory, item)

        if challenge_type == "library":
            print("You explore ancient texts in the Cryptic Library.")
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            found_clues = random.sample(possible_clues, 2)
            for clue in found_clues:
                clues = find_clue(clues, clue)
            if "staff_of_wisdom" in inventory:
                print("With the Staff of Wisdom, you bypass future puzzles!")

        elif challenge_type == "trap":
            print("You see a potential trap!")
            action = input("Do you want to disarm or bypass it? ").lower()
            if action == "disarm" and random.choice([True, False]):
                print(outcome[0])
            else:
                print(outcome[1])
                player_stats['health'] = max(player_stats['health'] + outcome[2], 0)

        elif challenge_type == "puzzle":
            print("You encounter a puzzle!")
            if "staff_of_wisdom" in inventory:
                print("Using the Staff of Wisdom, you bypass the puzzle!")
            else:
                try:
                    solve = input("Do you want to solve the puzzle? (yes/no): ").lower()
                except EOFError:
                    solve = "no"
                if solve == "yes":
                    success = random.choice([True, False])
                    print(outcome[0] if success else outcome[1])
                    player_stats['health'] = max(player_stats['health'] + outcome[2], 0)
                else:
                    print("You chose to skip the puzzle.")

        display_player_status(player_stats)
    return player_stats, inventory, clues

def main():
    """Main game loop."""
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall", "healing potion", "none", None),
        ("Small room", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]

    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    display_player_status(player_stats)

    if random.random() < 0.3:
        artifact_name = random.choice(list(artifacts.keys()))
        player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
        display_player_status(player_stats)

    if player_stats['health'] > 0:
        player_stats, inventory, clues = enter_dungeon(
            player_stats, inventory, dungeon_rooms, clues, artifacts)

        print("\n--- Game End ---")
        display_player_status(player_stats)
        print("Final Inventory:", inventory)
        print("Clues:", clues)

if __name__ == "__main__":
    main()
