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
args_parser.add_argument('--root_person', type=str,
                         required=False, help='Only include ancestors of this person')
args = args_parser.parse_args()
file_path = args.file_path
output_dir = args.output_dir
root_person_search = args.root_person

tree = FamilyTree(file_path)

if root_person_search:
    root_person = tree.find(root_person_search)
    output_file_suffix = root_person.get_display_name()
    people = [root_person]
    people.extend(tree.get_ancestors(root_person))
else:
    people = tree.individuals
    output_file_suffix = 'all'

with ObsidianNote('Mermaid tree ' + output_file_suffix, output_dir) as note:
    note.write_line('```mermaid')
    note.write_line('  graph TD;')

    def write_indented(text):
        note.write_line(f'      {text}')

    for person in people:
        id = person.get_id()
        write_indented(f'{id}("{person.get_display_name()} {person.get_birth_year()}")')
        parents = ' & '.join([p.get_id() for p in person.get_parents()])
        if len(parents):
            write_indented(f'{parents} --- {id}')
        write_indented(f'class {id} internal-link;')
