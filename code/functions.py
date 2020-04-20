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
    (person_1, person_2, interaction_score, description) = args[0]

    person_1.update_relationship(person_2, interaction_score)

    # Print description
    print(description)

# Ask for an item from person
def ask_for_item(*args):
    (person_1, person_2, item, description, already_done) = args[0]

    if item.name in person_2.inventory:
        person_1.get_item(item)
        person_2.inventory.pop(item.name.lower())
        # Print description
        print(description)
    else:
        print(already_done)

def redeem_item(*args):
    (person, buy_item, use_item, description) = args[0]

    # Use the item
    person.use_item(use_item)

    # Add bought item to inventory
    person.get_item(buy_item)

    print(description)


