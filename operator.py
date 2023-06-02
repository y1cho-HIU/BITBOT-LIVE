import threading
from datetime import datetime

import data_getter
import strategy


class Operator:
    def __init__(self, on_exception=None):
        self.dataGetter = data_getter.DataGetter
        self.strategy = strategy
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

    def _execute_trading(self):
        """ 자동 거래 이후 타이머 실행
            1. get_info from dataGetter
            2. update coin_data to strategy
            3. get_signal from strategy
            4. send request to trader
            5. start timer
        """