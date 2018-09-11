import pandas as pd
from dateutil.parser import parse


def col_str(column):
    if not isinstance(column, pd.Series):
        raise TypeError('type error')
    if column.str.startswith('=').get(0):
        coloumn = column.str.split('"').map(lambda s: s[1])
        return coloumn


def col_format(col, col_replace):
    scol = col_str(col)
    index = scol.loc[col.str.contains('——')].index
    if not index.empty:
        for i in index:
            col[i] = col_replace.get(i)
        return col


def col_timestamp(column):
    if not isinstance(column, pd.Series):
        raise TypeError('type error')
    column = col_str(column).map(lambda x: pd.to_datetime(x))
    return column

# d=parse('2018-08-09')
# print(d.day)


def col_date(timestamp_col, date):
    index = []
    for i, day in timestamp_col.map(lambda x: x.day).items():
        if day > parse(date).day:
            index.append(i)
    return index


def col_map(value):
    if value == '——':
        return value
    if value.startswith('='):
        return value.split('"')[1]
