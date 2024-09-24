import pandas as pd

def extract_tables_from_csv(file):
    df = pd.read_csv(file)
    non_null_counts = df.notna().sum(axis=1)
    total_columns = df.shape[1]
    non_null_percentage = (non_null_counts / total_columns) * 100
    rows_to_extract = df[non_null_percentage > 70]

    if rows_to_extract.empty:
        return pd.DataFrame()

    rows_to_extract.columns = rows_to_extract.iloc[0]
    rows_to_extract = rows_to_extract[1:]

    rows_to_extract.columns = [
        f"Unnamed{i+1}" if pd.isna(col) else col
        for i, col in enumerate(rows_to_extract.columns)
    ]

    columns = pd.Series(rows_to_extract.columns)
    for dup in columns[columns.duplicated()].unique():
        columns[columns[columns == dup].index.values.tolist()] = [
            f"{dup}_{i+1}" if i != 0 else dup
            for i in range(sum(columns == dup))
        ]
    rows_to_extract.columns = columns

    package_type_cols = ['CTNS', 'QTN', 'QTY/CTN', 'Pallet', 'Boxes', 'Euro Pallet', 'Bags', 'Cases']
    if any(col in rows_to_extract.columns and rows_to_extract[col].notna().any() for col in package_type_cols):
        rows_to_extract['Package Type'] = rows_to_extract.apply(
            lambda row: next((col for col in package_type_cols if col in rows_to_extract.columns and pd.notna(row[col])), None), axis=1
        )
        rows_to_extract = rows_to_extract.drop(columns=[col for col in package_type_cols if col in rows_to_extract.columns])

    return rows_to_extract

def convert_to_json_hierarchy(dataframe):
    return dataframe.to_json(orient='records', indent=2)

def convert_json_to_dataframe(json_data):
    return pd.read_json(json_data)
