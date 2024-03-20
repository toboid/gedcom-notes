import os


class ObsidianNote:
    def __init__(self, file_name, output_dir):
        self.file_path = os.path.join(output_dir, file_name + '.md')
        self.file = None

    def __enter__(self):
        self.file = open(self.file_path, 'w', encoding='utf-8')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def write(self, text):
        self.file.write(text)

    def write_h2(self, text):
        self.write_line(f'## {text}')

    def write_line(self, text):
        self.file.write(f'{text}  \n')

    def write_meta(self, name, value):
        self.write_line(f'[{name}:: {value}]')

    def write_meta_hidden(self, name, value):
        self.write_line(f'({name}:: {value})')

    def linked_note(self, text):
        return f'[[{text}]]'
