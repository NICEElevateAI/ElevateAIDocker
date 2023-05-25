import sys
import os
import json
import time
import argparse
from ElevateAIPythonSDK import ElevateAI
from rich.live import Live
from rich.table import Table

# Update the interaction status for each uploaded file
def update_results(upload_results, config):
    updated_results = []
    for row in upload_results:
        response = ElevateAI.GetInteractionStatus(row[1], config["api_token"])
        response_json = response.json()
        new_row = (row[0], row[1], response_json["status"])
        updated_results.append(new_row)
    return updated_results

# Generate the table to display the interaction status
def generate_table(results) -> Table:
    table = Table()
    table.add_column("Filename")
    table.add_column("Identifier")
    table.add_column("Status")

    for row in results:
        table.add_row(row[0], row[1], row[2])

    return table

# Process command-line arguments
def process_args(args):
    parser = argparse.ArgumentParser(description='Upload audio files to ElevateAI.')
    parser.add_argument('-f', '--files', nargs='+', help='Audio files to upload')
    parser.add_argument('-d', '--directory', help='Directory containing audio files to upload')
    parser.add_argument('-c', '--config', default='config.json', help='Path to config.json file')
    arguments = parser.parse_args(args)
    if arguments.files is None and arguments.directory is None:
        parser.print_help()
        sys.exit(0)
    
    audio_files = []
    if arguments.files:
        audio_files.extend(arguments.files)
    if arguments.directory:
        for root, dirs, files in os.walk(arguments.directory):
            for file in files:
                audio_files.append(os.path.join(root, file))
    
    return audio_files, arguments.config


# Check if the config file and audio files exist and load the config
def check_files(config_file, audio_files):
    if not os.path.isfile(config_file):
        print(f"Config file '{config_file}' not found. A config.json file is required.")
        sys.exit(1)

    if not all(os.path.isfile(file) for file in audio_files):
        print("One or more audio files do not exist. Please check the file paths and try again.")
        sys.exit(1)

    with open(config_file) as f:
        config = json.load(f)

    return config

# Upload each audio file and store the interaction status
def upload_files(audio_files, config):

    print("\nUploading files...\n")

    upload_results = []
    for file in audio_files:
        response = upload_file(file, config)

        if response.status_code == 201:
            upload_results.append((file, response.json()["interactionIdentifier"], "Uploaded Successfully"))
        else:
            upload_results.append((file, response.json()["interactionIdentifier"], "Upload error"))

    return upload_results

# Upload a single audio file and return the declare response
def upload_file(file_path, config):
    token = config['api_token']
    language_tag = "en-us"
    version = "default"
    transcription_mode = "highAccuracy"

    file_name = os.path.basename(file_path)

    declare_response = ElevateAI.DeclareAudioInteraction(language_tag, version, None, token, transcription_mode, False)
    declare_json = declare_response.json()
    interaction_id = declare_json["interactionIdentifier"]

    ElevateAI.UploadInteraction(interaction_id, token, file_path, file_name)
    return declare_response

def main(args):
    try:
        audio_files, config_file = process_args(args)
        config = check_files(config_file, audio_files)
        upload_results = upload_files(audio_files, config)

        print("\nPress C-c to exit. Processing will not be interrupted.\n")

        with Live(generate_table(upload_results), refresh_per_second=4) as live:
            while True:
                time.sleep(15)
                upload_results = update_results(upload_results, config)
                live.update(generate_table(upload_results))
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])


