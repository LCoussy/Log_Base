import os

def batchOpen(dir_path):
    filespath = []
    # get each name of everything in the directory
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