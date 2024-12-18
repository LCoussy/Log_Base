def getOnlyLost(data):
    return data.get("LOST", None)  # Return datas with "LOST" type

def getOnlyBlocked(data):
    return data.get("BLOCKED", None)  # Return datas with "BLOCKED" type 

def getOnlyUser(data):
    return data.get("USER", None)  # Return datas with "USER" type 

def getByUser(data, user):
    return data[data['utilisateur'] == user]

def getByTable(data, table):
    return data[data['table'] == table]