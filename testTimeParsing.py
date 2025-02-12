import GetContentLog
import os
import time
import re
def parse_files_in_directory(directory):
  start_time = time.time()
  for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    GetContentLog.parse(filepath=filepath)
  end_time = time.time()
  print(f"Time taken to parse files in directory: {end_time - start_time} seconds")

def read_logcache_files(directory):
  start_time = time.time()
  for filename in os.listdir(directory):
    if filename.endswith('.pkl'):
      filepath = os.path.join(directory, filename)
      with open(filepath, 'r') as file:
        file.read()
  end_time = time.time()
  print(f"Time taken to read .pkg files in __logcache__: {end_time - start_time} seconds")

# Example usage
directory_path = '/home/coussy/Downloads/GCE'
parse_files_in_directory(directory_path)

# logcache_directory_path = '/home/coussy/log-base/ihm_kivy/__logcache__'
# read_logcache_files(logcache_directory_path)