import data_getter
import params_private as prv
import params_public as pub


class Strategy:
    def __init__(self):
        self.coin_data = [] # {unix_time, open, close, volume}
        self.close_list = [] # only close prise list
        self.sma_period = prv.sma_period
        self.env_weight = prv.env_weight
        self.now_pos = pub.POS_OUT

    def get_coin_data(self):
        return self.coin_data

    def init_coin_data(self, info):
        """ info : list of [unix_time + ocv] with length sma_period """
        self.coin_data = info
        self.close_list = [row['close'] for row in info]

    def update_coin_data(self, info):
        """ coin_data update """
        if len(self.coin_data) == self.sma_period:
            del self.coin_data[0]
            del self.close_list[0]
            self.coin_data.append(info)
            self.close_list.append(info["close"])
        else:
            print("coin_data length error")

    def envelope_strategy(self):
        def calc_rrr(env, sma, rate):
            return round(((rate + 1) * env - sma) / rate, 4)
        now_price = self.close_list[-1]
        # return 값
        signal = False
        next_pos = self.now_pos

        now_sma = round(sum(self.coin_data)/len(self.coin_data), 4)
        env_up = round(now_sma * (1 + self.env_weight), 4)
        env_down = round(now_sma * (1 - self.env_weight), 4)
        rrr_up = calc_rrr(env_up, now_sma, prv.rrr_rate)
        rrr_down = calc_rrr(env_down, now_sma, prv.rrr_rate)

        # 현재 상태가 OUT 포지션 상태
        if self.now_pos == pub.POS_OUT:
            if now_price <= env_down:
                next_pos = pub.POS_LONG
                signal = True

            if now_price >= env_up:
                next_pos = pub.POS_SHORT
                signal = True
        # 현재 상태가 LONG 포지션 상태
        elif self.now_pos == pub.POS_LONG:
            if (now_price >= now_sma) | (now_price <= rrr_down):
                next_pos = pub.POS_OUT
                signal = True

        # 현재 상태가 SHORT 포지션 상태
        elif self.now_pos == pub.POS_SHORT:
            if (now_price <= now_sma) | (now_price >= rrr_up):
                next_pos = pub.POS_OUT
                signal = True

        # signal = True -> 시그널 변화 있음
        # signal = False -> 시그널 변화 없음
        return signal, next_pos

    def print_data(self):
        print(self.coin_data)
        print(self.close_list)


strategy = Strategy()
strategy.print_data()
