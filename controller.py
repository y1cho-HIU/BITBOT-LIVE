import strategy
import operator


class LiveController:
    BASIC_STATEMENT = "명령어를 입력하세요. (h, help : 도움말): "

    def __init__(self):
        self.operator = operator.Operator()
        self.command_list = []
        self.create_command()
        self.strategy = strategy.strategy()

    def create_command(self):
        self.command_list = [
            {
                "guide": "{0:15}도움말 출력".format("h, help"),
                "cmd": ["help", "h"],
                "action": self.help_command,
            },
            {
                "guide": "{0:15}거래 시작".format("r, run"),
                "cmd": ["run", "r"],
                "action": self.start_command,
            },
            {
                "guide": "{0:15}거래 중지".format("s, stop"),
                "cmd": ["stop", "s"],
                "action": self.stop_command,
            },
            {
                "guide": "{0:15}거래 현황".format("i, info"),
                "cmd": ["info", "i"],
                "action": self.info_command,
            },
        ]

    def main(self):
        while not self.stop:
            try:
                key = input(self.BASIC_STATEMENT)
                self._on_command(key)
            except EOFError:
                break

    def _on_command(self, key):
        for cmd in self.command_list:
            if key.lower() in cmd["cmd"]:
                print(f"{cmd['cmd'][0].upper()} 명령어 실행")
                cmd["action"]()
                return
        print("명령어를 다시 입력해주세요. (명령어 도움말 : h, help)")

    def help_command(self):
        """ 가이드 문구 출력 """
        print("===== 명령어 목록 =====")
        for command in self.command_list:
            print(command["guide"])

    def start_command(self):
        """ start """
        if self.operator.start() is not True:
            """ ??? """

    def stop_command(self, signum = None, frame=None):
        """ stop """
        del frame
        if signum is not None:
            print("강제 종료 신호 감지")
        print("프로그램 종료 중... ")
        if self.operator is not None:
            self.operator.stop()
        print("프로그램을 종료했습니다.")

    def info_command(self):
        """ information display """
        self._get_trading_record()

    def _get_trading_record(self):
        """ get trading record """
        for record in self.trading_record:
            print(record)