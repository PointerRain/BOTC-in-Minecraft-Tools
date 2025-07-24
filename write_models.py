import json
import os
from main import ALIGNMENT_INFO

for filename in os.listdir('icons'):
    if not filename.endswith('.png'):
        continue
    print(filename)

    with open(f'generated/models/townsfolk/{filename.removesuffix(".png")}.json', 'w') as f:
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"botctokens:item/townsfolk/{filename.removesuffix('.png')}"
            }
        }
        f.write(json.dumps(data, indent=2))
    with open(f'generated/models/outsider/{filename.removesuffix(".png")}.json', 'w') as f:
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"botctokens:item/outsider/{filename.removesuffix('.png')}"
            }
        }
        f.write(json.dumps(data, indent=2))
    with open(f'generated/models/minion/{filename.removesuffix(".png")}.json', 'w') as f:
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"botctokens:item/minion/{filename.removesuffix('.png')}"
            }
        }
        f.write(json.dumps(data, indent=2))
    with open(f'generated/models/demon/{filename.removesuffix(".png")}.json', 'w') as f:
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"botctokens:item/demon/{filename.removesuffix('.png')}"
            }
        }
        f.write(json.dumps(data, indent=2))
    with open(f'generated/models/traveller/{filename.removesuffix(".png")}.json', 'w') as f:
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"botctokens:item/traveller/{filename.removesuffix('.png')}"
            }
        }
        f.write(json.dumps(data, indent=2))
    with open(f'generated/models/fabled/{filename.removesuffix(".png")}.json', 'w') as f:
        data = {
            "parent": "minecraft:item/generated",
            "textures": {
                "layer0": f"botctokens:item/fabled/{filename.removesuffix('.png')}"
            }
        }
        f.write(json.dumps(data, indent=2))


