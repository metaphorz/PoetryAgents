"""
Fictional character names from famous novels.
"""

import random

# First names of fictional characters from famous novels
FICTIONAL_NAMES = [
    # Classic Literature
    "Elizabeth", "Darcy", "Jane", "Emma", "Catherine", "Heathcliff", "Rochester", "Jane",
    "Atticus", "Scout", "Holden", "Gatsby", "Daisy", "Tom", "Nick", "Myrtle",
    "Sherlock", "Watson", "Moriarty", "Irene", "Mycroft",
    "Harry", "Hermione", "Ron", "Dumbledore", "Severus", "Minerva", "Sirius",
    "Frodo", "Gandalf", "Aragorn", "Legolas", "Gimli", "Boromir", "Faramir",
    "Alice", "Hatter", "Cheshire", "Queen", "Rabbit",
    
    # Classic Adventure
    "Robinson", "Friday", "Gulliver", "Crusoe", "Sinbad",
    "Odysseus", "Penelope", "Telemachus", "Circe", "Athena",
    
    # Gothic Literature  
    "Dorian", "Basil", "Henry", "Victor", "Elizabeth", "Justine",
    "Dracula", "Mina", "Jonathan", "Lucy", "Van",
    
    # American Literature
    "Huckleberry", "Tom", "Becky", "Aunt", "Jim",
    "Ishmael", "Ahab", "Queequeg", "Starbuck", "Stubb",
    "Scarlett", "Rhett", "Ashley", "Melanie", "Mammy",
    
    # Russian Literature
    "Anna", "Vronsky", "Levin", "Kitty", "Dolly",
    "Pierre", "Natasha", "Andrei", "Nikolai", "Sonya",
    "Raskolnikov", "Sonia", "Porfiry", "Dunya", "Razumikhin",
    
    # Modern Literature
    "Winston", "Julia", "O'Brien", "Emmanuel", "Big",
    "Montag", "Clarisse", "Beatty", "Faber", "Mildred",
    "Yossarian", "Milo", "Major", "Chaplain", "Orr"
]

def get_random_names(count: int) -> list:
    """
    Get a list of random fictional character names.
    
    Args:
        count: Number of names to return
        
    Returns:
        List of randomly selected names
    """
    if count > len(FICTIONAL_NAMES):
        # If more names requested than available, cycle through the list
        names = FICTIONAL_NAMES * ((count // len(FICTIONAL_NAMES)) + 1)
        return random.sample(names, count)
    
    return random.sample(FICTIONAL_NAMES, count)

def get_random_name() -> str:
    """
    Get a single random fictional character name.
    
    Returns:
        A randomly selected name
    """
    return random.choice(FICTIONAL_NAMES)