import pandas as pd

def createTableBlockedRequest(data):
    """
    Creates a pandas DataFrame for blocked requests based on provided data.

    This function converts the provided data into a pandas DataFrame, removes any duplicate 
    rows, and resets the index. If the DataFrame is empty or does not contain a 'date' column, 
    it returns None. Otherwise, it returns a DataFrame with selected columns.

    Args:
        data (list of dict): A list of dictionaries where each dictionary contains information
                             about a blocked request.

    Returns:
        pd.DataFrame or None: A DataFrame containing the 'date', 'table', 'utilisateur', 'id',
                              and 'adresse' columns, or None if the DataFrame is empty or 
                              does not contain a 'date' column.
    """

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
    """
    Saves the provided DataFrame to a CSV file.

    This function takes a pandas DataFrame and saves its contents to a CSV file 
    named 'data.csv' without including the index in the output file.

    Args:
        dataFrame (pd.DataFrame): The DataFrame to be written to a CSV file.

    Returns:
        None
    """

    dataFrame.to_csv('data.csv', index=False)