import os

def batchOpen(dir_path):
    """
    Recursively retrieves all file paths from a given directory and its subdirectories.

    This function takes a directory path as input and iterates through all the files
    and subdirectories within it. If the current path is a directory, it recursively
    processes the contents. If it is a file, the full file path is added to the result list.

    Args:
        dir_path (str): The path to the directory or file to be processed.

    Returns:
        list: A list of full file paths found in the directory and its subdirectories.
        If a single file path is provided instead of a directory, it returns a list containing
        just that file's path.
    """
    filespath = []
    if os.path.isdir(dir_path):
        for filename in os.listdir(dir_path):
            # create full path
            full_path = os.path.join(dir_path, filename)
            # check if it's a directory
            if os.path.isdir(full_path):
                filespath.extend(batchOpen(full_path))  # Recursion for directories
            else:
                filespath.append(full_path)  # Add file path to the list
    else:
        filespath.append(os.path.realpath(dir_path))
    return filespath