import os
from pydub import AudioSegment
import nltk
from nltk.tokenize import sent_tokenize
from pocketsphinx import AudioFile, get_model_path

# iPhoneから取り込んだ音声ファイルのパス (.m4a)
audio_file_path_m4a = "gijiroku.m4a"
# 変換後の音声ファイルのパス (.wav)
audio_file_path_wav = "temp.wav"

# .m4aを.wavに変換する関数
def convert_m4a_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="m4a")
    audio.export(output_path, format="wav")

# 音声ファイルを文字起こしする関数
def transcribe_audio(file_path):
    # PocketSphinx用のオーディオファイル設定
    audio_config = {
        'audio_file': file_path,
        'buffer_size': 2048,
        'no_search': False,
        'full_utt': False,
        'hmm': os.path.join(get_model_path(), 'en-us'),
        'lm': os.path.join(get_model_path(), 'en-us.lm.bin'),
        'dict': os.path.join(get_model_path(), 'cmudict-en-us.dict')
    }
    
    audio = AudioFile(**audio_config)
    transcription = ""
    for phrase in audio:
        transcription += phrase
    
    return transcription

# テキストを分割して議事録の形式に整える関数
def create_minutes(transcription):
    sentences = sent_tokenize(transcription)
    minutes = "議事録\n\n"
    for i, sentence in enumerate(sentences):
        minutes += f"{i + 1}. {sentence}\n"
    return minutes

# .m4aを.wavに変換
convert_m4a_to_wav(audio_file_path_m4a, audio_file_path_wav)

# 音声ファイルを文字起こし
transcription = transcribe_audio(audio_file_path_wav)

# 議事録を作成
minutes = create_minutes(transcription)

# 議事録をファイルに保存
output_file_path = "path/to/output/minutes.txt"
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(minutes)

print("議事録が作成されました。")
