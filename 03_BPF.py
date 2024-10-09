# encoding: utf-8
import soundfile as sf
import numpy as np

x, Fs = sf.read("speech.wav") # 音声データとサンプリング周波数の読み込み
Len = len(x)                  # 信号の長さ

########################
#  フィルタ係数の計算  #
########################
FL = 2000                     # 遮断周波数(低域側)
FH = 4000                     # 遮断周波数(高域側)
fL = FL/Fs                    # 正規化遮断周波数(低域側)
fH = FH/Fs                    # 正規化遮断周波数(高域側)
wL = 2*np.pi*fL               # 正規化角遮断周波数(低域側)
wH = 2*np.pi*fH               # 正規化角遮断周波数(高域側)
M  = 200                      # フィルタ次数
h  = np.zeros(M+1)            # フィルタ係数の初期化
for m in range(M+1):
    if m==M/2:
        h[m] = (wH-wL)/np.pi  # 分母が0のときの値
    else:
        h[m] = wH/np.pi*np.sin(wH*(m-M/2))/(wH*(m-M/2))-wL/np.pi*np.sin(wL*(m-M/2))/(wL*(m-M/2))
han = np.hanning(M+1)         # ハニング窓
h   = h*han                   # フィルタ係数にハニング窓をかける

####################
#  フィルタリング  #
####################
y   = np.zeros(Len)           # 出力信号の初期化
for n in range(M+1, Len):     # メインループ
    xin  = x[n:n-M-1:-1]      # 入力信号の切り出し
    y[n] = np.dot(h, xin)     # フィルタ出力

# 16ビットのwavファイルとして書き出す
sf.write("output.wav", y, Fs, format="WAV", subtype="PCM_16") 

