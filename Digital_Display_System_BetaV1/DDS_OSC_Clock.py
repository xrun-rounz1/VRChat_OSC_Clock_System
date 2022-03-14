from pythonosc.udp_client import SimpleUDPClient
import time
import sys
import datetime

msg = """
//////////////////////////////////////////
VRChat Open Sound Control 
                  時刻表示プログラム

Digital Display System Beta Version 1.2

2022/03/14 : 風庭ゆい

注 : 対応したアバターのみ効力を発揮します

//////////////////////////////////////////
"""

#ipとポートをセットするよ
ip = "127.0.0.1"
port = 9000

client = SimpleUDPClient(ip, port)

print(msg)

print('初期化します', end="")

#初期化を実行するよ、一度0を送信してからもう一度表示させるよ
client.send_message("/avatar/parameters/DD_thp", 0)
client.send_message("/avatar/parameters/DD_hp", 0)
client.send_message("/avatar/parameters/DD_tp", 0)
client.send_message("/avatar/parameters/DD_op", 0)

print('\rOSC送信を開始します\n')

print("set_ip: ", ip, "\nset_port: ", port, "\n")

print('Ctrl+Cで終了してください\n')

try:

    while True:

        #datetimeモジュールからPCの時刻を取得するよ
        dt_now = datetime.datetime.now()

        #時、分、秒で分けてゼロ埋めするよ
        hours = dt_now.strftime('%H')
        minutes = dt_now.strftime('%M')
        seconds = dt_now.strftime('%S')

        num_h = hours.zfill(2)
        num_m = minutes.zfill(2)
        num_s = seconds.zfill(2)

        #それぞれの桁を変数に入れるよ
        htp = num_h[-2]
        hop = num_h[-1]

        mtp = num_m[-2]
        mop = num_m[-1]

        stp = num_s[-2]
        sop = num_s[-1]

        print("\r現在時刻:", htp,hop,":",mtp,mop,":",stp,sop, end="")

        #とんでけーー！！
        client.send_message("/avatar/parameters/DD_thp", int(htp))
        client.send_message("/avatar/parameters/DD_hp", int(hop))
        client.send_message("/avatar/parameters/DD_tp", int(mtp))
        client.send_message("/avatar/parameters/DD_op", int(mop))

        #飛んでったから一秒待つよ
        #ここを変更で送信頻度を変更できるよ
        time.sleep(1)

except KeyboardInterrupt:

    #Ctrl+Cが押された！
    #全部のパラメータを0にしてから非表示にするよ
    client.send_message("/avatar/parameters/DD_thp", 0)
    client.send_message("/avatar/parameters/DD_hp", 0)
    client.send_message("/avatar/parameters/DD_tp", 0)
    client.send_message("/avatar/parameters/DD_op", 0)

    print("\n\n初期化しました\n終了します")

    time.sleep(1)

    #メモリを開放するよ、またねー
    sys.exit()



