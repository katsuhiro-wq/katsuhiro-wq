# encoding: utf-8
import soundfile as sf
import numpy as np

x, Fs = sf.read("speech.wav")   # �����f�[�^�ƃT���v�����O���g���̓ǂݍ���
Len = len(x)                    # �M���̒���

###############
#  FFT�̐ݒ�  #
###############
N  = 512                        # �t���[���̒���
Sft= int(N/2)                   # �t���[���V�t�g
FL = 1000                       # ��摤���g��[Hz]
FH = 3000                       # ���摤���g��[Hz]
KL = int(FL/Fs*N)               # ��摤�̎��g���ԍ�
KH = int(FH/Fs*N)               # ���摤�̎��g���ԍ�
w  = np.hanning(N)              # ���֐�(�n����)
####################
#  �t�B���^�����O  #
####################
y = np.zeros(Len)               # �o�͐M���̏�����
for n in range(0, Len-N, Sft):  # ���C�����[�v
    xin = w*x[n:n+N]            # ���͐M���̐؂�o��
    X   = np.fft.rfft(xin)      # FFT�i�Ώ̐��͎����쐬�j
    Y   = X                     # �o�̓X�y�N�g���̏�����
    Y[0:KL]=0                   # ��摤���J�b�g
    Y[KH: ]=0                   # ���摤���J�b�g
    y[n:n+N] = y[n:n+N]+np.fft.irfft(Y) # �o�� y(n)

# 16�r�b�g��wav�t�@�C���Ƃ��ď����o��
sf.write("input.wav", x, Fs, format="WAV", subtype="PCM_16") 
sf.write("output.wav", y, Fs, format="WAV", subtype="PCM_16") 

