import os
import batchOpen as bo

def validate_directory(path):
    """
    Valide si le chemin est un dossier valide.

    Args:
        path (str): Chemin à valider.

    Returns:
        bool: True si le chemin est un dossier valide, sinon False.
    """
    return os.path.isdir(path)

def process_directory(path):
    """
    Traite le dossier sélectionné en appelant la fonction batchOpen.

    Args:
        path (str): Chemin du dossier à traiter.
    """
    try:
        bo.batchOpen(path)
    except Exception as e:
        print(f"Erreur lors du traitement du dossier {path} : {e}")