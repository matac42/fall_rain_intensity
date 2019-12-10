import csv
import re
from glob import glob
import codecs

#10秒単位のカウンターの動きを時間の経過のように振る舞わせる．例) 60sの次は70sではなく1m00sにする．
def clock(counter_per_ten):
    str_counter_per_ten = str(counter_per_ten)
    try:
        if str_counter_per_ten[-2] == '6':
            counter_per_ten += 40
        if str_counter_per_ten[-4] == '6':
            counter_per_ten += 4000
    except:
        pass
    return counter_per_ten

for file in glob('RxData/*/*/*_csv.log'):
    print(file)
    with open(file, 'r') as f:
        # null文字があるとファイルがうまく読み込まれないため，null文字を空白に置き換えている．
        reader = csv.reader((line.replace('\0','') for line in f))
        #counter_per_ten: 10ごとにカウントする. 初期値は抽出開始時刻.
        counter_per_ten = 0
        former_row = []
        for row in reader:
            try:
                #1行ずつ読み込む
                time = row[0]
                time_no_coron = int(time[-8:-6]+time[-5:-3]+time[-2:])
                #10秒ずつ抽出
                if time_no_coron == counter_per_ten:
                    print(row[0:2])
                    # ファイル書き込み処理はここ
                    counter_per_ten += 10
                    counter_per_ten = clock(counter_per_ten)
                else:
                    if time_no_coron > counter_per_ten:
                        counter_per_ten += 10
                        counter_per_ten = clock(counter_per_ten)
                        print(former_row[0:2], "former")
                        # ファイル書き込み処理はここ
                    else:
                        pass
            except:
                pass
            former_row = row
    print(file)