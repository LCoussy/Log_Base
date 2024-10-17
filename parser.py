import re
import json
from datetime import datetime
import pandas as pd
import data_handler as dh

def parse_blocked_request(content):
    """
    Parse a blocked request from the log content.

    This function extracts key details such as the request date, time, ID, table name, 
    state, SQL address, and user name for a blocked request. The data is returned in a dictionary format.

    Args:
        content (str): The content block containing the blocked request information.

    Returns:
        dict: Parsed information about the blocked request with keys:
            - "type": Type of request, always 'bloquee' for blocked requests.
            - "date": Combined date and time in 'YYYY-MM-DD HH:MM:SS' format or None if not found.
            - "id": Request ID (str) or None.
            - "state": Request state ('INACTIVE' or 'ACTIVE') or None.
            - "adresse": SQL address (str) or None.
            - "table": Name of the table involved (str) or None.
            - "utilisateur": User name associated with the request or None.
    """

    # Match pour la date et l'heure (deuxième occurrence)
    blocking_date_match = re.search(r'\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\s+\w+\s+(\d{2}/\d{2}/\d{2})\s+(\d{2}:\d{2}:\d{2})', content)
    if blocking_date_match:
        blocking_date = blocking_date_match.group(1)  # Deuxième date
        blocking_time = blocking_date_match.group(2)  # Deuxième heure

        # Combiner la date et l'heure, puis convertir au format YYYY-MM-DDTHH:MM:SS
        try:
            combined_datetime = datetime.strptime(f"{blocking_date} {blocking_time}", "%m/%d/%y %H:%M:%S")
            iso_format_datetime = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            iso_format_datetime = None
    else:
        iso_format_datetime = None

    # Extraction de l'état (ACTIVE ou INACTIVE)
    state_match = re.search(r'\b(ACTIVE|INACTIVE)\b', content)
    state = state_match.group(1) if state_match else None

    # Extraction des autres informations
    id_match = re.search(r'\s+(\d+)\s+(ACTIVE|INACTIVE)', content)
    request_id = id_match.group(1) if id_match else None

    sql_address_match = re.search(r'\b(INACTIVE|ACTIVE)\s+(\w+)', content)
    sql_address = sql_address_match.group(2) if sql_address_match else None

    table_match = re.search(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.*\n(\w+)', content, re.MULTILINE)
    table_name = table_match.group(1) if table_match else None

    user_matches = re.findall(r'^\s*([a-zA-Z0-9_]+)\s*$', content, re.MULTILINE)
    user_name = user_matches[1] if len(user_matches) >= 2 else None

    return {
        "type": "bloquee",
        "date": iso_format_datetime,
        "id": request_id,
        "state": state,
        "adresse": sql_address,
        "table": table_name,
        "utilisateur": user_name
    }

def parse_lost_request(content):
    """
    Parse a lost request from the log content.

    Similar to the blocked request parsing, this function extracts the date, time, ID, 
    table name, state, SQL address, and user for a lost request.

    Args:
        content (str): The content block containing the lost request information.

    Returns:
        dict: Parsed information about the lost request with keys:
            - "type": Type of request, always 'perdue' for lost requests.
            - "Date": Date of the request in 'YYYY-MM-DD' format or None.
            - "heure": Time of the request or None.
            - "id": Request ID (str) or None.
            - "state": Request state ('INACTIVE' or 'ACTIVE') or None.
            - "address": SQL address (str) or None.
            - "table": Name of the table involved (str) or None.
            - "user": User name associated with the request or None.
    """

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
        "Date": iso_format_datetime,
        "heure": blocking_time,
        "id": request_id,
        "state": state,
        "address": sql_address,
        "table": table_name,
        "user": user_name
    }



def parse_log(file_path):
    """
    Parse the log file and extract data from each log block.

    The log file is expected to contain different types of requests (blocked or lost).
    Each block in the log is processed, and if it's identified as blocked or lost, its details are parsed and added to a list.

    Args:
        file_path (str): The path to the log file to be parsed.

    Returns:
        list: A list of dictionaries, where each dictionary contains details of either a blocked or lost request.
    """

    logs = []

    # Regex for identifying the start of a block with a date
    date_regex = re.compile(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}')

    # Use the correct encoding to read the file
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        current_block = []

        for i, line in enumerate(lines):
            if date_regex.match(line):
                if current_block:
                    block_content = "\n".join(current_block)

                    # Vérifie si le bloc est une requête bloquée ou perdue
                    if "BLOQUE" in block_content:
                        parsed_data = parse_blocked_request(block_content)
                    else:
                        parsed_data = None

                    if parsed_data:
                        logs.append(parsed_data)

                current_block = [line.strip()]
            else:
                current_block.append(line.strip())

        if current_block:
            block_content = "\n".join(current_block)
            if "BLOQUE" in block_content:
                parsed_data = parse_blocked_request(block_content)
                if parsed_data:
                    logs.append(parsed_data)

    return logs
