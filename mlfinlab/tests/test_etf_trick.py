"""
Tests the financial data structures
"""

import unittest
import os
import numpy as np
import pandas as pd

from mlfinlab.multi_product.etf_trick import ETFTrick


class TestETFTrick(unittest.TestCase):
    """
    Test the various financial data structures:
    1. Dollar bars
    2. Volume bars
    3. Tick bars
    """

    def setUp(self):
        """
        Set the file path for the tick data csv
        """
        project_path = os.path.dirname(__file__)
        self.path = project_path + '/test_data'

        self.open_df_path = '{}/open_df.csv'.format(self.path)
        self.close_df_path = '{}/close_df.csv'.format(self.path)
        self.alloc_df_path = '{}/alloc_df.csv'.format(self.path)
        self.costs_df_path = '{}/costs_df.csv'.format(self.path)
        self.rates_df_path = '{}/rates_df.csv'.format(self.path)

        self.open_df = pd.read_csv(self.open_df_path, index_col=0, parse_dates=[0])
        self.close_df = pd.read_csv(self.close_df_path, index_col=0, parse_dates=[0])
        self.alloc_df = pd.read_csv(self.alloc_df_path, index_col=0, parse_dates=[0])
        self.costs_df = pd.read_csv(self.costs_df_path, index_col=0, parse_dates=[0])
        self.rates_df = pd.read_csv(self.rates_df_path, index_col=0, parse_dates=[0])

    def test_etf_trick_costs_defined(self):
        """
        Tests in-memory and csv ETF trick implementation, when costs_df is defined
        """

        csv_etf_trick = ETFTrick(self.open_df_path, self.close_df_path, self.alloc_df_path, self.costs_df_path,
                                 self.rates_df_path)
        in_memory_etf_trick = ETFTrick(self.open_df, self.close_df, self.alloc_df, self.costs_df, self.rates_df)
        in_memory_trick_series = in_memory_etf_trick.get_etf_series()
        csv_trick_series_4 = csv_etf_trick.get_etf_series(batch_size=4)
        csv_etf_trick.reset()
        csv_trick_series_100 = csv_etf_trick.get_etf_series(batch_size=100)
        csv_etf_trick.reset()
        csv_trick_series_all = csv_etf_trick.get_etf_series(batch_size=1e6)

        self.assertTrue(in_memory_trick_series.shape == csv_trick_series_4.shape)
        self.assertTrue(in_memory_trick_series.shape == csv_trick_series_100.shape)
        self.assertTrue(in_memory_trick_series.shape == csv_trick_series_all.shape)

        # value check
        self.assertTrue(abs(in_memory_trick_series.iloc[20] - 0.9933502) < 1e-6)

        # assert the first value equal to 1
        self.assertTrue(in_memory_trick_series.iloc[0] == 1.0)
        self.assertTrue(csv_trick_series_4.iloc[0] == 1.0)
        self.assertTrue(csv_trick_series_100.iloc[0] == 1.0)
        self.assertTrue(csv_trick_series_all.iloc[0] == 1.0)

        # assert the last values are equal
        self.assertTrue(in_memory_trick_series.iloc[-1] == csv_trick_series_4.iloc[-1])
        self.assertTrue(in_memory_trick_series.iloc[-1] == csv_trick_series_100.iloc[-1])
        self.assertTrue(in_memory_trick_series.iloc[-1] == csv_trick_series_all.iloc[-1])

        # Assert same values
        self.assertTrue(np.all(in_memory_trick_series.values == csv_trick_series_4.values))
        self.assertTrue(np.all(in_memory_trick_series.values == csv_trick_series_100.values))
        self.assertTrue(np.all(in_memory_trick_series.values == csv_trick_series_all.values))

    def test_etf_trick_rates_not_defined(self):
        """
        Tests in-memory and csv ETF trick implementation, when costs_df is not defined (should be set trivial)
        """

        csv_etf_trick = ETFTrick(self.open_df_path, self.close_df_path, self.alloc_df_path, self.costs_df_path, None)
        in_memory_etf_trick = ETFTrick(self.open_df, self.close_df, self.alloc_df, self.costs_df, None)
        in_memory_trick_series = in_memory_etf_trick.get_etf_series()
        csv_trick_series_4 = csv_etf_trick.get_etf_series(batch_size=4)
        csv_etf_trick.reset()
        csv_trick_series_100 = csv_etf_trick.get_etf_series(batch_size=100)
        csv_etf_trick.reset()
        csv_trick_series_all = csv_etf_trick.get_etf_series(batch_size=1e6)

        self.assertTrue(in_memory_trick_series.shape == csv_trick_series_4.shape)
        self.assertTrue(in_memory_trick_series.shape == csv_trick_series_100.shape)
        self.assertTrue(in_memory_trick_series.shape == csv_trick_series_all.shape)

        # value check
        self.assertTrue(abs(in_memory_trick_series.iloc[20] - 0.9933372) < 1e-6)

        # assert the first value equal to 1
        self.assertTrue(in_memory_trick_series.iloc[0] == 1)
        self.assertTrue(csv_trick_series_4.iloc[0] == 1)
        self.assertTrue(csv_trick_series_100.iloc[0] == 1)
        self.assertTrue(csv_trick_series_all.iloc[0] == 1)

        # assert the last values are equal
        self.assertTrue(in_memory_trick_series.iloc[-1] == csv_trick_series_4.iloc[-1])
        self.assertTrue(in_memory_trick_series.iloc[-1] == csv_trick_series_100.iloc[-1])
        self.assertTrue(in_memory_trick_series.iloc[-1] == csv_trick_series_all.iloc[-1])

        # Assert same values
        self.assertTrue(np.all(in_memory_trick_series.values == csv_trick_series_4.values))
        self.assertTrue(np.all(in_memory_trick_series.values == csv_trick_series_100.values))
        self.assertTrue(np.all(in_memory_trick_series.values == csv_trick_series_all.values))
