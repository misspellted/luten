
# For now, the dialogs are hard coded. TODO: Load them from a file.

shop_walk_in:list[tuple[bool, str, int]] = [ # TOOD: Maybe make a Conversation to encapsulate this lovley type?
  (False, "Hello, there! Looking for loot?", 1_000_000*300),
  (False, "I've got the supplies you're gonna need in your search of the dungeon!", 1_000_000*400),
  (True, "Sounds good. Let's see here...", 1_000_000*500),
]
