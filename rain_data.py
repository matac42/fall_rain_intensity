import csv
import os
from glob import glob
import re

#ディレクトリと書き込み用ファイルの作成
def save_file_at_new_dir(new_dir_path, new_filename, new_file_content):
    os.makedirs(new_dir_path, exist_ok=True)
    with open(new_filename, "a") as f:
        f.writelines(",".join(new_file_content))
        f.write("\n")


rainData = sorted(glob('RainData/*/*_rain.csv'))
except_count = 0
FILE_NAM = r'\d*_rain.csv'
for file in rainData:
    result_file = "result"+file
    result_file_directory = re.sub(FILE_NAM, '', result_file)
    with open(file, "r") as f:
        reader = csv.reader((line.replace('\0','') for line in f))
        for row in reader:
            try:
                result = row
                result[1] = str(int(row[1]) * 60)
                save_file_at_new_dir(result_file_directory, result_file, result)
            except:
                except_count += 1