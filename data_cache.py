import pandas as pd
import datetime

default_case_type = "confirmed"


class DataCache:
    dct = {}

    def dct_for_case_type(self, case_type=default_case_type):
        """
        Returns the cached version of data for the case_type and the timestamp for when it was last refreshed
        Fetches the data from Johns Hopkins github if no data in cache
        :param case_type: should be one of confirmed, recovered, deaths
        :return: {"df": dataframe of data, "ts": timestamp when last fetched}"""
        if case_type not in self.dct:
            url_raw_github = "https://raw.githubusercontent.com"
            repo = "CSSEGISandData/COVID-19"
            branch = "master"
            folder = "csse_covid_19_data/csse_covid_19_time_series"
            filename = f"time_series_covid19_{case_type}_global.csv"
            url_csv = f"{url_raw_github}/{repo}/{branch}/{folder}/{filename}"
            self.dct[case_type] = {"df": pd.read_csv(url_csv), "ts": datetime.datetime.now()}
        return self.dct[case_type]

    def df_for_case_type(self, case_type=default_case_type):
        """
        Returns just the cached version of data for the case_type
        :param case_type: should be one of confirmed, recovered, deaths
        :return: pandas dataframe"""
        return self.dct_for_case_type(case_type)["df"]

    def ts_for_case_type(self, case_type=default_case_type):
        """
        Returns the timestamp when the cached data was last refreshed for the given case_type
        :param case_type: should be one of confirmed, recovered, deaths
        :return: timestamp as a datetime object
        """
        return self.dct_for_case_type(case_type)["ts"]

    def refresh_data(self):
        """clear the cache"""
        self.dct = {}

    def df_for_location(self, case_type=default_case_type, country=None, state=None):
        """return the dataframe filtered by country, by state or by country and state"""
        df = self.df_for_case_type(case_type=case_type)
        filt = [True] * df.shape[0]
        if country:
            filt = filt & (df["Country/Region"] == country)
        if state:
            filt = filt & (df["Province/State"] == state)
        return df[filt]

    def series_sum_for_location(self, case_type=default_case_type, country=None, state=None):
        """returns a series of values totalled for a given df and country and/or state
        Index for returned series is a DateTimeIndex"""
        df = self.df_for_location(case_type=case_type, state=state, country=country)
        series = df.sum(axis="index")[4:].astype(int)
        series.index = pd.to_datetime(series.index)
        return series
