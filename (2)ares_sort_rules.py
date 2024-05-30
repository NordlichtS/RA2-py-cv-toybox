import configparser
import os

def get_ini_file(prompt):
    while True:
        file_name = input(prompt)
        if os.path.isfile(file_name):
            return file_name
        else:
            print(f"The file '{file_name}' does not exist in this folder. Please provide a valid file name.")

def create_sorted_ini_files(index_file, rules_file):
    index_config = configparser.ConfigParser()
    index_config.read(index_file)
    
    rules_config = configparser.ConfigParser()
    rules_config.read(rules_file)
    
    for section in index_config.sections():
        sorted_file_name = f"sort_{section}.ini"
        
        with open(sorted_file_name, 'w') as sorted_file:
            sorted_config = configparser.ConfigParser()
            sorted_config[section] = index_config[section]
            sorted_config.write(sorted_file)
            print(f"Created new file: '{sorted_file_name}'")

        game_objects = index_config[section].values()
        moved_sections_count = 0
        
        for game_object in game_objects:
            if rules_config.has_section(game_object):
                with open(sorted_file_name, 'a') as sorted_file:
                    sorted_config = configparser.ConfigParser()
                    sorted_config[game_object] = rules_config[game_object]
                    sorted_config.write(sorted_file)
                    #print(f"Moved section '{game_object}' to file '{sorted_file_name}'")
                    moved_sections_count += 1
                
                rules_config.remove_section(game_object)
        
        print(f"Total sections moved to '{sorted_file_name}': {moved_sections_count}")

    # Write the updated rules file
    with open(rules_file, 'w') as rules_file_handle:
        rules_config.write(rules_file_handle)
        print(f"Updated the rules file: '{rules_file}'")

if __name__ == "__main__":
    index_file = get_ini_file("Please provide the name of the index INI file: ")
    rules_file = get_ini_file("Please provide the name of the rules INI file: ")
    create_sorted_ini_files(index_file, rules_file)
