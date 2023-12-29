import os
import subprocess

def run_all_scripts_in_folder(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter out non-Python files
    python_files = [f for f in files if f.endswith('.py')]

    # Iterate over each Python file and run it
    for script in python_files:
        print(f"Running script: {script}")
        script_path = os.path.join(folder_path, script)
        subprocess.run(['python', script_path], check=True)

    print("Finished running all scripts.")

# Example usage
folder_path = '/path/to/your/folder'  # Replace with your folder path
run_all_scripts_in_folder(folder_path)