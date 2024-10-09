# encoding: utf-8
import soundfile as sf
import numpy as np

x, Fs = sf.read("speech.wav")   # �����f�[�^�ƃT���v�����O���g���̓ǂݍ���
Len = len(x)                    # �M���̒���

##################
#  �x���ʂ̐ݒ�  #
##################
D = 16                          # �x����

##################################
#  ���͐M���ɐ����g�m�C�Y��t��  #
##################################
for i in range(1,8):            # ���͐M���ɐ����g�m�C�Y��t��
    w = 2*np.pi*i/D
    x = x + 0.1*np.sin(w*np.arange(0,Len)); 

####################
#  �t�B���^�����O  #
####################
y = np.zeros(Len)               # �o�͐M���̏�����
for n in range(D, Len):         # ���C�����[�v
    y[n] = 0.5*(x[n]-x[n-D])    # �R���t�B���^�o�� y(n)

# 16�r�b�g��wav�t�@�C���Ƃ��ď����o��
sf.write("input.wav", x, Fs, format="WAV", subtype="PCM_16") 
sf.write("output.wav", y, Fs, format="WAV", subtype="PCM_16") 

