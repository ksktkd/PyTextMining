import MeCab
import sys
import re
import collections
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rc

if __name__ == '__main__' : 
    # ファイル読み込み
    with open("line_pomatti.txt") as f:
        data = f.readlines()

    prev_line = []
    date = ""
    full_data = []
    for line in data:
        line = line.split('\t')

        # Remove \n
        if line[0] == '\n' : continue

        # Remove the action information
        if len(line) == 2 : continue

        # Store the date info
        ## ex. 2020/05/19(火) --> OK
        if re.fullmatch(".*\/.*\/.*\(.*\)\n", line[0]) is not None: 
            date = line[0].replace("\n","")
            continue

        # Save the previous texts
        if   len(line) == 3 : 
            line.insert(0, date)
            prev_line = line
            
            full_data.append(line)

        elif len(prev_line) == 4 and len(line) == 1 :
            line.insert(0, date)
            line.insert(1, prev_line[1])
            line.insert(2, prev_line[2])
            
            full_data.append(line)

    # Count
    ## Create the data frame using pandas.DataFrame
    df = pd.DataFrame(data=full_data, columns=["date", "time", "name", "content"])
    print(df)

    print((df["name"] == "Keisuke Ogawa").sum())
    print((df["name"] == "Kosuke Takeda").sum())
    print((df["name"] == "又吉康平").sum())
    print(df["date"])
    print(df["date"].value_counts(sort=False))
    vc = df["date"].value_counts().sort_index()
    print(vc)

    font  = fm.FontProperties(fname="/System/Library/Fonts/ヒラギノ角ゴシック W2.ttc")
#
#    for var in ("date", "name"):
#        plt.figure(figsize=(50,10))
#        df[var].value_counts().plot(kind='bar')
#        plt.xticks(fontproperties=font)
#        plt.savefig("ranking_{}.png".format(var))
#
    
    df_ogawa     = df[df["name"] == 'Keisuke Ogawa']
    df_takeda    = df[df["name"] == 'Kosuke Takeda']
    df_matayoshi = df[df["name"] == '又吉康平']
    
    data_ogawa     = df_ogawa["date"].value_counts().sort_index()
    data_takeda    = df_takeda["date"].value_counts().sort_index()
    data_matayoshi = df_matayoshi["date"].value_counts().sort_index()
    
    data_merged    = pd.concat([data_ogawa, data_takeda, data_matayoshi], axis=1)
    print("***************")
    print(data_ogawa)
    print(data_takeda)
    print(data_matayoshi)
    print(data_merged)
    df_merged = pd.DataFrame({'Ogawaman': data_ogawa, 'Takeda': data_takeda, 'Matayo' : data_matayoshi})

    fig, axis = plt.subplots(figsize=(45,20))
    df_merged.plot(
            ax=axis,
            kind='bar', 
            width=1.0, 
            stacked=True,
            )

    axis.set_xlabel('日時'  , fontproperties=font, fontsize=40)
    axis.set_xlabel('日時'  , fontproperties=font, fontsize=40)
    axis.set_ylabel('発言数', fontproperties=font, fontsize=40)
    axis.set_title('LINEテキスト分析', fontproperties=font,fontsize=50 )

    plt.xticks(fontproperties=font, fontsize=5)
    plt.yticks(fontproperties=font, fontsize=18)
    plt.legend(fontsize=50)
    fig.savefig("hist.png", dpi=300)

    exit(1)
    
    # パース
    mecab = MeCab.Tagger("-Owakati")
    parse = mecab.parse(data)
    parse = parse.split(" ")
    coll = collections.Counter(parse)

    results = {}
    for word, count in coll.most_common():
        if count < 100: continue
        print("{} {}".format(word, count))
        results[word] = count
    
    
    x = []
    y = []
    font  = fm.FontProperties(fname="/System/Library/Fonts/ヒラギノ角ゴシック W2.ttc")
    
    for key, value in results.items():
        x.append(key)
        y.append(value)
    #    print("{} : {} ".format(key,value))
    
    #print(x)
    #print(y)
    plt.figure(figsize=(40,10))
    plt.bar(x, y)
    plt.xticks(rotation=90, fontproperties=font)
    plt.xticks(rotation=90)
    plt.xlim(-1, len(results))
    plt.savefig("ranking.png")
    
    print("FINISH")

