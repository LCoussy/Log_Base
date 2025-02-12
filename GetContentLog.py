import re
import os
import parser
import pickle

# dictionary to store cached file content
file_cache = {}

# function to read file content using pickle and implement caching
def read_file_pickle(file_path):
    # Check if the file is already in cache
    if file_path not in file_cache:
        # Check if the file exist and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                # Read the file using pickle and store the content in the cache
                with open(file_path, 'rb') as file:
                    file_content = pickle.load(file)
                    file_cache[file_path] = file_content
            except EOFError:
                print(f"Erreur : Le fichier {file_path} est vide ou corrompu.")
                return None
        else:
            print(f"Erreur : Le fichier {file_path} n'existe pas ou est vide.")
            return None
    # Return the content put in the cache
    return file_cache.get(file_path)



def GetContentLog(filepath):
  data_lost, data_blocked, data_user = [], [], []
  startbuffer = False
  buffer = ''
  date_pattern = r"^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}"
  delimiter_pattern = re.compile(r"(\d+|aucune)\s+lignes?", re.IGNORECASE)
  errerRequest = re.compile(r"résultat de concaténation de chaîne trop long", re.IGNORECASE)
  isRequest = True
  isBlocked = False
  with open(filepath, 'r', encoding='ISO-8859-1') as f:
    if ("ALTER SYSTEM KILL SESSION" in f):
      print("Erreur Alter System Kill Session")
      return {"ERROR" : "Erreur Alter System Kill Session"}
    for line in f:
      if ("résultat de concaténation de chaîne trop long" in line):
        print("Erreur Requête trop longue")
        return {"ERROR" : "Erreur Requête trop longue"}
      if (re.match(delimiter_pattern, line)):
        isRequest = False
        startbuffer = False
        continue

      dates = re.match(date_pattern, line)
      if (isRequest):
        if re.match(date_pattern, buffer) and dates:
          if (isBlocked):
            data_blocked.append(parser.parse_request(buffer, "BLOCKED"))
          else:
            data_lost.append(parser.parse_request(buffer, "LOST")) # Request processing
        if (dates):
          startbuffer = True
          buffer = line
          if ("BLOQUE" in line):
            isBlocked = True
          else:
            isBlocked = False
          continue
        if startbuffer:
          if re.match(date_pattern, buffer) and not dates:
            buffer += line
          else :
            startbuffer = False
      else:
        if startbuffer:
          if dates and not re.match(date_pattern, buffer):
            buffer += line
            data_user.append(parser.parse_user(buffer)) # User processing
            startbuffer = False
          else:
            buffer += line
        if not dates and startbuffer == False:
          startbuffer = True
          buffer = line
          continue


  data = {"LOST": data_lost, "BLOCKED": data_blocked, "USER": data_user}
  return data

def parse(filepath):
  patternFilePath = re.compile(r'[^\\|/]+(?=\.[^.]+$)')
  match = patternFilePath.search(filepath)
  if match:
    file_name = match.group(0)
    if '/' in filepath:
      cache_file_path = f'__logcache__/{file_name}.pkl'
    elif '\\' in filepath:
      cache_file_path = f'__logcache__\\{file_name}.pkl'
    if not os.path.exists(cache_file_path):
        if not os.path.exists('__logcache__'):
          os.makedirs('__logcache__')
        # Write data in the fiel using pickle
        with open(cache_file_path, 'wb') as file:
            print(f"Cache file created: {cache_file_path}")
            pickle.dump(GetContentLog(filepath), file)
        print(f"Cache file filled: {cache_file_path}")
    #  Read and return cached data from the file
    result = read_file_pickle(cache_file_path)
    if result is not None:
        return result
    else:
        print("Erreur : Impossible de lire les données mises en cache.")
        return None
  else:
      print("Erreur : Nom de fichier non trouvé.")
      return None