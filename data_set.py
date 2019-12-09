import csv
import re
#Ï
def clock(counter_per_ten):
    str_counter_per_ten = str(counter_per_ten)
    try:
        if str_counter_per_ten[-2] == '6':
            counter_per_ten += 40
        if str_counter_per_ten[-4] == '6':
            counter_per_ten += 4000
    except:
        pass

with open('/Users/e185742/rain_fall/RxData/200906/20090601/192.168.100.9_csv.log', 'r') as f:
    reader = csv.reader(f)
    ignore = 0
    counter_per_ten = 0
    for row in reader:
        #最初の2行を無視
        if ignore >= 2:
            #1行ずつ読み込む
            time = row[0]
            time_no_coron = int(time[-8:-6]+time[-5:-3]+time[-2:])
            #10秒ずつ抽出
            #counter_per_ten: 抽出開始時間
            if time_no_coron <= counter_per_ten:
                if time_no_coron == counter_per_ten:
                    print(row)
                else:
                    #10秒単位で一致するデータがなかった時の処理
                    #1秒前に戻ってそれを代替データとして採用する．
                    pass
            else:
                counter_per_ten += 10
                clock(counter_per_ten)
        ignore += 1

