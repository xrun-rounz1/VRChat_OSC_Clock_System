from pythonosc.udp_client import SimpleUDPClient
import time
import sys
import datetime

msg = """
//////////////////////////////////////////
VRChat Open Sound Control 
                  時刻表示プログラム

Analog Clock System Beta Version 1.0

最終更新 : 2022/03/15

//////////////////////////////////////////
"""

#作成 : 風庭ゆい

#ipとポートをセット
ip = "127.0.0.1"
port = 9000

client = SimpleUDPClient(ip, port)

print(msg)

print('初期化します', end="")

#初期化を実行
client.send_message("/avatar/parameters/AC_hh", float(0.0))
client.send_message("/avatar/parameters/AC_mh", float(0.0))
client.send_message("/avatar/parameters/AC_sc", float(0.0))

print('\rOSC送信を開始します\n')

print("set_ip: ", ip, "\nset_port: ", port, "\n")

print('Ctrl+Cで終了できます\n')

NUMBER_HOURS = {
    0:0.0,
    1:0.01,
    2:0.02,
    3:0.03,
    4:0.04,
    5:0.05,
    6:0.06,
    7:0.07,
    8:0.08,
    9:0.09,
    10:0.10,
    11:0.11,
    12:0.12,
    13:0.01,
    14:0.02,
    15:0.03,
    16:0.04,
    17:0.05,
    18:0.06,
    19:0.07,
    20:0.08,
    21:0.09,
    22:0.10,
    23:0.11,
    24:0.12
}

try:

    while True:

        #PCのローカル時間を取得
        dt_now = datetime.datetime.now()

        hours = dt_now.hour
        minutes = dt_now.minute
        seconds = dt_now.second

        hours_hand = NUMBER_HOURS[hours]
        minutes_hand = minutes / 100
        seconds_hand = seconds / 100

        print("\r現在時刻:", hours,":",minutes,":",seconds, end="")

        #とんでけーー！！
        client.send_message("/avatar/parameters/AC_hh", hours_hand)
        client.send_message("/avatar/parameters/AC_mh", minutes_hand)
        client.send_message("/avatar/parameters/AC_sc", seconds_hand)

        time.sleep(1)

except KeyboardInterrupt:

    #終了時初期化
    client.send_message("/avatar/parameters/AC_hh", float(0.0))
    client.send_message("/avatar/parameters/AC_mh", float(0.0))
    client.send_message("/avatar/parameters/AC_sc", float(0.0))

    print("\n\n初期化しました\n終了します")

    time.sleep(1)

    #メモリを開放するよ、またねー
    sys.exit()



