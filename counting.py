import MeCab
import sys
import re
import collections

if __name__ == '__main__' : 
    # ファイル読み込み
    with open("line_pomatti.txt") as f:
        data = f.readlines()

    prev_line = []
    date = ""
    for line in data:
        line = line.split('\t')

        # Remove \n
        if line[0] == '\n' : continue

        # Remove the action information
        if len(line) == 2 : continue

        # Store the date info
        if   '2015' in line[0] : date = line[0].replace("\n",""); continue
        elif '2016' in line[0] : date = line[0].replace("\n",""); continue
        elif '2017' in line[0] : date = line[0].replace("\n",""); continue
        elif '2018' in line[0] : date = line[0].replace("\n",""); continue
        elif '2019' in line[0] : date = line[0].replace("\n",""); continue
        elif '2020' in line[0] : date = line[0].replace("\n",""); continue

        # Save the previous texts
        if   len(line) == 3 : 
            line.insert(0, date)
            prev_line = line
            print(line)

        elif len(prev_line) == 4 and len(line) == 1 :
            line.insert(0, date)
            line.insert(1, prev_line[1])
            line.insert(2, prev_line[2])
            print(line)

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
    
    import matplotlib
    from matplotlib import font_manager as fm, rc
    import matplotlib.pyplot as plt
    
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

