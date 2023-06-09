import threading
from datetime import datetime

import data_getter
import strategy
import trader
import params_public as pub


class Operator:
    def __init__(self, on_exception=None):
        self.dataGetter = data_getter.DataGetter()
        self.strategy = strategy.Strategy()
        self.trader = trader.MockTrader()
        self.interval = 300
        self.is_timer_running = False
        self.timer = None
        self.timer_expired_time = None
        self.on_exception = on_exception

    def set_interval(self, interval):
        self.interval = interval

    def _start_timer(self):
        def on_timer_expired():
            self.timer_expired_time = datetime.now()

        if self.interval < 1:
            self.is_timer_running = True
            on_timer_expired()
            return

        adjusted_interval = self.interval

        if self.interval > 1 and self.timer_expired_time is not None:
            time_delta = datetime.now() - self.timer_expired_time
            adjusted_interval = self.interval - round(time_delta.total_seconds(), 1)

        self.timer = threading.Timer(adjusted_interval, on_timer_expired)
        self.timer.start()
        self.is_timer_running = True
        return

    def _get_init_info(self):
        trading_info = self.dataGetter.get_init_info()
        self.strategy.init_coin_data(trading_info)

    def _execute_trading(self):
        """ 자동 거래 이후 타이머 실행
            1. get_info from dataGetter
            2. update coin_data to strategy
            3. get_signal from strategy
            4. send request to trader
            5. start timer
        """
        try:
            if len(self.strategy.get_coin_data()) == 0:
                trading_info = self.dataGetter.get_init_info()
                self.strategy.init_coin_data(trading_info)
            else:
                trading_info = self.dataGetter.get_info()
                self.strategy.update_coin_data(trading_info)

            """ get signal from strategy """
            signal, next_pos = self.strategy.envelope_strategy()
            if signal:
                """ change position -> send request """
                bid, ask = self._request_now_price() # 매수, 매도
                if next_pos == pub.POS_OUT:
                    self.trader.sell_order(ask)
                if next_pos == pub.POS_LONG:
                    self.trader.buy_order(bid, pub.POS_LONG)
                if next_pos == pub.POS_SHORT:
                    self.trader.buy_order(bid, pub.POS_SHORT)

        except (AttributeError, TypeError) as msg:
            """ logger (executing fail {msg}) """

        except Exception as exc:
            if self.on_exception is not None:
                self.on_exception("Unexpected Error")
            raise RuntimeError("Unexpected Error") from exc

        self._start_timer()

    @staticmethod
    def _request_now_price():
        """
        :return: bid(매수), ask(매도)
        """
        import ccxt

        xrp_data = ccxt.binance().fetch_ticker("XRP/USDT")
        bid = xrp_data['bid']
        ask = xrp_data['ask']

        # bid = 매수, ask = 매도
        return bid, ask
