from functools import reduce, partial
from typing import Callable

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from ta import volume, volatility, trend
from scipy.signal import argrelextrema, savgol_filter

from config import *


class DataSchema:
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"
    VOLUME = "Volume"
    VWAP = "vwap"
    LAG = "lag"
    VWAP_LOCAL = "vwap_local"
    RETS = "returns"


class IndexSchema:
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"
    SCLOSE = "sclose"
    LOCAL = "local"


Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


def create_vwap(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.VWAP] = volume.volume_weighted_average_price(df[DataSchema.HIGH],
                                                               df[DataSchema.LOW],
                                                               df[DataSchema.CLOSE],
                                                               df[DataSchema.VOLUME], 15)
    return df


def create_smooth_vwap(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.LAG] = trend.ema_indicator(df[DataSchema.VWAP], 9)
    return df


def create_local_minimax(df: pd.DataFrame, field: str, name: str) -> pd.DataFrame:
    mini_max_arr = np.zeros(len(df))
    maximas = argrelextrema(df[field].values, np.greater)[0]
    minimas = argrelextrema(df[field].values, np.less)[0]
    mini_max_arr[maximas] = 1
    mini_max_arr[minimas] = -1
    df[name] = mini_max_arr
    return df


def create_returns(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.RETS] = (df[DataSchema.CLOSE] / df[DataSchema.OPEN]) - 1.
    return df


def create_index_smoother(df: pd.DataFrame) -> pd.DataFrame:
    df[IndexSchema.SCLOSE] = savgol_filter(df[IndexSchema.CLOSE].values,
                                           index_looback // 4, 3)
    return df


def compose_fns(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def load_tickers() -> dict:
    data = dict()
    preprocessor = compose_fns(create_vwap,
                               create_smooth_vwap,
                               partial(create_local_minimax, field=DataSchema.LAG, name=DataSchema.VWAP_LOCAL),
                               create_returns)
    for tkr in tickers:
        df = yf.download([tkr], start=datetime.utcnow() - timedelta(lookback), progress=False)
        data[tkr] = preprocessor(df)
        # data[tkr] = yf.download([tkr], start=datetime.utcnow() - timedelta(lookback), progress=False)
        # data[tkr][DataSchema.VWAP] = volume.volume_weighted_average_price(data[tkr][DataSchema.HIGH],
        #                                                                   data[tkr][DataSchema.LOW],
        #                                                                   data[tkr][DataSchema.CLOSE],
        #                                                                   data[tkr][DataSchema.VOLUME], 15)
        # data[tkr][DataSchema.LAG] = trend.ema_indicator(data[tkr][DataSchema.VWAP], 9)
        # mini_max_arr = np.zeros(len(data[tkr]))
        # maximas = argrelextrema(data[tkr][DataSchema.LAG].values, np.greater)[0]
        # minimas = argrelextrema(data[tkr][DataSchema.LAG].values, np.less)[0]
        # mini_max_arr[maximas] = 1
        # mini_max_arr[minimas] = -1
        # data[tkr][DataSchema.VWAP_LOCAL] = mini_max_arr
        # data[tkr][DataSchema.RETS] = (data[tkr][DataSchema.CLOSE] / data[tkr][DataSchema.OPEN]) - 1.

    return data


def load_indices() -> dict:
    data = dict()
    preprocessor = compose_fns(create_index_smoother,
                               partial(create_local_minimax, field=IndexSchema.SCLOSE, name=IndexSchema.LOCAL))
    for tkr, tkr_name in zip(indices, index_mapping):
        df = yf.download([tkr], start=datetime.utcnow() - timedelta(index_looback), progress=False)
        data[tkr_name] = preprocessor(df)
        # data[tkr_name] = yf.download([tkr], start=datetime.utcnow() - timedelta(index_looback), progress=False)
        # data[tkr_name][IndexSchema.SCLOSE] = savgol_filter(data[tkr_name][IndexSchema.CLOSE].values,
        #                                                    index_looback // 4, 3)
        # mini_max_arr = np.zeros(len(data[tkr_name]))
        # maximas = argrelextrema(data[tkr_name][IndexSchema.SCLOSE].values, np.greater)[0]
        # minimas = argrelextrema(data[tkr_name][IndexSchema.SCLOSE].values, np.less)[0]
        # mini_max_arr[maximas] = 1
        # mini_max_arr[minimas] = -1
        # data[tkr_name][IndexSchema.LOCAL] = mini_max_arr
    return data
