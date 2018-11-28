import pandas as pd


def md_table(df: pd.DataFrame) -> str:
    """
    Returns
    -------
    md :
        Markdown table
    """
    # noinspection PyUnusedLocal
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    return df_formatted.to_csv(sep='|', index=False)


def md_header(df: pd.DataFrame) -> str:
    """
    Returns
    -------
    md :
        Markdown table header + empty row
    """
    md = md_table(df.iloc[[0]]).split('\n')
    md[2] = md[1].replace('---', ' ')
    return '\n'.join(md)
