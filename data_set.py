import csv
import re
from glob import glob
import codecs
import os

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

def save_file_at_new_dir(new_dir_path, new_filename, new_file_content, mode='w'):
    os.makedirs(new_dir_path, exist_ok=True)
    with open(new_filename, "a") as f:
        f.writelines(",".join(new_file_content))
        f.write("\n")

rxfile = sorted(glob('RxData/*/*/*_csv.log'))

    

for file in rxfile:
    result_file = "result"+file
    result_file_directory = re.sub(r'/\d+.\d+.\d+.\d+_csv.log', '', result_file)
    with open(file, 'r') as f:
        # null文字があるとファイルがうまく読み込まれないため，null文字を空白に置き換えている．
        reader = csv.reader((line.replace('\0','') for line in f))
        #counter_per_ten: 10ごとにカウントする. 初期値は抽出開始時刻.
        counter_per_ten = 0
        former_row = []
        status = r"\n*\d+:\d+:\d+,-?\d*,-?\d*,-?\d*\n*"
        restatus = re.compile(status)
        for row in reader:
            try:
                #1行ずつ読み込む
                time = row[0]
                time_no_coron = int(time.replace(":",""))
                #10秒ずつ抽出
                if time_no_coron == counter_per_ten:
                    # print(row[0:2])
                    # ファイル書き込み処理はここ
                    save_file_at_new_dir(result_file_directory, result_file, row[0:2])
                    counter_per_ten += 10
                    counter_per_ten = clock(counter_per_ten)
                else:
                    if time_no_coron > counter_per_ten:
                        counter_per_ten += 10
                        counter_per_ten = clock(counter_per_ten)
                        # print(former_row[0:2])
                        # ファイル書き込み処理はここ
                        # former_rowの形式があっているかを正規表現で確認
                        # あっていなければrow[0:2]を使う．
                        # save_file_at_new_dir(result_file_directory, result_file, former_row[0:2])
                        if restatus.fullmatch(','.join(former_row)) != None:
                            save_file_at_new_dir(result_file_directory, result_file, former_row[0:2])
                        else:
                            save_file_at_new_dir(result_file_directory, result_file, row[0:2])
                    else:
                        pass
            except:
                pass
            former_row = row