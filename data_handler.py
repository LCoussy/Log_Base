import pandas as pd

def createTableBlockedRequest(data):
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(data)

    # remove all duplicate
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True) # reset all index
    if df.empty:
        return None
    if  not (df.columns.__contains__("date")):
        return None
    return df[['date','table','utilisateur' ,'id','adresse',]]


# not implemented yet
def createCsvBlockedRequest(dataFrame):
    dataFrame.to_csv('data.csv', index=False)