# encoding: utf-8
import soundfile as sf
import numpy as np

x, Fs = sf.read("speech.wav")   # 音声データとサンプリング周波数の読み込み
Len = len(x)                    # 信号の長さ

###############
#  FFTの設定  #
###############
N  = 512                        # フレームの長さ
Sft= int(N/2)                   # フレームシフト
FL = 1000                       # 低域側周波数[Hz]
FH = 3000                       # 高域側周波数[Hz]
KL = int(FL/Fs*N)               # 低域側の周波数番号
KH = int(FH/Fs*N)               # 高域側の周波数番号
w  = np.hanning(N)              # 窓関数(ハン窓)
####################
#  フィルタリング  #
####################
y = np.zeros(Len)               # 出力信号の初期化
for n in range(0, Len-N, Sft):  # メインループ
    xin = w*x[n:n+N]            # 入力信号の切り出し
    X   = np.fft.rfft(xin)      # FFT（対称性は自動作成）
    Y   = X                     # 出力スペクトルの初期化
    Y[0:KL]=0                   # 低域側をカット
    Y[KH: ]=0                   # 高域側をカット
    y[n:n+N] = y[n:n+N]+np.fft.irfft(Y) # 出力 y(n)

# 16ビットのwavファイルとして書き出す
sf.write("input.wav", x, Fs, format="WAV", subtype="PCM_16") 
sf.write("output.wav", y, Fs, format="WAV", subtype="PCM_16") 

