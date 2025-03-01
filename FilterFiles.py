import os
from datetime import datetime
import re
class FilterFiles:
    def __init__(self):
        self.pattern_filename = re.compile(r"GCE_([_1]\d|2[0-3])-([0-5]\d)-([0-5]\d)_\d{2}_(0[1-9]|1\d|2[0-8]|29(?=-\d\d-(?!1[01345789]00|2[1235679]00)\d\d(?:[02468][048]|[13579][26]))|30(?!-02)|31(?=-0[13578]|-1[02]))-(0[1-9]|1[0-2])-([12]\d{3})+")
    """
    FilterFiles is responsible for handling file processing tasks, such as
    organizing files into a hierarchical structure based on their modification times.
    """

    def get_month(self, monthNumber):
        """
        Get the month name based on the month number.

        Args:
            monthNumber (int): The month number (1-12).

        Returns:
            str: The month name.
        """
        months = [
            "Janvier",
            "Février",
            "Mars",
            "Avril",
            "Mai",
            "Juin",
            "Juillet",
            "Août",
            "Septembre",
            "Octobre",
            "Novembre",
            "Décembre",
        ]
        return months[monthNumber - 1]

    def convert_datetime(self, datestr):
        """
        Convert a string date to a datetime object.

        Args:
            datestr (str): The date string in the format 'YYYY-MM-DD HH:MM:SS'.

        Returns:
            datetime: The datetime object representing the input date.
        """
        datestr_good = datestr.group(6)+"-"+datestr.group(5)+"-"+datestr.group(4)+" "+datestr.group(1).replace("_","0")+":"+datestr.group(2)+":"+datestr.group(3)
        return datetime.strptime(datestr_good, "%Y-%m-%d %H:%M:%S")

    def organize_files_by_date(self, directory):
        """
        Organize files in the given directory by year, month, day, and hour.

        Args:
            directory (str): Path to the directory containing log files.

        Returns:
            dict: Nested dictionary organizing files by year, month, day, and hour.
        """
        if not os.path.exists(directory):
            return {}

        pattern_filename = re.compile(r"GCE_([_1]\d|2[0-3])-([0-5]\d)-([0-5]\d)_\d{2}_(0[1-9]|1\d|2[0-8]|29(?=-\d\d-(?!1[01345789]00|2[1235679]00)\d\d(?:[02468][048]|[13579][26]))|30(?!-02)|31(?=-0[13578]|-1[02]))-(0[1-9]|1[0-2])-([12]\d{3})+")
        hierarchy = {}

        for root, dir, files in os.walk(directory):
            for file in sorted(files, key=lambda f: self.convert_datetime(re.search(pattern_filename, os.path.join(root, f))) if re.search(pattern_filename, os.path.join(root, f)) else datetime.min, reverse=True):
                file_path = os.path.join(root, file)
                pat = re.search(pattern_filename, file_path)
                if pat:
                    year, month, day, hour = (
                        pat.group(6),
                        self.get_month(int(pat.group(5))),
                        pat.group(4),
                        f"{pat.group(1).replace('_', '0')}:00"
                    )
                    hierarchy.setdefault(year, {}).setdefault(month, {}).setdefault(day, {}).setdefault(hour, []).append({
                        "file_path": file_path,
                        "formatted_time": f"{pat.group(1).replace('_','0')}:{pat.group(2)}"
                    })
        return hierarchy
    def get_logs_in_date_range(self, directory, start_date, end_date):
        """
        Récupère les fichiers logs qui sont dans la plage de dates spécifiée.

        Args:
            directory (str): Le répertoire contenant les fichiers logs.
            start_date (datetime): Date de début.
            end_date (datetime): Date de fin.

        Returns:
            list: Liste des fichiers logs correspondant à la plage de dates.
        """
        logs = []
        if not os.path.exists(directory):
            return logs

        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                pat = re.search(self.pattern_filename, file_path)
                if pat:
                    file_date = datetime.strptime(f"{pat.group(6)}-{pat.group(5)}-{pat.group(4)}", "%Y-%m-%d")
                    if start_date <= file_date <= end_date:
                        logs.append(file_path)

        return logs