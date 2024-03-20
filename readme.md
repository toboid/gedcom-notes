# Family tree parser
This is a personal project to generate markdown notes and mermaid diagrams from a gedcom family tree file. Sharing here for others to reference but please keep in mind this was developed for my personal use and to practice a bit of Python.

## Available scripts

### create_notes.py
Creates an Obsidian note for each person in the gedcom file. Each note contains main (not all)
details and links to family members.

Note that currently the output_dir must already exist.
```sh
python src/create_notes.py --output_dir="./files" --file_path="./tree.ged"
```

## Useful python commands
Load the venv
```sh
source ./bin/activate
```

Add a new dependency
```sh
pip install <dep-name>
# now update deps list
pip freeze > requirements.txt
```

Install dependencies
```sh
pip install -r requirements.txt
```
