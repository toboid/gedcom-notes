import os

def parse_gedcom(file_path):
    individuals = {}
    current_id = None  # Use None to indicate no individual has been initialized yet
    parsing_birth_date = False  # Flag to indicate if the next DATE tag is for birth

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(' ', 2)
            level = parts[0]
            tag = parts[1] if len(parts) > 1 else ""
            data = parts[2] if len(parts) == 3 else ""

            if level == '0' and tag != 'INDI' and current_id:
                parsing_birth_date = False  # Reset flag if we're moving out of an individual's context

            if level == '0' and data.endswith('INDI'):
                current_id = tag
                individuals[current_id] = {"name": "", "dob": "", "details": []}
            elif current_id:  # Ensure operations are only performed when an individual has been initialized
                if tag == 'NAME':
                    individuals[current_id]["name"] = data.replace('/', '').strip()
                elif tag == 'SEX':
                    individuals[current_id]["details"].append(f'Sex: {data}')
                elif tag == 'BIRT':
                    parsing_birth_date = True
                elif tag == 'DATE' and parsing_birth_date:
                    individuals[current_id]["dob"] = data
                    individuals[current_id]["details"].append(f'Date of Birth: {data}')
                    parsing_birth_date = False  # Reset flag after recording DOB
                elif data:  # Ensure we don't append empty lines
                    individuals[current_id]["details"].append(line.strip())

    return individuals

# Ensure the file_path is correctly set to where your GEDCOM file is located
file_path = './Stableford Family Tree.ged'
individuals_revised = parse_gedcom(file_path)

# Specify the directory where you want to save the markdown files
output_dir = './files'
os.makedirs(output_dir, exist_ok=True)

# Creating markdown files for each individual with revised data, including DOB
for ind_id, ind_info in individuals_revised.items():
    file_name = ind_info["name"].replace(" ", "-") + ".md"
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# {ind_info['name']}\n\n")
        for detail in ind_info["details"]:
            md_file.write(detail + '\n')
    break;
