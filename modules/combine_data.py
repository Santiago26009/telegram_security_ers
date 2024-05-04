from .functions import combine_json_files

def combine_data():

    # Specify the folder containing JSON files and the output file name
    json_folder_path = './reports-json/'
    json_output_file = json_folder_path + '_combined_data.json'

    combine_json_files(json_folder_path, json_output_file)

# Call the function to execute the functionality
if __name__ == "__main__":
    combine_data()