import configparser
import os

def get_sections_and_values(index_file_path):
    """Parse the index file and return all section names and values as a set of strings."""
    config = configparser.ConfigParser()
    config.read(index_file_path, encoding='utf-8')

    index_items = set()

    for section in config.sections():
        index_items.add(section)
        for key, value in config.items(section):
            index_items.add(value)

    return index_items

def clean_ini_file(index_items, ini_file_path):
    """Remove sections from the ini file if their name is in the index items."""
    config = configparser.ConfigParser()
    config.read(ini_file_path, encoding='utf-8')

    sections_to_remove = []
    for section in config.sections():
        if section in index_items:
            sections_to_remove.append(section)

    for section in sections_to_remove:
        config.remove_section(section)

    # Write the cleaned file back
    with open(ini_file_path, 'w', encoding='utf-8') as cleaned_file:
        config.write(cleaned_file)

    return len(sections_to_remove)

def main():
    index_file = input("Please enter the name of the index file (including .ini extension): ")
    ini_file_to_clean = input("Please enter the name of the file to be cleaned (including .ini extension): ")

    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the paths to the index and ini files
    index_file_path = os.path.join(script_directory, index_file)
    ini_file_path = os.path.join(script_directory, ini_file_to_clean)

    # Check if the files exist
    if not os.path.exists(index_file_path):
        print(f"Index file '{index_file}' not found in {script_directory}.")
        input("Press Enter to exit...")
        return

    if not os.path.exists(ini_file_path):
        print(f"File to be cleaned '{ini_file_to_clean}' not found in {script_directory}.")
        input("Press Enter to exit...")
        return

    # Parse the index file to get section names and values
    index_items = get_sections_and_values(index_file_path)

    # Clean the ini file by removing sections that match the index items
    sections_deleted = clean_ini_file(index_items, ini_file_path)

    # Print the result
    print(f"Total number of sections deleted: {sections_deleted}")

    # Wait for user input before exiting
    input("Processing complete. Press Enter to exit...")

if __name__ == '__main__':
    main()
