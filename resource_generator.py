import json

class Item:
    def __init__(self, name, directory=None, texture=None):
        self.name = name
        self.directory = directory or "items"
        self.primary_name = name[0] if isinstance(name, list) else name
        self.texture = texture if texture else self.primary_name.lower().replace(' ', '_')
        self.filename = f"{self.directory}/{self.texture}.png"

    def __repr__(self):
        return f"Item(name={self.name}, filename={self.filename})"

    def write_model(self):
        return NotImplemented

resources = {
    "minecraft:snowball": [
        Item(["White Ball", "White Bouncy Ball"], "items/balls"),
        Item(["Red Ball", "Red Bouncy Ball", "Bouncy Ball"], "items/balls"),
        Item(["Blue Ball", "Blue Bouncy Ball"], "items/balls"),
        Item(["Green Ball", "Green Bouncy Ball"], "items/balls"),
        Item(["Yellow Ball", "Yellow Bouncy Ball"], "items/balls"),
        Item(["Purple Ball", "Purple Bouncy Ball"], "items/balls"),
        Item(["Black Ball", "Black Bouncy Ball"], "items/balls"),
        Item(["Pink Ball", "Pink Bouncy Ball"], "items/balls"),
        Item(["Orange Ball", "Orange Bouncy Ball"], "items/balls"),
        Item(["Brown Ball", "Brown Bouncy Ball"], "items/balls"),
        Item(["Grey Ball", "Grey Bouncy Ball"], "items/balls"),
        Item(["Light Blue Ball", "Light Blue Bouncy Ball"], "items/balls"),
        Item(["Lime Ball", "Lime Bouncy Ball"], "items/balls"),
        Item(["Cyan Ball", "Cyan Bouncy Ball"], "items/balls"),
        Item(["Magenta Ball", "Magenta Bouncy Ball"], "items/balls"),
        Item(["Light Grey Ball", "Light Grey Bouncy Ball"], "items/balls"),
    ],
    "minecraft:totem_of_undying": [
        Item("GoldenRedstone", "items/totems"),
        Item("JoeGaming", "items/totems"),
    ],
}

print(resources)