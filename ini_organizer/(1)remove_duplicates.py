import os

def parse_ini_file(file_path):
    sections = {}
    current_section = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                if current_section not in sections:
                    sections[current_section] = []
                else:
                    print(f"Duplicate section '{current_section}' found and removed.")
                    sections[current_section].append('DUPLICATE_SECTION')
            elif '=' in line and current_section:
                key = line.split('=')[0].strip().lower()
                value = '='.join(line.split('=')[1:]).strip()
                if any(k.split('=')[0].strip().lower() == key for k in sections[current_section]):
                    print(f"Duplicate option '{key}' found in section '{current_section}' and removed.")
                    sections[current_section].append(f'DUPLICATE_OPTION={value}')
                else:
                    sections[current_section].append(line)
            elif current_section:
                sections[current_section].append(line)

    return sections

def write_ini_file(file_path, sections):
    with open(file_path, 'w', encoding='utf-8') as file:
        for section, lines in sections.items():
            if 'DUPLICATE_SECTION' not in lines:
                file.write(f'[{section}]\n')
                for line in lines:
                    if not line.startswith('DUPLICATE_OPTION='):
                        file.write(f'{line}\n')

def remove_duplicates(sections):
    cleaned_sections = {}
    duplicated_sections_count = 0
    duplicated_options_count = 0

    for section, lines in sections.items():
        if 'DUPLICATE_SECTION' in lines:
            duplicated_sections_count += 1
            continue

        cleaned_lines = []
        seen_options = set()

        for line in lines:
            if '=' in line:
                option = line.split('=')[0].strip().lower()
                if option in seen_options:
                    duplicated_options_count += 1
                    print(f"Duplicate option '{option}' found in section '{section}' and removed.")
                    continue
                seen_options.add(option)

            cleaned_lines.append(line)

        cleaned_sections[section] = cleaned_lines

    return cleaned_sections, duplicated_sections_count, duplicated_options_count

def process_ini_file(file_path):
    # Parse the original ini file
    sections = parse_ini_file(file_path)

    # Remove duplicated sections and options
    cleaned_sections, duplicated_sections_count, duplicated_options_count = remove_duplicates(sections)

    # Write the cleaned sections back to the file
    write_ini_file(file_path, cleaned_sections)

    print(f"Processed file saved: {file_path}")
    print(f"Total duplicated sections removed: {duplicated_sections_count}")
    print(f"Total duplicated options removed: {duplicated_options_count}")

def main():
    # Prompt the user to enter the name of the ini file
    input_file = input("Please enter the name of the ini file (including .ini extension): ")

    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the ini file
    ini_file_path = os.path.join(script_directory, input_file)

    # Check if the file exists
    if not os.path.exists(ini_file_path):
        print(f"File '{input_file}' not found in {script_directory}.")
        input("Press Enter to exit...")
        return

    # Process the ini file
    process_ini_file(ini_file_path)

    # Wait for user input before exiting
    input("Processing complete. Press Enter to exit...")

if __name__ == '__main__':
    main()
