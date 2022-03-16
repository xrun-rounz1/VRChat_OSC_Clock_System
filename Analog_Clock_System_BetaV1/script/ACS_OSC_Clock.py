from pythonosc.udp_client import SimpleUDPClient
import time
import sys
import datetime
import math

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

HOURS_NOTATION = {
    0:0,
    1:1,
    2:2,
    3:3,
    4:4,
    5:5,
    6:6,
    7:7,
    8:8,
    9:9,
    10:10,
    11:11,
    12:12,
    13:1,
    14:2,
    15:3,
    16:4,
    17:5,
    18:6,
    19:7,
    20:8,
    21:9,
    22:10,
    23:11,
    24:12
}

try:

    while True:

        #PCのローカル時間を取得
        dt_now = datetime.datetime.now()

        hours = dt_now.hour
        minutes = dt_now.minute
        seconds = dt_now.second

        #12時間表記をintで取りたい
        #strftime(%h)で取るのもなんかなぁ。。。
        #もっと良い方法があるはず、思いつくまでとりあえずこれで
        hours_notation = HOURS_NOTATION[hours]

        minutes_hand = minutes / 100
        seconds_hand = seconds / 100

        #上書きするとなぜか実際の送信時間と一秒違う、なんで？？
        #あと上書きしてるせいで前の表示が残るようになったのでとりあえず垂れ流すようにする
        #print("\r現在時刻:", hours,":",minutes,":",seconds, end="")
        print("現在時刻:", hours,":",minutes,":",seconds)

        #hourを60に分割
        min_hours = math.floor(minutes / 12)

        if hours_notation != 12:
            hours_hh = hours / 20

        else:
            hours_hh = 0

        hh = hours_hh + (min_hours / 100)
        hours_hand = round(hh, 2)

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



