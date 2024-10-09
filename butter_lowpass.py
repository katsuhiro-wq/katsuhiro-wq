import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

# ボイスメモで収録したwavファイルを読み込む
sounds = AudioSegment.from_file('20240406_voicedata0003.wav', 'wav')

# 基本情報の表示
print(f'channel: {sounds.channels}')
print(f'frame rate: {sounds.frame_rate}')
print(f'duration: {sounds.duration_seconds} s')
print(f'sample width: {sounds.sample_width}')

# チャンネルが2 （ステレオ) の場合，交互にデータが入っているので，二つおきに読み出す。
# ただし，今回の場合はモノラルのはず。つまり，sounds.channels = 1
sig = np.array(sounds.get_array_of_samples())[::sounds.channels]
dt = 1.0/sounds.frame_rate # サンプリング時間

# 時間アレイを作る
tms = 0.0 # サンプル開始時間を0にセット
tme = sounds.duration_seconds # サンプル終了時刻
tm = np.linspace(tms, tme, len(sig), endpoint=False) # 時間numpy配列を作成

# DFT
N = len(sig)
X = np.fft.fft(sig)
f = np.fft.fftfreq(N, dt) # Xのindexに対応する周波数のnumpy配列を取得

# ローパスフィルタ
f_cutoff_LPF = 0.02e2 # カットオフ周波数

X_LPFed = X.copy()
X_LPFed[(f > f_cutoff_LPF) | (f < -f_cutoff_LPF)] = 0.0 # カットオフ周波数より大きい周波数成分を0に
sig_LPFed = np.real(np.fft.ifft(X_LPFed))

# 音声データの書き出し
sounds_LPFed = AudioSegment(sig_LPFed.astype("int16").tobytes(), 
                            sample_width=sounds.sample_width, 
                            frame_rate=sounds.frame_rate, channels=1)
sounds_LPFed.export("vasound_LPFed.wav", format="wav")

# ハイパスフィルタ
f_cutoff_HPF = 0.6e2 # カットオフ周波数

X_HPFed = X.copy()
X_HPFed[((f > 0) & (f < f_cutoff_HPF)) | ((f < 0) & (f > -f_cutoff_HPF))] = 0.0 #カットオフ周波数より小さい周波数成分を0に
sig_HPFed = np.real(np.fft.ifft(X_HPFed))

# 音声データの書き出し
sounds_HPFed = AudioSegment(sig_HPFed.astype("int16").tobytes(), 
                            sample_width=sounds.sample_width, 
                            frame_rate=sounds.frame_rate, channels=1)
sounds_HPFed.export("vasound_HPFed.wav", format="wav")

# データをプロット (なくても良い)
fig, (ax01, ax02) = plt.subplots(nrows=2, figsize=(6, 8))
plt.subplots_adjust(wspace=0.0, hspace=0.6)

ax01.set_xlim(tms, tme)
ax01.set_xlabel('time (s)')
ax01.set_ylabel('x')
ax01.plot(tm, sig, color='black') # 入力信号
ax01.plot(tm, sig_LPFed, color='blue') # LPF後の波形
ax01.plot(tm, sig_HPFed, color='orange') # LPF後の波形

ax02.set_xlim(0, 2000)
ax02.set_xlabel('frequency (Hz)')

ax02.set_ylabel('|X|/N')
ax02.plot(f[0:N//2], np.abs(X[0:N//2])/N, color='black') # 振幅スペクトル
ax02.plot(f[0:N//2], np.abs(X_LPFed[0:N//2])/N, color='blue') # 振幅スペクトル
ax02.plot(f[0:N//2], np.abs(X_HPFed[0:N//2])/N, color='orange') # 振幅スペクトル

plt.savefig('va_filter.png', dpi=300)
plt.show()