# encoding: utf-8
import soundfile as sf
import numpy as np

x, Fs = sf.read("speech.wav")   # 音声データとサンプリング周波数の読み込み
Len = len(x)                    # 信号の長さ

##################
#  遅延量の設定  #
##################
D = 16                          # 遅延量

##################################
#  入力信号に正弦波ノイズを付加  #
##################################
for i in range(1,8):            # 入力信号に正弦波ノイズを付加
    w = 2*np.pi*i/D
    x = x + 0.1*np.sin(w*np.arange(0,Len)); 

####################
#  フィルタリング  #
####################
y = np.zeros(Len)               # 出力信号の初期化
for n in range(D, Len):         # メインループ
    y[n] = 0.5*(x[n]-x[n-D])    # コムフィルタ出力 y(n)

# 16ビットのwavファイルとして書き出す
sf.write("input.wav", x, Fs, format="WAV", subtype="PCM_16") 
sf.write("output.wav", y, Fs, format="WAV", subtype="PCM_16") 

