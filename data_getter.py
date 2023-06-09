import requests

import params_private


class DataGetter:
    """
        from binance data getter
        """

    ISO_DATEFORMAT = "%Y-%m-%dT%H:%M:%S"
    COIN_NAME = "XRPUSDT"
    INTERVAL = "5m"
    LIMIT = params_private.sma_period

    def __init__(self):
        self.url = f'https://api.binance.com/api/v3/klines?symbol={self.COIN_NAME}&interval={self.INTERVAL}&limit={self.LIMIT}'

    def get_info(self):
        """
        :return: datetime + ohlcv
        """
        data = self.__get_data_from_server()
        return self.__create_candle_info(data[-1])

    def get_init_info(self):
        data = self.__get_data_from_server()
        return [self.__create_candle_info(data[i]) for i in range(0, self.LIMIT)]

    @staticmethod
    def __create_candle_info(data):
        """
        :return:{
            "datetime",
            "open",
            "close",
            "volume",
        }
        """
        try:
            return {
                "datetime": float(data[0]),
                "open": float(data[1]),
                "close": float(data[4]),
                "volume": float(data[5]),
            }
        except KeyError as err:
            # logger
            return None

    def __get_data_from_server(self):
        params = {
            'symbol': self.COIN_NAME,
            'interval': self.INTERVAL,
        }
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except ValueError as error:
            # logger
            raise UserWarning("Fail get data from server") from error
        except requests.exceptions.HTTPError as error:
            # logger
            raise UserWarning("Fail get data from server") from error
        except requests.exceptions.RequestException as error:
            # logger
            raise UserWarning("fail get data from server") from error


dg = DataGetter()
# print(dg.get_init_info())
# print(dg.get_info())
