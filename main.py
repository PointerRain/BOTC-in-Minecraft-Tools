import json

import pandas as pd

file = 'roles.xlsx'
all_sheets = pd.read_excel(file, sheet_name=None)
sheets = list(all_sheets.keys())[1:]

info = pd.read_excel(file, sheet_name=list(all_sheets.keys())[0])

ALIGNMENT_INFO = {
    'townsfolk': {'title': 'Townsfolk', 'colour': 'dark_blue', 'text_colour': 'blue', 'team': 'Good'},
    'outsider': {'title': 'Outsider', 'colour': 'dark_aqua', 'text_colour': 'aqua', 'team': 'Good'},
    'minion': {'title': 'Minion', 'colour': 'red', 'text_colour': 'red', 'team': 'Evil'},
    'demon': {'title': 'Demon', 'colour': 'dark_red', 'text_colour': 'dark_red', 'team': 'Evil'},
    'traveller': {'title': 'Traveller', 'colour': 'dark_purple', 'text_colour': 'purple'},
    'fabled': {'title': 'Fabled', 'colour': 'gold', 'text_colour': 'gold'},
}

SUBSET_ALIGNMENTS = {a: ALIGNMENT_INFO[a] for a in ALIGNMENT_INFO if a in {'townsfolk', 'outsider', 'minion', 'demon'}}
