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

#ディレクトリと書き込み用ファイルの作成
def save_file_at_new_dir(new_dir_path, new_filename, new_file_content, mode='w'):
    os.makedirs(new_dir_path, exist_ok=True)
    with open(new_filename, "a") as f:
        f.writelines(",".join(new_file_content))
        f.write("\n")

#18GHzの数値データを物理量に加工
def num_processing(filereg, file, data):
    if refile_9.fullmatch(file.name) != None:
        #ここに数値処理を書く
        int_data = int(data)
        if int_data < 0:
            int_data += 256
        int_data = int_data/2 - 121
        data = str(int_data)
    return data


rxfile = sorted(glob('RxData/*/*/*_csv.log'))
STATUS = r"\n*\d+:\d+:\d+,-?\d*,-?\d*,-?\d*\n*"
FILE_9 = r"RxData\/\d*\/\d*\/\d*.\d*.\d*.9_csv.log"
FILE_NAM = r'/\d+.\d+.\d+.\d+_csv.log'
restatus = re.compile(STATUS)
refile_9 = re.compile(FILE_9)
fine_wether = ['00:00:00','-50'] #仮の値です
PER_DAY = 43200


for file in rxfile:
    result_file = "result"+file
    result_file_directory = re.sub(FILE_NAM, '', result_file)
    with open(file, 'r') as f:
        # null文字があるとファイルがうまく読み込まれないため，null文字を空白に置き換えている．
        reader = csv.reader((line.replace('\0','') for line in f))
        #counter_per_ten: 10ごとにカウントする. 初期値は抽出開始時刻.
        counter_per_ten = 0
        former_row = []
        row_count = 0
        for row in reader:
            row_count += 1
            try:
                #1行ずつ読み込む
                time = row[0]
                time_no_coron = int(time.replace(":",""))
                #10秒ずつ抽出
                if time_no_coron == counter_per_ten:
                    row[1] = num_processing(refile_9, f, row[1])
                    save_file_at_new_dir(result_file_directory, result_file, row[0:2])
                    counter_per_ten += 10
                    counter_per_ten = clock(counter_per_ten)
                else:
                    if time_no_coron > counter_per_ten:
                        # former_rowの形式があっているかを正規表現で確認
                        # あっていなければrow[0:2]を使う．
                        if restatus.fullmatch(','.join(former_row)) != None:
                            former_row[1] = num_processing(refile_9, f, former_row[1])
                            save_file_at_new_dir(result_file_directory, result_file, former_row[0:2])
                        else:
                            row[1] = num_processing(refile_9, f, row[1])
                            save_file_at_new_dir(result_file_directory, result_file, row[0:2])
                        counter_per_ten += 10
                        counter_per_ten = clock(counter_per_ten)
            except:
                pass
            former_row = row
        # データ数が半分以下の場合の処理
        if row_count < PER_DAY/2:
            for d in range(0, PER_DAY):
                save_file_at_new_dir(result_file_directory, result_file, fine_wether[0:2])