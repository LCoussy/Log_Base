


def getOnlyLost(data):
    return data.get("LOST", None)  # Retourne les données associées à la clé "LOST"

def getOnlyBlocked(data):
    return data.get("BLOCKED", None)  # Retourne les données associées à la clé "BLOCKED"

def getOnlyUser(data):
    return data.get("USER", None)  # Retourne les données associées à la clé "USER"

def getByUser(data, user):
    return data[data['utilisateur'] == user]

def getByTable(data, table):
    return data[data['table'] == table]