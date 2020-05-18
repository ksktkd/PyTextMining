import MeCab
import sys
import re
import collections

if __name__ == '__main__' : 
    # ファイル読み込み
    with open("LINE.txt") as f:
        data = f.read()
    
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

