import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

#メイン関数
def FFT_main(t, x, dt):
    sp_data = data_sp(t, x)
    FFT_list = []
    for data_count in sp_data:
        FFT_count = FFT(data_count, dt)
        FFT_list.append(FFT_count)
    fq_ave = FFT_list[0][0]
    PS_ave = np.zeros(len(fq_ave))
    for i in range(len(FFT_list)):
        PS_ave = PS_ave + FFT_list[i][1]
    PS_ave = PS_ave/(i+1)
    plot_FFT(t, x, fq_ave, PS_ave)
    return fq_ave, PS_ave

filepath = "竹鼻立原町 3.wav"
data, samplerate = sf.read(filepath)
n = len(data)
t = np.linspace(0, n / samplerate ,n)
dt = 1 / samplerate
FFT_main(t, data, dt)

#窓関数をかけた後にフーリエ変換を行う関数
def FFT(data_input, dt):
    N = len(data_input[0])
    window = data_input * np.hanning(N)
    F = np.fft.fft(window)
    F_abs = np.abs(F)
    AS = F_abs / N * 2
    PS = AS ** 2
    fq = np.linspace(0, 1.0 / dt ,N)
    PS = 1/(sum(np.hanning(N)) / N) * PS
    fq = fq[:int(N/2)+1]
    PS = PS[:int(N/2)+1]
    return [fq, PS]

#フーリエ変換後のPSをグラフに抽出する関数
def plot_FFT(t, x, fq, PS):
    fig = plt.figure(figsize=(16, 6))
    ax2 = fig.add_subplot(121)
    plt.plot(t, x)
    plt.xlabel("time[s]")
    plt.ylabel("signal amplitude")
    plt.title("time domain")
    ax2 = fig.add_subplot(122)
    plt.plot(fq, PS)
    plt.xlabel('frequency[Hz]')
    plt.ylabel('power spectrum')
    plt.title('frequency domain')
    plt.savefig('VA sound.png', dpi=300)
    PS_simp = PS[:-1]
    fq_simp = fq[-1]

print(data.shape)
print(samplerate)
print(n)
print(t)
print(dt)
plt.show


