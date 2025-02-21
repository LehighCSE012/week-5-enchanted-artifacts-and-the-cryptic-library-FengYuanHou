'''Enhance your text-based adventure game by using dictionaries to manage enchanted artifacts \
    and sets to handle unique clues in a cryptic library.'''
import random

def display_player_status(player_stats):
    """Display player's current health and attack power."""
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")

def acquire_item(inventory, item):
    """Add an item to the inventory and print confirmation."""
    if item not in inventory:
        inventory.append(item)
        print(f"You acquired a {item}!")
    else:
        print(f"You already have a {item}.")
    return inventory

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discover an artifact, apply its effect, and remove it from the artifact pool."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You found the {artifact_name}! {artifact['description']}")
        if artifact['effect'] == 'increases health':
            player_stats['health'] += artifact['power']
            print(f"Your health increased by {artifact['power']}!")
        elif artifact['effect'] == 'enhances attack':
            player_stats['attack'] += artifact['power']
            print(f"Your attack increased by {artifact['power']}!")
        del artifacts[artifact_name]
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Add a unique clue to the clues set."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """Explore dungeon rooms, collect items, and face challenges."""
    for desc, item, challenge_type, outcome in dungeon_rooms:
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
            try:
                action = input("Do you want to disarm or bypass it? (disarm/bypass): ").lower()
            except EOFError:
                action = "bypass"
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
                if solve == "yes" and random.choice([True, False]):
                    print(outcome[0])
                else:
                    print(outcome[1])
                    player_stats['health'] = max(player_stats['health'] + outcome[2], 0)

        display_player_status(player_stats)
    return player_stats, inventory, clues

def main():
    """Main function to run the adventure game."""
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
            "description": "Glowing amulet that boosts life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Ring that enhances attack power.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff filled with ancient knowledge.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle failed.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]

    print("Welcome to the Adventure Game!")
    display_player_status(player_stats)

    # Enter dungeon
    player_stats, inventory, clues = enter_dungeon(player_stats, inventory,
                                                   dungeon_rooms, clues, artifacts)

    # Random artifact discovery
    if random.random() < 0.3 and artifacts:
        artifact_name = random.choice(list(artifacts.keys()))
        player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)

    print("\n--- Game End ---")
    display_player_status(player_stats)
    print(f"Final Inventory: {inventory}")
    print(f"Clues Discovered: {', '.join(clues) if clues else 'None'}")

if __name__ == "__main__":
    main()
