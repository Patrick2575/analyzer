import os
import grequests

class ExchangeInfo:
    def __init__(self, url = f"{os.getenv('base_url')}{os.getenv('exchange_info_path')}"):
        self.m_url = url
        self.m_symbols = []
        self.m_tradable_symbols = []
        self.m_tradable_quote_assets = []
        self.m_tradable_symbols_map = {} # key quote_assets, value : list of symbols
        self.m_no_tradable_symbols = []
        self.m_data_loaded = False   

    def symbol_names(self):
        """
            returns a list of symbol names that are tradable on Binance exchange
            Example of symbols : BTCUSDT, LTCUSDT, ETHUSDT ...
        """
        if not self.m_data_loaded:
            self._load_data()
        
        names = [symbol['symbol'] for symbol in self.m_tradable_symbols]
        return names

    #------------------------------------------------------------------------------------
    #
    #------------------------------------------------------------------------------------
    def quote_assets(self):
        """
            retuns quote assets names that are currently used in trading on binance
            Example of quote asset: USTD, BUSD, USDC, EUR,USDC, BTC, ETH  ...
        """
        if not self.m_data_loaded:
            self._load_data()
        return self.m_tradable_quote_assets


    #------------------------------------------------------------------------------------
    #
    #------------------------------------------------------------------------------------
    def symbols_for_quote_asset(self, quote_asset):
        """
            returs a list of tradable symbol names associated with a given quote asset
            for example :given USTD it may return [BTCUSDT, ETHUSDT, LTCUSDT, ....]
        """
        if not self.m_data_loaded:
            self._load_data()

        if quote_asset in self.m_tradable_symbols_map:
            symbols = self.m_tradable_symbols_map[quote_asset]
            names = [symbol['symbol'] for symbol in symbols]
            return names
        else:
            return []

    #------------------------------------------------------------------------------------
    #
    #------------------------------------------------------------------------------------
    def leveraged_symbol_names(self):
        """
            returns a list of everaged symbols that are currently tradable
        """
        if not self.m_data_loaded:
            self._load_data()

        names = [ symbol['symbol'] for symbol in self.m_tradable_symbols if symbol['baseAsset'].endswith('UP') or symbol['baseAsset'].endswith('DOWN') ]
        return names

    #
    #-------------------- helpes ---------------------------------
    #

    #------------------------------------------------------------------------------------
    #
    #------------------------------------------------------------------------------------
    def _load_url(self, url):
        res = grequests.get(url)
        grequests.map([res])
        return res.response.json()


    #------------------------------------------------------------------------------------
    #
    #------------------------------------------------------------------------------------
    def _load_data(self):
        if self.m_data_loaded:
            return

        exchange_info_data = self._load_url(self.m_url)
        self.m_symbols= exchange_info_data["symbols"]
        self.m_tradable_symbols = [symbol for symbol in self.m_symbols if symbol['status'] == 'TRADING']
        self.m_tradable_quote_assets  = set([symbol['quoteAsset']  for symbol in self.m_tradable_symbols])

        for quote_asset in self.m_tradable_quote_assets:
            self.m_tradable_symbols_map[quote_asset] = [symbol for symbol in self.m_tradable_symbols if symbol['quoteAsset'] == quote_asset]

        self.m_no_tradable_symbols = [symbol for symbol in self.m_symbols if symbol['status'] != 'TRADING']
        self.m_data_loaded = True

        


