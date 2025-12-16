import pandas as pd

def load_dbd_data(path="data/DATA DBD.csv"):
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()

    date_col = df.columns[0]
    case_col = df.columns[1]

    df["time"] = range(len(df))
    df["cases_norm"] = df[case_col] / df[case_col].max()

    return df[["time", "cases_norm"]]
