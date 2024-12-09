import os
from datetime import datetime

class FilterFiles:
    """
    FilterFiles is responsible for handling file processing tasks, such as 
    organizing files into a hierarchical structure based on their modification times.
    """

    @staticmethod
    def get_file_date(file_path):
        """
        Get the last modification date of a file.
        
        Args:
            file_path (str): Path to the file.
        
        Returns:
            datetime: The modification date of the file.
        """
        return datetime.fromtimestamp(os.path.getmtime(file_path))

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

        hierarchy = {}

        # Walk through the directory and process files
        for root, _, files in os.walk(directory):
            for file in sorted(files, key=lambda f: os.path.getmtime(os.path.join(root, f)), reverse=True):
                file_path = os.path.join(root, file)
                file_date = self.get_file_date(file_path)

                # Extract hierarchy keys
                year, month, day, hour = (
                    str(file_date.year),
                    file_date.strftime('%B'),
                    str(file_date.day),
                    f"{file_date.hour}:00"
                )

                # Build nested structure
                hierarchy.setdefault(year, {}).setdefault(month, {}).setdefault(day, {}).setdefault(hour, []).append({
                    "file_path": file_path,
                    "formatted_time": file_date.strftime('%H:%M')
                })

        return hierarchy
