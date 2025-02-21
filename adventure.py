# Your code goes here'''Enhance your text-based adventure game by using dictionaries to manage enchanted artifacts \'''
import random

def display_player_status(player_stats):
    """Display the player's current health and attack power."""
    print(f"Health: {player_stats['health']}, Attack: {player_stats['attack']}")

def acquire_item(inventory, item):
    """Add an item to the inventory."""
    inventory.append(item)
    print(f"You acquired a {item}!")

def display_inventory(inventory):
    """Display the current inventory."""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for i, item in enumerate(inventory, start=1):
            print(f"{i}. {item}")

def discover_artifact(player_stats, artifacts, artifact_name):
    """Discover an artifact and update player stats based on its effect."""
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
    """Find a unique clue and add it to the clues set."""
    if new_clue not in clues:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    else:
        print("You already know this clue.")
    return clues

def combat_encounter(player_stats, monster_health):
    """Simulate a combat encounter using player stats."""
    print("\nA monster appears! Prepare for battle.")
    while player_stats['health'] > 0 and monster_health > 0:
        print(f"You attack and deal {player_stats['attack']} damage!")
        monster_health -= player_stats['attack']
        if monster_health <= 0:
            print("You defeated the monster!")
            break
        print("The monster attacks you for 10 damage!")
        player_stats['health'] -= 10
        display_player_status(player_stats)
        if player_stats['health'] <= 0:
            print("Game Over! You have been defeated.")
            return None
    return player_stats

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """Explore dungeon rooms, collect items, and face challenges."""
    for room in dungeon_rooms:
        desc, item, challenge_type, outcome = room
        print(f"\nYou enter: {desc}")
        if item:
            acquire_item(inventory, item)
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
                print("With the Staff of Wisdom, you decipher the clues and bypass future puzzles!")
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
                solve = input("Do you want to solve the puzzle? (yes/no): ").lower()
                if solve == "yes" and random.choice([True, False]):
                    print(outcome[0])
                else:
                    print(outcome[1])
                    player_stats['health'] = max(player_stats['health'] + outcome[2], 0)
        display_inventory(inventory)
        display_player_status(player_stats)
    return player_stats, inventory, clues

def main():
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()

    artifacts = {
        "amulet_of_vitality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts your attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "A staff imbued with ancient wisdom.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    dungeon_rooms = [
        ("Dusty library", "key", "puzzle", \
         ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap", \
         ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle", \
         ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]

    print("Welcome to the Enchanted Adventure!")
    display_player_status(player_stats)

    monster_health = 70
    player_stats = combat_encounter(player_stats, monster_health)
    if not player_stats:
        return

    if random.random() < 0.3 and artifacts:
        artifact_name = random.choice(list(artifacts.keys()))
        player_stats, artifacts = discover_artifact(\
            player_stats, artifacts, artifact_name)

    player_stats, inventory, clues = enter_dungeon(\
        player_stats, inventory, dungeon_rooms, clues, artifacts)

    print("\n--- Game End ---")
    display_player_status(player_stats)
    print("Final Inventory:")
    display_inventory(inventory)
    print("Clues:")
    if clues:
        for clue in clues:
            print(f"- {clue}")
    else:
        print("No clues found.")

if __name__ == "__main__":
    main()
