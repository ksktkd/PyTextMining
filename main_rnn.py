import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from keras.preprocessing.text     import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

from LineTextHelper import LineTextHelper
import MeCab

if __name__ == '__main__':
    # ---------------------------------------------
    #  Text pre-processing
    # ---------------------------------------------
    lth = LineTextHelper('./line_pomatti.txt')
    df_data = pd.DataFrame(data=lth.get_full_data(), columns=['date','time','name','text'])
    df_data = df_data.drop(columns='date', axis=1)
    df_data = df_data.drop(columns='time', axis=1)
    
    mecab = MeCab.Tagger('-Owakati')
    df_data['text_mecab'] = df_data.apply(lambda x: mecab.parse(str(x['text'])).replace('\n',''), axis=1 )
    
    df_data['category'] = df_data.apply(lambda x: 0 if x['name'] == 'Keisuke Ogawa' else 1 if x['name'] == 'Kosuke Takeda' else 2, axis=1 )
    
    # ---------------------------------------------
    #  split test/train data 
    # ---------------------------------------------
    x_train, x_test, y_train, y_test = train_test_split(
            df_data[['text_mecab']],     # train data 
            df_data[['category']], # test  data 
            test_size=0.2, 
            random_state=0 )
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(x_train['text_mecab'])
    ## save tokenizer object
    with open("tokenizer.pickle", 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(x_test)

    x_train = tokenizer.texts_to_sequences(x_train['text_mecab'])
    x_test  = tokenizer.texts_to_sequences(x_test['text_mecab'])
    
    # 1メッセージの最大単語数 (不足分はパディング)
    x_train = pad_sequences(x_train, maxlen=100)
    x_test  = pad_sequences(x_test, maxlen=100)
    
    # ---------------------------------------------
    # RNN LSTM model
    # ---------------------------------------------
    
    vocabulary_size = len(tokenizer.word_index) + 1  # 学習データの語彙数+1
    
    model = Sequential()
    model.add(Embedding(input_dim=vocabulary_size, output_dim=32))
    model.add(LSTM(16, return_sequences=False))
    model.add(Dense(1, activation='softmax'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    model.summary()
    
    # テストデータの設定
    y_train = y_train['category'].values
    y_test  = y_test['category'].values
    
    # Training
    history = model.fit(
        x_train, 
        y_train, 
        batch_size=32, 
        epochs=10,
        validation_data=(x_test, y_test)
    )
    
    model.save('pomatti_model.h5')
    #
    #plt.figure()
    #plt.plot(history.history['acc'])
    #plt.plot(history.history['val_acc'])
    #plt.legend(['Train', 'Test'], loc='upper left')
    #plt.savefig("acc.png")
    #
    #plt.figure()
    #plt.plot(history.history['loss'])
    #plt.plot(history.history['val_loss'])
    #plt.legend(['Train', 'Test'], loc='upper left')
    #plt.savefig("loss.png")
    
    
    #y_pred = model.predict_classes(x_test)
    #
    #print(confusion_matrix(y_test, y_pred))
    #print(x_test[y_test > y_pred.reshape(-1)]['text'])
    #print(x_test[y_test < y_pred.reshape(-1)]['text'])
