import csv
import os
from glob import glob
import re
import pandas as pd
import matplotlib.pyplot as plt

#ディレクトリと書き込み用ファイルの作成
def save_file_at_new_dir(new_dir_path, new_filename, new_file_content):
    os.makedirs(new_dir_path, exist_ok=True)
    with open(new_filename, "a") as f:
        f.writelines(",".join(new_file_content))
        f.write("\n")


def judge_range(rain_data, data_list):
    rain_amount = 0.
    rain_data = float(rain_data)
    while rain_data > rain_amount:
        rain_amount += 3.
    data_list[int(rain_amount/3.)] += 1
    # if rain_data == 0:
    #     data_list[int(rain_amount/3.)] += 1
    # else:
    #     data_list[int(rain_amount/3.)-1] += 1
    
    return data_list


rainData = sorted(glob('RainData/*/*_rain.csv'))
FILE_NAM = r'\d*_rain.csv'
data_list = [0] * 51
for file in rainData:
    with open(file, "r") as f:
        reader = csv.reader((line.replace('\0','') for line in f))
        for row in reader:
            try:
                result = row
                result[1] = str(float(row[1]) * 0.0083333 * 60.0)
                data_list = judge_range(result[1], data_list)
            except:
                pass

file_name = "resultRainData.csv"
accumulation = 0
all_data = 0
upper_limit = 150
for data in data_list:
    all_data += data
with open(file_name, "a") as f:
    f.write("CumulativeTimeRate,RainfallIntensity\n")
for data in reversed(data_list):
    accumulation += data
    ratio = float(accumulation) / float(all_data) * 100
    with open(file_name, "a") as f:
        f.write(str(upper_limit)+","+str(ratio)+"\n")
    upper_limit -= 3

# プロット
df = pd.read_csv('resultRainData.csv', index_col="RainfallIntensity")
plt.plot(df)
plt.xscale('log')
plt.xlabel('Cumulative time rate(%)')
plt.ylabel('Rainfall intensity(mm/h)')
plt.show()