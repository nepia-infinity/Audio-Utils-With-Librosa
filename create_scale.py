import librosa
import numpy as np
import soundfile as sf

def create_scale(audio_data, sampling_rate):
  """音階を生成する関数

  Args:
    audio_data: 音源データ (numpy array)
    sampling_rate: サンプリングレート

  Returns:
    音階のデータ (numpy array)
  """
  do = audio_data
  re = librosa.effects.pitch_shift(audio_data, sr=sampling_rate, n_steps=2)
  mi = librosa.effects.pitch_shift(audio_data, sr=sampling_rate, n_steps=4)
  fa = librosa.effects.pitch_shift(audio_data, sr=sampling_rate, n_steps=5)
  sol = librosa.effects.pitch_shift(audio_data, sr=sampling_rate, n_steps=7)
  la = librosa.effects.pitch_shift(audio_data, sr=sampling_rate, n_steps=9)
  ti = librosa.effects.pitch_shift(audio_data, sr=sampling_rate, n_steps=11)
  do_ = librosa.effects.pitch_shift(audio_data, sr=sampling_rate, n_steps=12)

  doremi = np.concatenate((do, re, mi, fa, sol, la, ti, do_))
  return doremi

# 音源を読み込む
audio_data, sampling_rate = librosa.load("boil_louder.wav", duration=0.5)

# 音階を生成
scale_data = create_scale(audio_data, sampling_rate)

# 音階をファイルに保存
sf.write("doremi.wav", scale_data, sampling_rate)
print("END")