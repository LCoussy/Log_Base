import re
import json
from datetime import datetime
import pandas as pd
import data_handler as dh

def parse_blocked_request(content):
    # Match pour la date et l'heure (deuxième occurrence)
    blocking_date_match = re.search(r'\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\s+\w+\s+(\d{2}/\d{2}/\d{2})\s+(\d{2}:\d{2}:\d{2})', content)
    if blocking_date_match:
        blocking_date = blocking_date_match.group(1)  # Deuxième date
        blocking_time = blocking_date_match.group(2)  # Deuxième heure
        
        # Combiner la date et l'heure, puis convertir au format YYYY-MM-DDTHH:MM:SS
        try:
            combined_datetime = datetime.strptime(f"{blocking_date} {blocking_time}", "%d/%m/%y %H:%M:%S")
            iso_format_datetime = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            iso_format_datetime = None
    else:
        iso_format_datetime = None

    # Match pour l'ID de requête (exemple : 29682)
    id_match = re.search(r'\s+(\d+)\s+INACTIVE', content)
    request_id = id_match.group(1) if id_match else None

    # Match pour le nom de la table (première ligne avec un mot seul après la date)
    table_match = re.search(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.*\n(\w+)', content, re.MULTILINE)
    table_name = table_match.group(1) if table_match else None

    # Match pour l'état (INACTIVE)
    state_match = re.search(r'\b(INACTIVE|ACTIVE)\b', content)
    state = state_match.group(1) if state_match else None

    # Match pour l'adresse SQL de la requête (exemple : 5j067zm8mp28h)
    sql_address_match = re.search(r'INACTIVE\s+(\w+)', content)
    sql_address = sql_address_match.group(1) if sql_address_match else None

    # Match pour l'utilisateur
    user_matches = re.findall(r'^\s*([a-zA-Z0-9_]+)\s*$', content, re.MULTILINE)
    if user_matches and len(user_matches) >= 2:
        user_name = user_matches[1]  # Prend le deuxième utilisateur trouvé
    else:
        user_name = None

    # Résultat final avec date et heure combinées au format ISO 8601
    return {
        "type": "bloquee",
        "datetime": iso_format_datetime,
        "id": request_id,
        "state": state,
        "adress": sql_address,
        "table": table_name,
        "user": user_name
    }

def parse_lost_request(content):
    # Match pour la date et l'heure (deuxième occurrence)
    blocking_date_match = re.search(r'\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\s+\w+\s+(\d{2}/\d{2}/\d{2})\s+(\d{2}:\d{2}:\d{2})', content)
    if blocking_date_match:
        blocking_date = blocking_date_match.group(1)  # Deuxième date
        blocking_time = blocking_date_match.group(2)  # Deuxième heure
        
        # Combiner la date et l'heure, puis convertir au format YYYY-MM-DDTHH:MM:SS
        try:
            combined_datetime = datetime.strptime(f"{blocking_date} {blocking_time}", "%d/%m/%y %H:%M:%S")
            iso_format_datetime = combined_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            iso_format_datetime = None
    else:
        iso_format_datetime = None

    # Match pour l'ID de requête (exemple : 29682)
    id_match = re.search(r'\s+(\d+)\s+INACTIVE', content)
    request_id = id_match.group(1) if id_match else None

    # Match pour le nom de la table
    table_match = re.search(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.*\n(\w+)', content, re.MULTILINE)
    table_name = table_match.group(1) if table_match else None

    # Match pour l'état (INACTIVE)
    state_match = re.search(r'\b(INACTIVE|ACTIVE)\b', content)
    state = state_match.group(1) if state_match else None

    # Match pour l'adresse SQL de la requête (exemple : 5j067zm8mp28h)
    sql_address_match = re.search(r'INACTIVE\s+(\w+)', content)
    sql_address = sql_address_match.group(1) if sql_address_match else None

    # Match pour l'utilisateur concerné (premier utilisateur trouvé)
    user_matches = re.findall(r'^\s*([a-zA-Z0-9_]+)\s*$', content, re.MULTILINE)
    if user_matches:
        user_name = user_matches[0]  # Prend le premier utilisateur trouvé
    else:
        user_name = None

    return {
        "type": "perdue",
        "datetime": iso_format_datetime,
        "heure": blocking_time,
        "id": request_id,
        "state": state,
        "address": sql_address,
        "table": table_name,
        "user": user_name
    }



def parse_log(file_path):
    logs = []
    
    # Regex for identifying the start of a block with a date
    date_regex = re.compile(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}')
    
    # Use the correct encoding to read the file
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        current_block = []
        
        for i, line in enumerate(lines):

            if "ligne créée" in line:
                logs.append({"type": "ligne_creee"})

            if date_regex.match(line):
                if current_block:
                    block_content = "\n".join(current_block)

                    # Vérifie si le bloc est une requête bloquée ou perdue
                    if "BLOQUE" in block_content:
                        parsed_data = parse_blocked_request(block_content)
                    # elif "INACTIVE" in block_content:
                    #     parsed_data = parse_lost_request(block_content)
                    else:
                        parsed_data = None
                    

                    if parsed_data:
                        logs.append(parsed_data)

                current_block = [line.strip()]
            else:
                current_block.append(line.strip())

    return logs

# Usage
log_file = "GCE_10-30-02_17_07-10-2024.txt"
parsed_logs = parse_log(log_file)

# pd.set_option('display.max_columns', None)

# print(dh.createTableBlockedRequest(parsed_logs))

# df = pd.DataFrame(parsed_logs)
# df.drop_duplicates(inplace=True)
# df.reset_index(drop=True, inplace=True)
#
# print(df[['datetime','table','user' ,'id','adress',]])
#
#
# df.to_csv('requete.csv', index=False)

# with open('requêtes.json', 'w') as json_file:
#     json.dump(parsed_logs, json_file, indent=4)

# print("Les données ont été écrites dans 'requêtes.csv'.")