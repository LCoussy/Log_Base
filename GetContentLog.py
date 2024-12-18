import re
import json
import os
import parser
import pickle

# dictionary to store cached file content
file_cache = {}

# function to read file content using pickle and implement caching
def read_file_pickle(file_path):
    # Vérifier si le contenu du fichier est déjà dans le cache
    if file_path not in file_cache:
        # Vérifier que le fichier existe et n'est pas vide
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                # Lire le fichier en utilisant pickle et stocker le contenu dans le cache
                with open(file_path, 'rb') as file:
                    file_content = pickle.load(file)
                    file_cache[file_path] = file_content
            except EOFError:
                print(f"Erreur : Le fichier {file_path} est vide ou corrompu.")
                return None
        else:
            print(f"Erreur : Le fichier {file_path} n'existe pas ou est vide.")
            return None
    # Retourner le contenu mis en cache du fichier
    return file_cache.get(file_path)



def GetContentLog(filepath):
  # print(filepath)
  data_lost, data_blocked, data_user = [], [], []
  startbuffer = False
  buffer = ''
  date_pattern = r"^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}"
  delimiter_pattern = re.compile(r"(\d+|aucune)\s+lignes?", re.IGNORECASE)
  errerRequest = re.compile(r"résultat de concaténation de chaîne trop long", re.IGNORECASE)
  isRequest = True
  isBlocked = False
  with open(filepath, 'r', encoding='ISO-8859-1') as f:
    # start_index = 0
    for line in f:
      if ("résultat de concaténation de chaîne trop long" in line):
        print("Erreur Requête trop longue")
        return {"ERROR" : "Erreur Requête trop longue"}
      if (re.match(delimiter_pattern, line)):
        # print("eh merdes")
        # print(line)
        isRequest = False
        startbuffer = False
        continue

      dates = re.match(date_pattern, line)
      if (isRequest):
        # print(dates)
        if re.match(date_pattern, buffer) and dates:
          # print("buffer: "+buffer)
          if (isBlocked):
            data_blocked.append(parser.parse_request(buffer, "BLOCKED"))
          else:
            data_lost.append(parser.parse_request(buffer, "LOST")) #traitement de la requête
          # print("added buffer to data")
        if (dates):
          startbuffer = True
          buffer = line
          if ("BLOQUE" in line):
            isBlocked = True
          else:
            isBlocked = False
          # print("buffer started")
          continue
        if startbuffer:
          # print(startbuffer)
          # print(re.match(date_pattern, buffer), dates)
          if re.match(date_pattern, buffer) and not dates:
            # print("----"+buffer)
            buffer += line
          else :
            startbuffer = False
        # print(buffer+"-----------------")
      else:
        # print("hey c'est un user")
        # print(line)
        if startbuffer:
          if dates and not re.match(date_pattern, buffer):
            # print("buffer: "+buffer)
            buffer += line
            data_user.append(parser.parse_user(buffer)) #traitement de l'utilisateur
            # print(buffer+"-----------------")
            startbuffer = False
          else:
            # print("-----------"+buffer)
            buffer += line
        if not dates and startbuffer == False:
          startbuffer = True
          buffer = line
          continue

  # data = parser.update_logs_with_duration(data)

  data = {"LOST": data_lost, "BLOCKED": data_blocked, "USER": data_user}
  return data

def parse(filepath):
  # print(filepath)
  # patternFilePath = re.compile(r'(?:[^/]+)(?=\.)')
  patternFilePath = re.compile(r'[^\\|/]+(?=\.[^.]+$)')
  match = patternFilePath.search(filepath)
  # print(match.group(0))
  if match:
    file_name = match.group(0)
    if '/' in filepath:
      cache_file_path = f'__logcache__/{file_name}.pkl'
    elif '\\' in filepath:
      cache_file_path = f'__logcache__\\{file_name}.pkl'
    if not os.path.exists(cache_file_path):
        if not os.path.exists('__logcache__'):
          os.makedirs('__logcache__')
        # Écrire les données dans le fichier en utilisant pickle
        with open(cache_file_path, 'wb') as file:
            pickle.dump(GetContentLog(filepath), file)
        print(f"Cache file created: {cache_file_path}")
    # Lire et retourner les données mises en cache à partir du fichier
    result = read_file_pickle(cache_file_path)
    if result is not None:
        return result
    else:
        print("Erreur : Impossible de lire les données mises en cache.")
        return None
  else:
      print("Erreur : Nom de fichier non trouvé.")
      return None
  # if not os.access('__logcache__/{}.pkl'.format(match.group(0)), os.F_OK):
  #   # write data to file using pickle
  #   print("no access to cache file")
  #   with open('__logcache__/{}.pkl'.format(match.group(0)), 'wb') as file:
  #       pickle.dump(GetContentLog(filepath), file)

# print(parse("/home/coussy/log-base/ihm_kivy/log/GCE_15-45-02_75_02-12-2024.txt"))

  # # read and print cached data from file
  # result = read_file_pickle('__logcache__/{}.pkl'.format(match.group(0)))
  # return result


# filepath = 'GCE_14-45-02_75_02-12-2024'
# fileExtension='.txt'
# get_content = GetContentLog("/home/coussy/log-base/ihm_kivy/log/GCE_14-45-02_75_02-12-2024.txt")
# for i in get_content:
#   print(i)
# print(get_content)

# data to be pickled and cached

# write data to file using pickle