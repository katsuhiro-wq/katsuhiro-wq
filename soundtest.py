import librosa
import matplotlib.pyplot as plt
import numpy as np

# 音声ファイルの読み込み
y, sr = librosa.load('audio.wav')  # y: 音声データ, sr: サンプリングレート

# スペクトログラムの計算
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)

# デシベルに変換
log_S = librosa.power_to_db(S, ref=np.max)

# スペクトログラムの表示
plt.figure(figsize=(10, 4))
librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel spectrogram')
plt.tight_layout()
plt.show()