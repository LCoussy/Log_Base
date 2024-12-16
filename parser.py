import re
from datetime import datetime
import uuid
def convert_seconds_to_dhm(seconds):
    """
    Converts a duration in seconds into a readable format: days, hours, minutes.

    Args:
        seconds (float): The number of seconds to convert.

    Returns:
        str: A formatted string representing the duration in days, hours, minutes.
    """
    days = seconds // (24 * 3600) -177
    hours = (seconds % (24 * 3600)) // 3600
    minutes = (seconds % 3600) // 60
    if days >= 1:
        return f"{int(days)} jours, {int(hours)} heures, {int(minutes)} minutes"
    else:
        if hours >= 1:
            return f"{int(hours)} heures, {int(minutes)} minutes"
        else:
            return f"{int(minutes)} minutes"

def get_log_segment(file_path, request_id):
    """
    Retrieve the log segment corresponding to a specific request ID.

    Args:
        file_path (str): The path to the log file.
        request_id (str): The request ID to search for.

    Returns:
        str: The segment of the log containing the specified request ID, or None if not found.
    """
    date_regex = re.compile(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}')

    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        current_block = []
        matching_block = None

        for line in lines:
            if date_regex.match(line):
                # Start a new block
                if current_block:
                    block_content = "\n".join(current_block)
                    if f" {request_id} " in block_content:
                        matching_block = block_content
                        break
                current_block = [line.strip()]
            else:
                current_block.append(line.strip())

        # Check the last block
        if not matching_block and current_block:
            block_content = "\n".join(current_block)
            if f" {request_id} " in block_content:
                matching_block = block_content

        return matching_block

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
            - "date2": Second date found, formatted to 'YYYY-MM-DD HH:MM:SS'.
            - "id": Request ID (str) or None.
            - "state": Request state ('INACTIVE' or 'ACTIVE') or None.
            - "adresse": SQL address (str) or None.
            - "table": Name of the table involved (str) or None.
            - "utilisateur": User name associated with the request or None.
            - "poste": User's machine name associated with the request or None.
    """
    
    # Match pour la première date et heure
    first_date_match = re.search(r'(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', content)
    first_date = None
    if first_date_match:
        try:
            first_date = datetime.strptime(first_date_match.group(1), "%d/%m/%y %H:%M:%S")
        except ValueError:
            pass

    # Match pour la date 2 (BLOQUE)
    second_date_match = re.search(r'BLOQUE (\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', content)
    second_date = None
    if second_date_match:
        try:
            second_date = datetime.strptime(second_date_match.group(1), "%d/%m/%y %H:%M:%S")
        except ValueError:
            pass

    # Extraction de l'état (ACTIVE ou INACTIVE)
    state_match = re.search(r'\b(ACTIVE|INACTIVE)\b', content)
    state = state_match.group(1) if state_match else None

    # Extraction de l'ID de la requête
    request_id_match = re.search(r'\s+(\d+)\s+(ACTIVE|INACTIVE)', content)
    request_id = request_id_match.group(1) if request_id_match else None

    # Extraction de l'adresse SQL
    sql_address_match = re.search(r'\b(INACTIVE|ACTIVE)\s+(\w+)', content)
    sql_address = sql_address_match.group(2) if sql_address_match else None

    # Extraction du nom de l'utilisateur
    user_match = re.search(r'\n\s*(\w+)\s*$', content)
    user_name = user_match.group(1) if user_match else None

    # Extraction du nom de la table
    table_match = re.search(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}.*\n(\w+)', content, re.MULTILINE)
    table_name = table_match.group(1) if table_match else None

    # Extraction du poste de l'utilisateur
    poste_match = re.search(r'^(?:.*\n){4}(\S+)', content)
    poste = poste_match.group(1) if poste_match else None

    # Formatage de la date en ISO si elle existe
    formatted_first_date = first_date.strftime("%Y-%m-%d %H:%M:%S") if first_date else None
    formatted_second_date = second_date.strftime("%Y-%m-%d %H:%M:%S") if second_date else None

    return {
        "type": "bloquee" if request_type == "BLOCKED" else "LOST",
        "date": formatted_first_date,
        "date2": formatted_second_date,
        "id": request_id,
        "state": state,
        "adresse": sql_address,
        "table": table_name,
        "utilisateur": user_name,
        "poste": poste
    }

def update_logs_with_duration(logs):
    """
    Update logs with correct blocking duration and remove duplicates by keeping only the most recent entry.

    Args:
        logs (list): The list of logs to update with the correct blocking durations.

    Returns:
        list: Updated logs with correct durations and duplicates removed.
    """
    requests = {}

    for log in logs:
        request_id = log["id"]
        first_date = log["date"]
        second_date = log["date2"]


        if request_id not in requests or first_date > requests[request_id]["last_appearance"]:
            requests[request_id] = {
                "last_appearance": first_date,
                "start_blocking": second_date
            }
        else:
            if first_date > requests[request_id]["last_appearance"]:
                requests[request_id]["last_appearance"] = first_date
            if not requests[request_id]["start_blocking"]:
                requests[request_id]["start_blocking"] = second_date

    for log in logs:
        request_id = log["id"]
        if request_id in requests:
            last_appearance = datetime.strptime(requests[request_id]["last_appearance"], "%Y-%m-%d %H:%M:%S")
            start_blocking = datetime.strptime(requests[request_id]["start_blocking"], "%Y-%m-%d %H:%M:%S")
            duration = (last_appearance - start_blocking).total_seconds()
            log["duree"] = convert_seconds_to_dhm(duration)

    return logs


def parse_log(file_path):
    """
    Parse a single log file and extract data from each log block.

    Args:
        file_path (str): The path to the log file to be parsed.

    Returns:
        list: A list of dictionaries, where each dictionary contains details of either a blocked or lost request,
              including a unique ID and the raw segment content.
    """
    logs = []
    date_regex = re.compile(r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}')
    segment_id_counter = 0

    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        lines = file.readlines()
        current_block = []

        for line in lines:
            if date_regex.match(line):
                if current_block:
                    block_content = "\n".join(current_block)
                    if "BLOQUE" in block_content:
                        parsed_data = parse_request(block_content, "BLOCKED")
                        segment_id = str(uuid.uuid4()) 
                        parsed_data["segment_id"] = segment_id
                        parsed_data["raw_content"] = block_content
                        logs.append(parsed_data)
                current_block = [line.strip()]
            else:
                current_block.append(line.strip())

        if current_block:
            block_content = "\n".join(current_block)
            if "BLOQUE" in block_content:
                parsed_data = parse_request(block_content, "BLOCKED")
                segment_id = str(uuid.uuid4()) 
                parsed_data["segment_id"] = segment_id
                parsed_data["raw_content"] = block_content
                logs.append(parsed_data)

    logs = update_logs_with_duration(logs)

    return logs

def get_segment_by_id(logs, segment_id):
    """
    Retrieve the raw content of a log segment by its unique ID.

    Args:
        logs (list): List of parsed logs containing segment IDs and raw content.
        segment_id (str): The unique ID of the segment to retrieve.

    Returns:
        str: The raw content of the log segment or a message if not found.
    """
    for log in logs:
        if log.get("segment_id") == segment_id:
            return log.get("raw_content", f"Segment pour l'ID {segment_id} introuvable.")
    return f"Segment pour l'ID {segment_id} introuvable."