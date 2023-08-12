import shutil
import os


def clear_files_in_path(directory_path):
    try:
        files = os.listdir(directory_path)
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        pass

def copy_file_to_path(source_file_path, destination_path):
    shutil.copy(source_file_path, destination_path)
