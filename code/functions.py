# Special functions

# Print the given description
def describe_something(*args):
    (description) = args[0]
    print(description)

# Summon character to given location
def call_to_location(*args):
    (location, npc, description, already_done) = args[0]

    # Move person to location
    if npc.name not in location.characters:
        npc.set_location(location)
        # Print description
        print(description)
    else:
        print(already_done)

# Interact with person
def interaction_with_person(*args):
    (player, npc, interaction_score, description) = args[0]

    player.update_relationship(npc, interaction_score)

    # Print description
    print(description)

# Ask for an item from person
def ask_for_item(*args):
    (player, npc, item, description, already_done) = args[0]

    if item.name in npc.inventory:
        player.get_item(item)
        npc.inventory.pop(item.name.lower())
        # Print description
        print(description)
    else:
        print(already_done)

def redeem_item(*args):
    (player, buy_item, use_item, description) = args[0]

    # Use the item
    player.use_item(use_item)

    # Add bought item to inventory
    player.add_item(buy_item)

    print(description)


