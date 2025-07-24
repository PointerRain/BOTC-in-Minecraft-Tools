import json
from textwrap import wrap

from main import ALIGNMENT_INFO

MAX_PAGE_LINES = 14
APPROX_PAGE_WIDTH = 23

COLOURS = {
    'black': '0', 'dark_blue': '1', 'dark_green': '2', 'dark_aqua': '3', 'dark_red': '4',
    'dark_purple': '5', 'gold': '6', 'gray': '7', 'dark_gray': '8', 'blue': '9', 'green': 'a',
    'aqua': 'b', 'red': 'c', 'light_purple': 'd', 'yellow': 'e', 'white': 'f', 'reset': 'r',
    'bold': 'l', 'italic': 'o', 'underlined': 'n', 'strikethrough': 'm', 'obfuscated': 'k',
    'townsfolk_title': '1', 'townsfolk': '9', 'outsider_title': '3', 'outsider': '3',
    'minion_title': 'c', 'minion': 'c', 'demon_title': '4', 'demon': '4',
    'traveller_title': '5', 'traveller': 'd', 'fabled_title': '6', 'fabled': '6',
}

def formatted_text(text, colour='black', bold=False, italic=False, underlined=False,
                   strikethrough=False, obfuscated=False):
    """Formats text with Minecraft-style formatting codes."""
    codes = ''
    if colour != 'black':
        codes += f"§{COLOURS.get(colour, '0')}"
    if bold: codes += '§l'
    if italic: codes += '§o'
    if underlined: codes += '§n'
    if strikethrough: codes += '§m'
    if obfuscated: codes += '§k'
    return f"{codes}{text}§r"

def count_approx_lines(text):
    """Counts the approximate number of lines in a text block."""
    return len(wrap(text, APPROX_PAGE_WIDTH, fix_sentence_endings=True))

class Script:
    def __init__(self, script_file, colour='black', text_colour=None):
        with open('roles.json', 'r', encoding='utf8') as f:
            self.roles_data = json.load(f)
        with open(script_file, 'r', encoding='utf8') as f:
            script = json.load(f)
        self.title = script[0].get('name', 'Untitled Script')
        self.author = script[0].get('author', '')
        self.role_ids = script[1:]
        self.roles = [role for role in self.roles_data if role['id'] in self.role_ids]
        self.colour = colour
        self.text_colour = text_colour or colour
        self.pages = []
        self.data = {}

    def write_script(self):
        self.add_title_page()
        self.add_character_lists(['townsfolk', 'outsider', 'minion', 'demon', 'traveller', 'fabled'])
        self.add_character_pages(['townsfolk', 'outsider', 'minion', 'demon', 'traveller', 'fabled'])
        self.add_jinxes(self.get_jinxes())
        self.data = {'author': self.author, 'pages': self.pages}

    def add_title_page(self):
        page = ['', '', formatted_text(self.title, colour=self.colour, bold=True, underlined=True)]
        if self.author:
            page += ['', '', formatted_text(f'By {self.author}', colour=self.text_colour, bold=True)]
        self.pages.append('\n'.join(page))

    def get_roles_by_alignment(self, alignment):
        return [role for role in self.roles if role.get('team') == alignment]

    def add_character_lists(self, alignments):
        page = []
        for alignment in alignments:
            info = ALIGNMENT_INFO[alignment]
            characters = [r['name'] for r in self.get_roles_by_alignment(alignment)]
            title = info['title'] + (f" - {info.get('team', '')}" if info.get('team') else '')
            header = formatted_text(title, colour=info['colour'], bold=True, underlined=True)

            while True:
                # Write the alignment header
                # If there are no characters left, break the loop
                if not characters:
                    break
                # If on a new page and the page will be too long, add the current page to the pages list and start a new page
                elif len(page) <= 1 and len(page) + len(characters) + 1 > MAX_PAGE_LINES:
                    page = [header] + [f'- {formatted_text(character, colour=info["text_colour"])}'
                                       for character in characters[:MAX_PAGE_LINES - 1]]
                    characters = characters[MAX_PAGE_LINES - 1:]
                    self.pages.append('\n'.join(page))
                    page = []
                # If the characters don't fit on the current page, add the current page to the pages list and start a new page
                elif len(page) + len(characters) + (0 if len(page) <= 1 else 2) > MAX_PAGE_LINES:
                    self.pages.append('\n'.join(page))
                    page = []
                # Otherwise, add the characters to the current page
                else:
                    if len(page) > 0:
                        page.append('')
                    page.append(header)
                    page += [f'- {formatted_text(character, colour=info["text_colour"])}'
                             for character in characters]
                    break

        self.pages.append('\n'.join(page))

    def add_character_pages(self, alignments):
        for alignment in alignments:
            page = []
            page_length = 0
            info = ALIGNMENT_INFO[alignment]
            roles = self.get_roles_by_alignment(alignment)
            if not roles:
                continue
            title = info['title'] + (f" - {info.get('team', '')}" if info.get('team') else '')

            for role in roles:
                if len(page) > 1 and page_length + count_approx_lines(role['ability']) + 2 > MAX_PAGE_LINES:
                    self.pages.append('\n'.join(page))
                    page = []
                    page_length = 0
                page += [
                    formatted_text(role['name'], colour=info['colour'], bold=True, underlined=True),
                    formatted_text(title, colour=info['text_colour']),
                    role.get('ability', 'No ability')
                ]
                page_length += count_approx_lines(role['ability']) + 2
            if page:
                self.pages.append('\n'.join(page))

            # pairs = [(i, j) if j is not None else (i,) for i, j in zip_longest(roles[::2], roles[1::2])]
            #
            # for pair in pairs:
            #     page = []
            #     for role in pair:
            #         page += [
            #             formatted_text(role['name'], colour=info['colour'], bold=True, underlined=True),
            #             formatted_text(title, colour=info['text_colour']),
            #             role.get('ability', 'No ability')
            #         ]
            #     self.pages.append('\n'.join(page))



    def get_jinxes(self):
        jinxes = []
        for role in self.roles:
            for jinx in role.get('jinxes', []):
                if jinx['id'] in self.role_ids:
                    other = next((r for r in self.roles if r['id'] == jinx['id']), None)
                    if other:
                        jinxes.append({'characters': (role, other), 'reason': jinx['reason']})
        return jinxes

    def add_jinxes(self, jinxes):
        if not jinxes:
            return
        for jinx in jinxes:
            first, second = jinx['characters']
            reason = jinx.get('reason', 'No ability')
            page = [
                formatted_text('Jinxes', colour='gold', bold=True, underlined=True),
                f'{formatted_text(first["name"], colour=first["team"])} + {formatted_text(second["name"], colour=second["team"])}',
                reason
            ]
            self.pages.append('\n'.join(page))

    def save(self):
        if not self.data:
            raise ValueError("No script data to save. Please call write_script() first.")
        with open(f'generated/scripts/{self.title.replace(" ", "_")}.json', 'w', encoding='utf8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

script = Script('scripts/trouble_brewing.json', 'dark_red', 'red')
# script = Script('scripts/sects_and_violets.json', 'dark_purple', 'light_purple')
# script = Script('scripts/bad_moon_rising.json', 'gold', 'gold')
# script = Script('scripts/separation_church_state.json', 'dark_purple', 'light_purple')
# script = Script('scripts/whalebucket.json')
script.write_script()
script.save()