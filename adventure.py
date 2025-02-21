'''Enhance your text-based adventure game by using dictionaries to manage enchanted artifacts \
    and sets to handle unique clues in a cryptic library.'''
import random

def display_player_status(player_stats):
    """Display current player health and attack stats."""
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")

def acquire_item(inventory, item):
    """Add an item to the inventory."""
    if item not in inventory:
        inventory.append(item)
        print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """Display the player's inventory."""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for index, item in enumerate(inventory, start=1):
            print(f"{index}. {item}")

def find_clue(clues, new_clue):
    """Add a unique clue to the set of clues."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discover an artifact and apply its effects to player stats."""
    artifact = artifacts.get(artifact_name)
    if artifact:
        print(f"You found the {artifact_name}! {artifact['description']}")
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
        print(f"Effect: {artifact['effect']}. Power: {artifact['power']}")
        del artifacts[artifact_name]
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """Explore dungeon rooms, collect items, and face challenges."""
    for room in dungeon_rooms:
        try:
            desc, item, challenge_type, outcome = room
        except ValueError:
            print(f"Invalid room structure: {room}")
            continue

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
                action = input("Do you want to disarm or bypass it? ").lower()
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
    """Main game loop."""
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
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

    print("Welcome to the Enchanted Dungeon!")
    display_player_status(player_stats)

    player_stats, inventory, clues = enter_dungeon(
        player_stats, inventory, dungeon_rooms, clues, artifacts
    )

    print("\n--- Game End ---")
    display_player_status(player_stats)
    print("Final Inventory:")
    display_inventory(inventory)
    print("Clues:")
    for clue in clues:
        print(f"- {clue}")

if __name__ == "__main__":
    main()
