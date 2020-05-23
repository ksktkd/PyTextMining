
from LineTextHelper import LineTextHelper
import MeCab
import collections
import pandas as pd
from matplotlib import font_manager as fm, rc
from matplotlib import rcParams
import matplotlib.pyplot as plt

if __name__ == "__main__":
    lth = LineTextHelper('line_pomatti.txt')
    
    stop_words = []
    with open("Japanese.txt") as f:
        lines = f.readlines()
        for line in lines:
            stop_words.append(line.replace('\n',''))

    full_list = []
    full_list_wo_sword = []
    mecab = MeCab.Tagger("-Owakati")
    for line in lth.get_full_data():
    
        words = mecab.parse(line[3])
        words = words.split(" ")
        del words[-1]
    
        full_list.extend(words)

        for word in words:
            if word not in stop_words:
                full_list_wo_sword.append(word)
    
    # Counting
    coll = collections.Counter(full_list_wo_sword)
    
    results = {}
    for word, count in coll.most_common():
        if count < 100 : 
            continue
        print("{} {}".format(word, count))
        results[word] = count
    
    # Count
    ## Create the data frame using pandas.DataFrame
    df = pd.DataFrame(data=lth.full_data, columns=["date", "time", "name", "content"])
    print(df)

    print((df["name"] == "Keisuke Ogawa").sum())
    print((df["name"] == "Kosuke Takeda").sum())
    print((df["name"] == "又吉康平").sum())
    print(df["date"])
    print(df["date"].value_counts(sort=False))
    vc = df["date"].value_counts().sort_index()
    print(vc)


    font  = fm.FontProperties(fname="/System/Library/Fonts/ヒラギノ角ゴシック W2.ttc")
    rcParams["font.family"] = font.get_name()
   
    
    width=0.3
    #for year in ('2016', '2017', '2018', '2019', '2020'):
    hist_data = {}
    for name in ('Keisuke Ogawa', 'Kosuke Takeda', '又吉康平'):
        df_all = df[ df['name'] == name ]
      
        list_ = []
        for year in ('2016', '2017', '2018', '2019', '2020' ):
            list_.append( len( df_all[ df['date'].str.startswith(year) ] ) )

        hist_data[name] = list_

        #df_all["date"].hist(bins=5, histtype="step", label='{}'.format(name))
        #df_all["name"].value_counts().plot(kind='bar', label='{}'.format(year))
        
        plt.plot(['2016','2017','2018','2019','2020'], hist_data[name], label=name)
   
    print(hist_data)
    plt.grid(False)
    plt.legend()
    plt.savefig("name.png", dpi=300)
    plt.yscale('log')
    plt.legend()
    plt.savefig("name_log.png", dpi=300)

    exit(1)



    for year in ('20', ):

        df_ogawa     = df[ ( df["name"] == 'Keisuke Ogawa') & ( df['date'].str.contains(year) ) ]
        df_takeda    = df[ ( df["name"] == 'Kosuke Takeda') & ( df['date'].str.contains(year) ) ]
        df_matayoshi = df[ ( df["name"] == '又吉康平'     ) & ( df['date'].str.contains(year) ) ]
        
        data_ogawa     = df_ogawa["date"]    .value_counts().sort_index()
        data_takeda    = df_takeda["date"]   .value_counts().sort_index()
        data_matayoshi = df_matayoshi["date"].value_counts().sort_index()
        
        data_merged    = pd.concat([data_ogawa, data_takeda, data_matayoshi], axis=1)
        df_merged = pd.DataFrame({'Ogawaman': data_ogawa, 'Takeda': data_takeda, 'Matayo' : data_matayoshi})
    
        fig, axis = plt.subplots(figsize=(45,20))
        fig.subplots_adjust(bottom=0.2, top=0.9)

        df_merged.plot(
                ax=axis,
                kind='bar', 
                width=1.0, 
                stacked=True,
                )
    
        plt.xticks(fontproperties=font)
        plt.yticks(fontproperties=font)

        #axis.set_xlabel('日時'  , fontproperties=font, fontsize=40)
        axis.set_ylabel('発   言   数', fontproperties=font, fontsize=40, rotation=90)
        axis.set_title('LINEテキスト分析', fontproperties=font,fontsize=50)
        #axis.tick_params(axis='x', rotation=45, labelsize=12)

        xlabels = []
        isFirst = True
        duration = 0
        for row in df.itertuples():
            if isFirst : 
                xlabels.append(row[1])
                isFirst = False

            elif prev_date != row[1] : 
                duration += 1
                if duration == 10 :
                    xlabels.append(row[1])
                    duration =0 
                else : 
                    xlabels.append('')
            
            prev_date = row[1]

        axis.tick_params(axis='x', labelsize=25)
        axis.tick_params(axis='y', labelsize=30)
        axis.set_xticklabels(xlabels, rotation=45, ha='right')
        
        plt.legend(fontsize=50)
        fig.savefig("hist_{}.png".format(year), dpi=300)

