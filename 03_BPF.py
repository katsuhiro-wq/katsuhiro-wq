# encoding: utf-8
import soundfile as sf
import numpy as np

x, Fs = sf.read("speech.wav") # �����f�[�^�ƃT���v�����O���g���̓ǂݍ���
Len = len(x)                  # �M���̒���

########################
#  �t�B���^�W���̌v�Z  #
########################
FL = 2000                     # �Ւf���g��(��摤)
FH = 4000                     # �Ւf���g��(���摤)
fL = FL/Fs                    # ���K���Ւf���g��(��摤)
fH = FH/Fs                    # ���K���Ւf���g��(���摤)
wL = 2*np.pi*fL               # ���K���p�Ւf���g��(��摤)
wH = 2*np.pi*fH               # ���K���p�Ւf���g��(���摤)
M  = 200                      # �t�B���^����
h  = np.zeros(M+1)            # �t�B���^�W���̏�����
for m in range(M+1):
    if m==M/2:
        h[m] = (wH-wL)/np.pi  # ���ꂪ0�̂Ƃ��̒l
    else:
        h[m] = wH/np.pi*np.sin(wH*(m-M/2))/(wH*(m-M/2))-wL/np.pi*np.sin(wL*(m-M/2))/(wL*(m-M/2))
han = np.hanning(M+1)         # �n�j���O��
h   = h*han                   # �t�B���^�W���Ƀn�j���O����������

####################
#  �t�B���^�����O  #
####################
y   = np.zeros(Len)           # �o�͐M���̏�����
for n in range(M+1, Len):     # ���C�����[�v
    xin  = x[n:n-M-1:-1]      # ���͐M���̐؂�o��
    y[n] = np.dot(h, xin)     # �t�B���^�o��

# 16�r�b�g��wav�t�@�C���Ƃ��ď����o��
sf.write("output.wav", y, Fs, format="WAV", subtype="PCM_16") 

