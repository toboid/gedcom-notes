import os
from family_tree import FamilyTree
import pprint

file_path = './Stableford Family Tree.ged'
output_dir = './files'

tree = FamilyTree(file_path)


class NoteFile:
    def __init__(self, entity_name):
        self.file_path = os.path.join(output_dir, entity_name + '.md')
        self.file = None

    def __enter__(self):
        self.file = open(self.file_path, 'w', encoding='utf-8')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def write(self, text):
        self.file.write(text)

    def write_line(self, text):
        self.file.write(f'{text}  \n')

    def write_meta(self, name, value):
        self.write_line(f'[{name}:: {value}]')

    def write_meta_hidden(self, name, value):
        self.write_line(f'({name}:: {value})')


for individual in tree.individuals:
    note_file_path = os.path.join(
        output_dir, individual.get_display_name() + '.md')

    with NoteFile(individual.get_display_name()) as file:
        file.write_line('## Attributes')
        file.write_meta('ID', individual.get_pointer())
        file.write_meta('Name', individual.get_display_name())
        file.write_meta(
            'Lived', f'{individual.get_birth_year()}-{individual.get_death_year()}')
        file.write_meta('Sex', individual.get_gender())
        file.write_meta('Born', individual.get_date_of_birth())
        file.write_meta('Place of birth', individual.get_place_of_birth())
        file.write_meta('Passed-away', individual.get_date_of_death())
        file.write_meta('Place of death', individual.get_place_of_death())
        file.write_line('')

        file.write_line('## Parents')
        for parent in individual.get_parents():
            file.write_meta_hidden(
                'Parent', f'[[{parent.get_display_name()}]]')
        file.write_line('')

        file.write_line('## Children')
        for child in individual.get_children():
            file.write_meta_hidden(
                'Child', f'[[{child.get_display_name()}]]')
        file.write_line('')

        file.write_line('## Partners')
        for partner in individual.get_partners():
            file.write_line(partner.get_display_name())
