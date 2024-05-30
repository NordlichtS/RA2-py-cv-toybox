import os
import configparser

def parse_ini_file(file_path):
    sections = {}
    current_section = None
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith(';') or not line:
                continue
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].strip()
                sections[current_section] = []
            elif current_section is not None:
                sections[current_section].append(line)
    return sections

def write_ini_file(file_path, sections):
    with open(file_path, 'w', encoding='utf-8') as file:
        for section, lines in sections.items():
            file.write(f'[{section}]\n')
            for line in lines:
                file.write(f'{line}\n')
            file.write('\n')

def copy_sections(game_objects_index, rules):
    script_directory = os.path.dirname(os.path.abspath(__file__))

    game_objects_index_path = os.path.join(script_directory, game_objects_index)
    rules_path = os.path.join(script_directory, rules)

    if not os.path.exists(game_objects_index_path):
        print(f"File {game_objects_index} not found.")
        return

    if not os.path.exists(rules_path):
        print(f"File {rules} not found.")
        return

    print(f"Found {game_objects_index_path}")
    print(f"Found {rules_path}")

    game_objects_index_data = parse_ini_file(game_objects_index_path)
    rules_data = parse_ini_file(rules_path)

    for list_name, items in game_objects_index_data.items():
        new_ini_path = os.path.join(script_directory, f'{list_name}.ini')
        new_sections = {list_name: items}

        copied_sections_count = 0

        for item in items:
            if '=' in item:
                _, game_object = item.split('=', 1)
                game_object = game_object.strip()
                if game_object.upper() in (name.upper() for name in rules_data.keys()):
                    for key in rules_data.keys():
                        if key.upper() == game_object.upper():
                            new_sections[key] = rules_data[key]
                            copied_sections_count += 1
                            break

        write_ini_file(new_ini_path, new_sections)
        print(f"Copied {copied_sections_count} sections to {new_ini_path}")


def find_ini_files():
    # Get the directory of the script
    script_directory = os.path.dirname(__file__)

    # Construct paths to game_objects_index.ini and rules.ini in the same directory as the script
    game_objects_index_filename = os.path.join(script_directory, 'game_objects_index.ini')
    rules_filename = os.path.join(script_directory, 'rules.ini')

    # Check if the provided files exist
    if not os.path.isfile(game_objects_index_filename):
        print(f"Error: {game_objects_index_filename} not found.")
        return None, None

    if not os.path.isfile(rules_filename):
        print(f"Error: {rules_filename} not found.")
        return None, None

    print(f"Found {game_objects_index_filename} and {rules_filename}.")
    return game_objects_index_filename, rules_filename

def create_new_ini_files(game_objects_index):
    # Get the directory of the script
    script_directory = os.path.dirname(__file__)

    # Read the game_objects_index.ini file with UTF-8 encoding
    config = configparser.ConfigParser()
    config.read(game_objects_index, encoding='utf-8')

    # Process each section in game_objects_index.ini
    for section in config.sections():
        # Create a new configparser object for the new ini file
        new_ini = configparser.ConfigParser()

        # Write the new ini file with UTF-8 encoding
        new_ini_filename = os.path.join(script_directory, f'{section}.ini')
        with open(new_ini_filename, 'w', encoding='utf-8') as new_file:
            new_ini.write(new_file)
            print(f"Created new INI file: {new_ini_filename}")


if __name__ == "__main__":
    # Step 1: Find game_objects_index.ini and rules.ini
    game_objects_index, rules = find_ini_files()

    if game_objects_index and rules:
        # Step 2: Create new INI files for each section in game_objects_index.ini
        create_new_ini_files(game_objects_index)

        # Step 3: Copy sections from rules.ini into the new INI files
        copy_sections(game_objects_index, rules)

        # final fix
        # restore_placeholders()

    input("Press Enter to close the script.")
