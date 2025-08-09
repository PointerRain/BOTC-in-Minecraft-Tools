import json
from textwrap import wrap

from main import ALIGNMENT_INFO

MAX_PAGE_LINES = 14
APPROX_PAGE_WIDTH = 23

COLOURS = {
    'black': '0', 'dark_blue': '1', 'dark_green': '2', 'dark_aqua': '3', 'dark_red': '4',
    'dark_purple': '5', 'gold': '6', 'gray': '7', 'dark_gray': '8', 'blue': '9', 'green': 'a',
    'aqua': 'b', 'red': 'c', 'light_purple': 'd', 'yellow': 'e', 'white': 'f', 'reset': 'r',
    'bold': 'l', 'italic': 'o', 'underlined': 'n', 'strikethrough': 'm', 'obfuscated': 'k'
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
    def __init__(self, script_file, colour='black', text_colour=None, included_types=None):
        with open('roles.json', 'r', encoding='utf8') as f:
            self.roles_data = json.load(f)
        with open(script_file, 'r', encoding='utf8') as f:
            script = json.load(f)
        self.title = script[0].get('name', 'Untitled Script')
        self.author = script[0].get('author', '')
        self.colour = colour
        self.text_colour = text_colour or colour
        self.included_types = included_types
        if included_types is None:
            self.included_types = ['townsfolk', 'outsider', 'minion', 'demon', 'traveller', 'fabled']
        self.role_ids = script[1:]
        self.roles = [role for role in self.roles_data if role['id'] in self.role_ids and role['team'] in self.included_types]
        self.pages = []
        self.data = {}

    def write_script(self):
        """Generates the script content."""
        self.add_title_page()
        self.add_character_lists(self.included_types)
        self.add_character_pages(self.included_types)
        self.add_jinxes(self.get_jinxes())
        for night in ('first', 'other'):
            self.write_night_order(night, self.get_night_order(night))
        self.data = {'author': self.author, 'pages': self.pages}

    def write_section(self, header: list | str, items: list[list | str], max_breaks: int = 3, ignore_width=False) -> None:
        """
        Writes a section to the script with a header and multiple items.
        """
        header = header if isinstance(header, list) else [header]
        page = [header]
        page_length = sum(count_approx_lines(line) for line in header) if not ignore_width else len(header)
        for item in items:
            item = item if isinstance(item, list) else [item]
            new_lines = sum(count_approx_lines(line) for line in item) if not ignore_width else len(item)

            # If the item is too long to fit on the current page, write the current page and start a new one
            if len(page) > 1 and page_length + new_lines > MAX_PAGE_LINES:
                self.write_page(page, page_length, max_breaks=max_breaks)
                page = [header]
                page_length = sum(count_approx_lines(line) for line in header) if not ignore_width else len(header)

            page.append(item)
            page_length += new_lines

        # If there are still items left after the loop, write the remaining page
        if len(page) > 1:
            self.write_page(page, page_length, max_breaks=max_breaks)

    def write_page(self, content: list, page_length: int, max_breaks: int = 3):
        """
        Writes a page to the script, ensuring it fits within the maximum number of lines.
        Adds breaks between items if there are enough spare lines.

        Parameters:
            content (list): The content of the page as a list of strings.
            page_length (int): The current length of the page in lines.
            max_breaks (int): The maximum number of breaks to insert between items.
        """
        page = []
        spare_lines = MAX_PAGE_LINES - page_length - 1
        if spare_lines >= 1 and len(content) > 2:
            breaks = spare_lines // (len(content) - 2)
            breaks = min(breaks, max_breaks)  # Limit breaks to a maximum of 2
        else:
            breaks = 0
        for n, item in enumerate(content):
            page.extend(item)
            if breaks > 0 and 0 < n < len(content) - 1:
                # Insert breaks between items if there are enough spare lines
                page.extend([''] * breaks)
        self.pages.append('\n'.join(page))

    def add_title_page(self):
        """
        Adds the title page to the script.
        The title page includes the script title and author.
        """
        page = ['', '', formatted_text(self.title, colour=self.colour, bold=True, underlined=True)]
        if self.author:
            page += ['', '', formatted_text(f'By {self.author}', colour=self.text_colour, bold=True)]
        self.pages.append('\n'.join(page))

    def get_roles_by_alignment(self, alignment):
        """Returns a list of roles from the script that match the given alignment."""
        return [role for role in self.roles if role.get('team') == alignment]

    def add_character_lists(self, alignments: list):
        """
        Adds character lists to the script based on the provided alignments.
        Each alignment will have its own page, with a header and a list of characters.

        Parameters:
            alignments (list): A list of alignments to include in the script.
        """
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

    def add_character_pages(self, alignments):
        """Adds character pages to the script for each alignment."""
        for alignment in alignments:
            info = ALIGNMENT_INFO[alignment]
            roles = self.get_roles_by_alignment(alignment)
            if not roles:
                continue

            header = info['title'] + (f" - {info.get('team', '')}" if info.get('team') else '')
            items = [[
                formatted_text(role['name'], colour=info['colour'], bold=True, underlined=True),
                formatted_text(header, colour=info['text_colour']),
                role.get('ability', 'No ability')
            ] for role in roles]
            self.write_section([], items)

    def get_jinxes(self) -> list[dict]:
        """
        Returns a list of jinxes from the script.
        Each jinx is represented as a dictionary with 'characters' (a tuple of two roles)
        and 'reason' (the reason for the jinx).
        """
        jinxes = []
        for role in self.roles:
            for jinx in role.get('jinxes', []):
                if jinx['id'] in self.role_ids:
                    other = next((r for r in self.roles if r['id'] == jinx['id']), None)
                    if other:
                        jinxes.append({'characters': (role, other), 'reason': jinx['reason']})
        return jinxes

    def add_jinxes(self, jinxes: list[dict]) -> None:
        """Adds a section for jinxes to the script."""
        if not jinxes:
            return

        header = formatted_text('Jinxes', colour='gold', bold=True, underlined=True)
        items = [[
                formatted_text(role['name'], colour=info['colour'], bold=True, underlined=True),
                formatted_text(header, colour=info['text_colour']),
                role.get('ability', 'No ability')
            ] for role in roles]
        self.write_section(header, items)

    def get_night_order(self, night: str) -> list[dict]:
        """
        Returns a list of roles ordered by their first or other night actions.

        Parameters:
            night (str): Either 'first' or 'other', indicating which night to get the order for.
        """
        if night not in ('first', 'other'):
            raise ValueError("Night must be either 'first' or 'other'.")
        order = [r for r in self.roles if r.get(f'{night}Night') is not None and r.get(f'{night}NightReminder')]
        return sorted(order, key=lambda r: r.get(f'{night}Night'))

    def write_night_order(self, night: str, order: list = None) -> None:
        """
        Writes the night order section to the script.
        Parameters:
            night (str): Either 'first' or 'other', indicating which night to write the order for.
            order (list): A list of roles ordered by their first or other night actions
        """
        if not order:
            return
        if night not in ('first', 'other'):
            raise ValueError("Night must be either 'first' or 'other'.")
        header = formatted_text(f'{night.capitalize()} Night Order', bold=True, underlined=True)
        items = [f'{n + 1:>2}. ' + formatted_text(role['name'], colour=ALIGNMENT_INFO[role['team']]['text_colour'])
                 for n, role in enumerate(order)]
        self.write_section(header, items, max_breaks=1, ignore_width=True)

    def save(self, file=None) -> None:
        """ Saves the script data to a JSON file."""
        if not self.data:
            raise ValueError("No script data to save. Please call write_script() first.")
        with open(file or f'generated/scripts/{self.title.replace(" ", "_")}.json', 'w', encoding='utf8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)


character_types = ['townsfolk', 'outsider', 'minion', 'demon', 'fabled']

script = Script('scripts/trouble_brewing.json', 'dark_red', 'red', character_types)
script = Script('scripts/sects_and_violets.json', 'dark_purple', 'light_purple', character_types)
# script = Script('scripts/bad_moon_rising.json', 'gold', 'gold', character_types)
# script = Script('scripts/separation_church_state.json', 'dark_purple', 'light_purple')
# script = Script('scripts/whalebucket.json', included_types=character_types)
script.write_script()
script.save()
