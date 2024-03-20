import os
import argparse
from lib.family_tree import FamilyTree
from lib.obsidian_note import ObsidianNote

args_parser = argparse.ArgumentParser(
    description='Creates obsidian notes from a gedcom file.')
args_parser.add_argument('--file_path', type=str,
                         required=True, help='The path to the gedcom input file')
args_parser.add_argument('--output_dir', type=str,
                         required=True, help='The directory to output the notes')
args = args_parser.parse_args()
file_path = args.file_path
output_dir = args.output_dir

tree = FamilyTree(file_path)

for individual in tree.individuals:
    with ObsidianNote(individual.get_file_name(), output_dir) as note:
        note.write_h2('Attributes')
        note.write_meta('ID', individual.get_pointer())
        note.write_meta('Name', individual.get_display_name())
        note.write_meta(
            'Lived', f'{individual.get_birth_year()}-{individual.get_death_year()}')
        note.write_meta('Sex', individual.get_gender())
        note.write_meta('Born', individual.get_date_of_birth())
        note.write_meta('Place of birth', individual.get_place_of_birth())
        note.write_meta('Passed-away', individual.get_date_of_death())
        note.write_meta('Place of death', individual.get_place_of_death())
        note.write_line('')

        note.write_h2('Parents')
        for parent in individual.get_parents():
            note.write_meta_hidden(
                'Parent', note.linked_note(parent.get_file_name()))
        note.write_line('')

        note.write_h2('Children')
        for child in individual.get_children():
            note.write_meta_hidden(
                'Child', note.linked_note(child.get_file_name()))
        note.write_line('')

        note.write_h2('Partners')
        for partner in individual.get_partners():
            note.write_meta_hidden(
                'Partner', note.linked_note(partner.get_file_name()))
