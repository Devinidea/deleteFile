import os
import shutil
import time
from datetime import datetime

def delete_old_folders(root_folder, log_file_name, days=7):
    # Validate input parameters
    if not os.path.isdir(root_folder):
        raise ValueError(f"Invalid root folder: {root_folder}")
    if not isinstance(log_file_name, str) or not log_file_name.endswith('.log'):
        raise ValueError("Log file name must be a string ending with .log")
    if not isinstance(days, int) or days < 1:
        raise ValueError("Days must be a positive integer")

    # Get the current time
    now = time.time()
    # Calculate the cutoff time
    cutoff = now - (days * 86400)  # 86400 seconds in a day

    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path for the log file within the script's directory
    log_file_path = os.path.join(script_dir, log_file_name)

    # Open the log file
    with open(log_file_path, 'a') as log:
        deleted_count = 0
        error_count = 0
        
        # Traverse the root folder
        for root, dirs, files in os.walk(root_folder):
            # Check the depth of the current folder
            depth = root[len(root_folder):].count(os.sep)
            if depth == 1:  # Only process second-level folders
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        # Get the creation time of the folder
                        creation_time = os.path.getctime(dir_path)
                        # If the folder's creation time is earlier than the cutoff, delete it
                        if creation_time < cutoff:
                            print(f"Deleting folder: {dir_path}")
                            shutil.rmtree(dir_path)
                            # Log the deletion in the log file with timestamp to seconds
                            log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            log.write(f"Deleted folder: {dir_path} at {log_time}\n")
                            deleted_count += 1
                    except Exception as e:
                        error_count += 1
                        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log.write(f"Error deleting {dir_path} at {log_time}: {str(e)}\n")
                        print(f"Error deleting {dir_path}: {str(e)}")
        
        # Log summary
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"Operation completed at {log_time}. Deleted {deleted_count} folders, {error_count} errors.\n")
        print(f"Operation completed. Deleted {deleted_count} folders, {error_count} errors.")

def main():
    # Define the root folder and log file name
    root_folder = r"C:\Users\Tech20\Nextcloud2"  # Replace with your folder path
    log_file_name = "deletefile.log"  # Log file name

    # Call the function to delete old folders
    delete_old_folders(root_folder, log_file_name)

if __name__ == "__main__":
    main()
