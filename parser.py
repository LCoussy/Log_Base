import re
import json
from datetime import datetime
import pandas as pd
import data_handler as dh

import re
import json
from datetime import datetime

import re
import json
from datetime import datetime

import re
import json
from datetime import datetime

def parse_request(content, request_type):
    """
    Parse a request from the log content.

    This function extracts key details such as the request date, time, ID, table name,
    state, SQL address, and user name for a request. The data is returned in a dictionary format.

    Args:
        content (str): The content block containing the request information.
        request_type (str): The type of request, either "BLOCKED" or "LOST".
    Returns:
        dict: Parsed information about the request with keys:
            - "type": Type of request, Blocked or Lost.
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
    poste_match = re.search(r'^(?:.*\n){4}(\S+)', content)  # Cherche le premier mot de la 6e ligne
    if poste_match:
        poste = poste_match.group(1)  # Le premier mot de la 6e ligne
    else:
        poste = None


    sql_address_match = re.search(r'\b(INACTIVE|ACTIVE)\s+(\w+)', content)
    sql_address = sql_address_match.group(2) if sql_address_match else None

    # Extraction de l'ID de l'utilisateur dans ce cas particulier où il est sur la ligne contenant "svc_halimede"
    user_match = re.search(r'\n\s*(\w+)\s*$', content)
    user_name = user_match.group(1) if user_match else None

    # Utiliser l'utilisateur trouvé pour l'ID si ce n'est pas déjà défini
    if not request_id and user_name:
        request_id = user_name  # Utiliser le nom d'utilisateur comme ID dans ce cas

    # Extraction du nom de la table
    table_match = re.search(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.*\n(\w+)', content, re.MULTILINE)
    table_name = table_match.group(1) if table_match else None

    return {
        "type": "bloquee" if request_type == "BLOCKED" else "LOST",
        "date": iso_format_datetime,
        "id": request_id,
        "state": state,
        "adresse": sql_address,
        "table": table_name,
        "utilisateur": user_name,
        "poste": poste
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
                        parsed_data = parse_request(block_content, "BLOCKED")
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
                parsed_data = parse_request(block_content, "BLOCKED")
                if parsed_data:
                    logs.append(parsed_data)

    return logs
