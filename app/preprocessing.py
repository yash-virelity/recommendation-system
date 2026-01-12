import ast

def parse_list_columns(df, columns):
    for col in columns:
        df[col] = df[col].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else []
        )
    return df
