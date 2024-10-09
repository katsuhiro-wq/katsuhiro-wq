import numpy as np
#import japanize_matplotlib as plt
import matplotlib.pyplot as plt

#タイトルで漢字が使えるようフォントを設定
plt.rcParams['font.family'] = 'Meiryo'

N = 1001 #分割数   1-1節参照
t = np.linspace (0,1,N) # 時間

y1 = 10*np.cos(2*np.pi*10*t+0)  
y2 = 10*np.sin(2*np.pi*20*t+0)  
y3 = 5*np.cos(2*np.pi*40*t+0)  
y4 = 8*np.cos(2*np.pi*5*t+np.pi/2)  

#4波の合成
z=y1+y2+y3+y4
#描画
fig2 = plt.figure(2)#figureウインドウの作成
ax = fig2.add_subplot()#サブプロットの追加
ax.plot(t, z, label = '$z=y1+y2+y3+y4$')#グラフの描画
ax.set_xlabel("時間 t [sec]")#x軸のラベル
ax.set_ylabel("z=y1+y2+y3+y4", )#y軸のラベル
ax.grid()#グラフの中にグリッド（網）を表示する
plt.legend() #凡例の表示
plt.savefig("./Fig2.png") #図の保存

#fftの計算
F = np.fft.fft(z)#fft計算
f =  np.linspace (0,N-1,N)# 周波数
#描画ウインドウの作成
fig3 = plt.figure(3)#figureウインドウの作成
ax = fig3.add_subplot()#サブプロットの追加
ax.plot(f, abs(F), label = '$F=fft(y1+y2+y3+y4)$')#グラフの描画
ax.set_xlabel("周波数 f[Hz]")#x軸のラベル
ax.set_ylabel("FFT演算結果の振幅")#y軸のラベル
ax.grid()#グラフの中にグリッド（網）を表示する
plt.legend() #凡例の表示
plt.savefig("./Fig3.png") #図の保存


#振幅調整
G=abs(F)/N*2#全体のサンプル数で割り、正負に分かれた分を戻す
Nf = int((N-1)/2)#時間データの半分
#描画ウインドウの作成
fig4 = plt.figure(4)#figureウインドウの作成
ax = fig4.add_subplot()#サブプロットの追加
ax.plot(f[0:Nf:1], G[0:Nf:1], label = '$G=abs(F)/N*2')#グラフの描画
ax.set_xlabel("周波数 f[Hz]")#x軸のラベル
ax.set_ylabel("FFT演算結果の振幅調整")#y軸のラベル
ax.grid()#グラフの中にグリッド（網）を表示する
plt.legend() #凡例の表示
plt.savefig("./Fig4.png") #図の保存