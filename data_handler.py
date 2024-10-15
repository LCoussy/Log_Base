import pandas as pd

def createTableBlockedRequest(data):
    # pd.set_option('display.max_columns', None)
    df = pd.DataFrame(data)

    # remove all duplicate
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True) # reset all index
    if df.empty:
        return None
    return df[['datetime','table','user' ,'id','adress',]]


# not implemented yet
def createCsvBlockedRequest(dataFrame):
    dataFrame.to_csv('data.csv', index=False)
    print('Data saved to data.csv')