import json

import pandas as pd

from main import ALIGNMENT_INFO, SUBSET_ALIGNMENTS

file = 'roles.xlsx'
all_sheets = pd.read_excel(file, sheet_name=None)
sheets = list(all_sheets.keys())[1:]
info = pd.read_excel(file, sheet_name=list(all_sheets.keys())[0])

data = {
    "model": {
        "type": "minecraft:select",
        "property": "minecraft:component",
        "component": "minecraft:custom_name",
        "cases": [],
        "fallback": {
            "type": "minecraft:model",
            "model": "minecraft:item/paper"
        }
    }
}


def write_character(name, file, alignment):
    character_cases = {}
    for al in SUBSET_ALIGNMENTS:
        character_cases[f'{al}/{file}'] = character_cases.get(f'{al}/{name}', []) + [
            {'italic': False,
             'extra': [{'color': ALIGNMENT_INFO[al]['text_colour'],
                        'bold': True,
                        'text': name}],
             'text': ''}]
    character_cases[f'{alignment}/{file}'] = character_cases.get(f'{alignment}/{name}', []) + [
        name,
        f'iregex:.*{name}.*',
    ]

    return character_cases


def write_alignment(alignment, column1, column2):
    """
    Writes the model cases for a given alignment based on the specified columns in the info DataFrame.
    :param alignment: The alignment to write cases for (e.g., 'townsfolk', 'outsider').
    :param column1: The index of the first column in the info DataFrame to use for names.
    :param column2: The index of the second column in the info DataFrame to use for file names.
    :return: A dictionary containing the alignment cases with character names and their corresponding file names.
    """
    alignment_cases = {}
    for row in zip(info.iloc[:, column1], info.iloc[:, column2]):
        if pd.isnull(row[0]) or pd.isnull(row[1]):
            continue
        for k, v in write_character(*row, alignment).items():
            alignment_cases[k] = alignment_cases.get(k, []) + v
    return alignment_cases


cases = {}
for n, alignment in enumerate(SUBSET_ALIGNMENTS.keys()):
    alignment_cases = write_alignment(alignment, 2 * n, 2 * n + 1)
    for k, v in alignment_cases.items():
        cases[k] = cases.get(k, []) + v

for k, v in cases.items():
    print(k, v)
    data['model']['cases'].append({
        "when": v,
        "model": {
            "type": "minecraft:model",
            "model": f"botctokens:{k}"
        }
    })
with open('generated/paper.json', 'w') as f:
    # f.write(json.dumps(data, indent=0, separators=(',',':')).replace('"{', "{").replace('}"', "}")
    #                                       .replace('\\"', '"').replace('\n', ''))
    json.dump(data, f, indent=2, separators=(',', ':'))
