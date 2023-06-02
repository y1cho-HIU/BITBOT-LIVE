import params_private as prv
import params_public as pub


class Strategy:
    def __init__(self):
        self.coin_data = []

    def strategy(self, now_pos, sma_list, env_weight):
        def calc_rrr(env, sma, rate):
            return round(((rate + 1) * env - sma) / rate, 4)

        now_price = sma_list[-1]
        # return 값
        signal = False
        next_pos = now_pos

        now_sma = round(sum(sma_list)/len(sma_list), 4)
        env_up = round(now_sma * (1 + env_weight), 4)
        env_down = round(now_sma * (1 - env_weight), 4)
        rrr_up = calc_rrr(env_up, now_sma, prv.rrr_rate)
        rrr_down = calc_rrr(env_down, now_sma, prv.rrr_rate)

        # 현재 상태가 OUT 포지션 상태
        if now_pos == pub.POS_OUT:
            if now_price <= env_down:
                next_pos = pub.POS_LONG
                signal = True

            if now_price >= env_up:
                next_pos = pub.POS_SHORT
                signal = True
        # 현재 상태가 LONG 포지션 상태
        elif now_pos == pub.POS_LONG:
            if (now_price >= now_sma) | (now_price <= rrr_down):
                next_pos = pub.POS_OUT
                signal = True

        # 현재 상태가 SHORT 포지션 상태
        elif now_pos == pub.POS_SHORT:
            if (now_price <= now_sma) | (now_price >= rrr_up):
                next_pos = pub.POS_OUT
                signal = True

        # signal = True -> 시그널 변화 있음
        # signal = False -> 시그널 변화 없음
        return signal, next_pos
