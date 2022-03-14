from pythonosc.udp_client import SimpleUDPClient
import time
import sys
import datetime

msg = """
//////////////////////////////////////////
VRChat Open Sound Control 
                  時刻表示プログラム

Analog Clock System Alpha Version 1.1.1

2022/03/13 : 風庭ゆい

注 : 対応したアバターのみ効力を発揮します

//////////////////////////////////////////
"""

#ipとポートをセットするよ
ip = "127.0.0.1"
port = 9000

client = SimpleUDPClient(ip, port)

print(msg)

print('初期化します', end="")

#初期化を実行するよ
client.send_message("/avatar/parameters/AC_hh", float(0.0))
client.send_message("/avatar/parameters/AC_mh", float(0.0))
client.send_message("/avatar/parameters/AC_sc", float(0.0))

print('\rOSC送信を開始します\n')

print("set_ip: ", ip, "\nset_port: ", port, "\n")

print('Ctrl+Cで終了してください\n')

#浮動小数点数演算はなんか知らないけどうまくいかないので良い方法思いつくまでゴリ押す
NUMBER = {
    00:0.00,
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
    13:0.13,
    14:0.14,
    15:0.15,
    16:0.16,
    17:0.17,
    18:0.18,
    19:0.19,
    20:0.20,
    21:0.21,
    22:0.22,
    23:0.23,
    24:0.24,
    25:0.25,
    26:0.26,
    27:0.27,
    28:0.28,
    29:0.29,
    30:0.30,
    31:0.31,
    32:0.32,
    33:0.33,
    34:0.34,
    35:0.35,
    36:0.36,
    37:0.37,
    38:0.38,
    39:0.39,
    40:0.40,
    41:0.41,
    42:0.42,
    43:0.43,
    44:0.44,
    45:0.45,
    46:0.46,
    47:0.47,
    48:0.48,
    49:0.49,
    50:0.50,
    51:0.51,
    52:0.52,
    53:0.53,
    54:0.54,
    55:0.55,
    56:0.56,
    57:0.57,
    58:0.58,
    59:0.59,
    60:0.60
}

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

        time.sleep(1)

        #datetimeモジュールからPCの時刻を取得するよ
        dt_now = datetime.datetime.now()

        hours = dt_now.strftime('%H')
        minutes = dt_now.strftime('%M')
        seconds = dt_now.strftime('%S')

        hours_hand = NUMBER_HOURS[int(hours)]
        minutes_hand = NUMBER[int(minutes)]
        seconds_hand = NUMBER[int(seconds)]

        print("現在時刻(debug):", hours_hand,":",minutes_hand,":",seconds_hand)

        #とんでけーー！！
        
        client.send_message("/avatar/parameters/AC_hh", float(hours_hand))
        client.send_message("/avatar/parameters/AC_mh", float(minutes_hand))
        client.send_message("/avatar/parameters/AC_sc", float(seconds_hand))

except KeyboardInterrupt:

    #Ctrl+Cが押された！
    #全部のパラメータを0にしてから非表示にするよ
    client.send_message("/avatar/parameters/AC_hh", float(0.0))
    client.send_message("/avatar/parameters/AC_mh", float(0.0))
    client.send_message("/avatar/parameters/AC_sc", float(0.0))

    print("\n\n初期化しました\n終了します")

    time.sleep(1)

    #メモリを開放するよ、またねー
    sys.exit()



