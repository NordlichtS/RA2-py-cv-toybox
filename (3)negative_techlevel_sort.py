import os
import configparser

def load_ini_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    return config

def write_ini_file(file_path, config):
    with open(file_path, 'w', encoding='utf-8') as file:
        config.write(file)

def process_ini_file(file_path):
    # Load the original ini file
    config = load_ini_file(file_path)

    # Create a new empty config for sections with negative TechLevel
    new_config = configparser.ConfigParser()

    # Counters for moved and not moved sections
    moved_sections_count = 0
    not_moved_sections_count = 0

    # Iterate through the sections and process them
    sections_to_remove = []
    for section in config.sections():
        if any(option.lower() in ['undeploysinto', 'deploysinto'] for option in config[section]):
            not_moved_sections_count += 1
            continue
        
        if 'techlevel' in (key.lower() for key in config[section]):
            techlevel_value = config[section]['TechLevel']
            try:
                techlevel_value = int(techlevel_value)
                if techlevel_value < 0:
                    # Move the section to the new config
                    new_config[section] = config[section]
                    sections_to_remove.append(section)
                    moved_sections_count += 1
                else:
                    not_moved_sections_count += 1
            except ValueError:
                not_moved_sections_count += 1
                continue
        else:
            not_moved_sections_count += 1

    # Remove sections with negative TechLevel from the original config
    for section in sections_to_remove:
        config.remove_section(section)

    # Determine the new file name
    new_file_path = file_path.replace('.ini', '_negative.ini')

    # Write the new config to the new file
    write_ini_file(new_file_path, new_config)
    print(f"New file with negative TechLevel sections created: {new_file_path}")

    # Write the updated original config back to the original file
    write_ini_file(file_path, config)
    print(f"Original file updated without negative TechLevel sections: {file_path}")

    # Print the counts
    print(f"Total sections moved: {moved_sections_count}")
    print(f"Total sections not moved: {not_moved_sections_count}")

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
