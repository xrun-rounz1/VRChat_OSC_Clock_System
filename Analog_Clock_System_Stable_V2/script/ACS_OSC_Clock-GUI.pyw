from pythonosc.udp_client import SimpleUDPClient
import PySimpleGUI as sg
import time
import threading
import sys
import datetime
import math
import ipaddress

msg = """
//////////////////////////////////////////
VRChat Open Sound Control 
                  時刻表示プログラム

Analog Clock System Stable Version 2.0.1 for GUI

//////////////////////////////////////////
"""

#作成 : 風庭ゆい
#最終更新 : 2022/04/03

AC_hh = "AC_hh"
AC_mh = "AC_mh"
AC_sc = "AC_sc"

buttonflag = False

sg.theme("Default")

layout = [
    [
        sg.Text("IP", size=(8,1)), sg.InputText("127.0.0.1", key="ip", size=(15,1))
    ],

    [
        sg.Text("Port", size=(8,1)), sg.InputText("9000", key="port", size=(15,1))
    ],

    [
        sg.Text("送信間隔", size=(8,1)), sg.InputText("1", key="interval", size=(5,1)),
        sg.Text("秒")
    ],

    [
        sg.Submit(button_text="設定を反映", key="settings"),
        sg.Text("設定中のIPアドレス:ポート番号 ▷"),
        sg.Text("127.0.0.1:9000", size=(15,1), key="paramtext")
    ],

    [
        sg.Text("Advanced Settings---"),
        sg.Text(" 【送信するパラメータを変更します】")
    ],

    [sg.Text("時", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_hh", key="hh", size=(30,1))],

    [sg.Text("分", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_mh", key="mh", size=(30,1))],

    [sg.Text("秒", size=(2,1)), sg.Text("/avatar/parameters/"), sg.InputText("AC_sc", key="sc", size=(30,1))],

    [],

    [
        sg.Button("送信開始", key="startbutton"),
        sg.Text("送信停止中", size=(20,1), key="sstext")
    ],

    [
        sg.Text("", key="time")
    ]

]

window = sg.Window("Analog Clock System Beta 2.0.1 for GUI", layout)

class Receive():
    def __init__(self):
        self.ROOP = False


    def target(self):

        client = SimpleUDPClient(ip, port)

        param_hh = "/avatar/parameters/" + AC_hh
        param_mh = "/avatar/parameters/" + AC_mh
        param_sc = "/avatar/parameters/" + AC_sc

        print(param_hh)
        print(param_mh)
        print(param_sc)

        while (self.ROOP):

            dt_now = datetime.datetime.now()

            hours = dt_now.hour % 12
            minutes = dt_now.minute
            seconds = dt_now.second
            meridian = dt_now.strftime('%p')

            minutes_hand = minutes / 100
            seconds_hand = seconds / 100

            time_hh = str(hours)
            time_mh = str(minutes)
            time_sc = str(seconds)

            time_notify = time_hh + ":" + time_mh + ":" + time_sc + "." + meridian + "."

            print("\r現在時刻:", time_notify, end="")

            window["time"].update("送信中の現在時刻 :" + str(time_notify))

            #hourを60に分割
            min_hours = math.floor(minutes / 12)

            if hours != 12:
                hours_hh = hours / 20

            else:
                hours_hh = 0

            hh = hours_hh + (min_hours / 100)
            hours_hand = round(hh, 2)

            #とんでけーー！！
            client.send_message(param_hh, hours_hand)
            client.send_message(param_mh, minutes_hand)
            client.send_message(param_sc, seconds_hand)

            time.sleep(interval)


    def start(self):
        self.thread = threading.Thread(target = self.target)
        self.thread.start()


if __name__ == "__main__":
    r = Receive()

    def startEvent(event):
        r.ROOP = True
        r.start()


    def changeEvent(event):
        pass


    def finishEvent(event):
        r.ROOP = False
        window.close()
        sys.exit()


    def isalnum_ascii(s):
        str_list = list(s)

        for i in str_list:
            if not i == "_":
                if i.isalnum() and i.isascii():
                    str_list[str_list.index(i)] = 1

                else:
                    str_list[str_list.index(i)] = 0

            else:
                str_list[str_list.index(i)] = 1

        if not 0 in str_list:
            return True

        return False


    def ip_check(values): #IPv4が有効かどうか
        try:
            ip_set = ipaddress.ip_address(values["ip"])

            if type(ip_set) is ipaddress.IPv4Address:
                ip = str(ip_set)

            else:
                sg.popup("エラーが発生しました！\n【このIPは使用できません】")
                window["ip"].update("127.0.0.1")
                ip = "127.0.0.1"

        except ValueError:
            sg.popup("エラーが発生しました！\n【IPに使用できない値が含まれています】")
            window["ip"].update("127.0.0.1")
            ip = "127.0.0.1"

        finally:
            return ip


    def port_check(values): #ポート番号が有効かどうか
        try:
            port_set = int(values["port"])

            if 0 <= port_set <= 65535:
                port = port_set

            else:
                sg.popup("エラーが発生しました！\n【このポート番号は無効です】")

                window["port"].update("9000")
                port = 9000

        except ValueError:
            sg.popup("エラーが発生しました！\n【Portに使用できない値が含まれています】")

            window["port"].update("9000")
            port = 9000

        finally:
            return port

    def interval_check(values):
        try:
            interval_set = int(values["interval"])

            if 1 <= interval_set <= 3600:
                interval = interval_set

            else:
                sg.popup("エラーが発生しました！\n【送信間隔が小さい、または大きすぎます】")

                window["interval"].update("1")
                interval = 1

        except ValueError:
            sg.popup("エラーが発生しました！\n【入力された送信間隔は無効です】")

            window["interval"].update("1")
            interval = 1

        finally:
            return interval


    def str_check(values): #パラメータが有効かどうか
        if parameter_check(values):
            hh = values["hh"]
            mh = values["mh"]
            sc = values["sc"]

            return hh, mh, sc

        else:
            sg.popup("エラーが発生しました！\n【Parametersに使用できない文字列が含まれています】")

            window["hh"].update("AC_hh")
            window["mh"].update("AC_mh")
            window["sc"].update("AC_sc")

            hh = "AC_hh"
            mh = "AC_mh"
            sc = "AC_sc"

            return hh, mh, sc
            

    def parameter_check(values):
        param_list = [
            values["hh"],
            values["mh"],
            values["sc"]
        ]

        for i in param_list:
            if not isalnum_ascii(i):
                return False
                
            if " " in i:
                return False

        return True


while True:

    event, values = window.read()
    print(event, values)

    if event is None:
        break

    if event == sg.WINDOW_CLOSED: #ウインドウの×ボタン
        break

    if event == "settings": #設定反映ボタン
        ip = ip_check(values)
        port = port_check(values)
        interval = interval_check(values)
        window["paramtext"].update(ip + ":" + str(port))

        print(ip, ":", end="")
        print(port)
        print(interval, "秒")

        strcheck = str_check(values)

        AC_hh = strcheck[0]
        AC_mh = strcheck[1]
        AC_sc = strcheck[2]


    if event == "startbutton": #送信ボタン
        if not buttonflag: #送信ボタンがFalseのとき
            ip = ip_check(values)
            port = port_check(values)
            interval = interval_check(values)
            window["paramtext"].update(ip + ":" + str(port))

            print("start")

            startEvent(event)

            window["startbutton"].update("送信停止")
            window["sstext"].update("送信を開始しました")
            buttonflag = True

            window["ip"].update(disabled=True)
            window["port"](disabled=True)
            window["interval"](disabled=True)
            window["settings"](disabled=True)
            window["hh"](disabled=True)
            window["mh"](disabled=True)
            window["sc"](disabled=True)

        else: #送信ボタンがTrueのとき
            r.ROOP = False
            window["startbutton"].update("送信開始")
            window["sstext"].update("送信を停止しました")
            buttonflag = False

            window["ip"].update(disabled=False)
            window["port"](disabled=False)
            window["interval"](disabled=False)
            window["settings"](disabled=False)
            window["hh"](disabled=False)
            window["mh"](disabled=False)
            window["sc"](disabled=False)

finishEvent(event)