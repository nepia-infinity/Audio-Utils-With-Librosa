import os
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import butter, lfilter



def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
    ローパスフィルタを適用する関数

    Args:
        data (numpy.ndarray): 音声データ
        cutoff (float): カットオフ周波数
        fs (int): サンプリング周波数
        order (int): フィルタの次数（デフォルトは5）

    Returns:
        numpy.ndarray: フィルタ適用後の音声データ
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)



def get_audio_files(dir_path):
  """
  指定されたディレクトリ内の音声ファイルをリスト化する関数

  Args:
      dir_path (str): ディレクトリのパス

  Returns:
      list: 音声ファイルのパスリスト
  """

  audio_files = []
  for filename in os.listdir(dir_path):
      if filename.endswith(('.wav', '.mp3', '.aac')):  # 拡張子でフィルタリング
          file_path = os.path.join(dir_path, filename)
          audio_files.append(file_path)
  return audio_files



def trim_silence(audio_file_path, output_dir):
    """
    音声ファイルの無音部分をトリミングする関数

    Args:
        audio_file_path (str): 音声ファイルのパス
        output_dir (str): 出力先のディレクトリ
    """

    try:
        # 音声ファイルを読み込む
        audio_data, sampling_rate = librosa.load(audio_file_path, sr=None)

         # 低周波フィルタリングを適用
        cutoff = 3000  # カットオフ周波数を指定（例: 3000 Hz）
        audio_data_filtered = butter_lowpass_filter(audio_data, cutoff, sampling_rate)

        # 無音部分をトリミング
        audio_data_trimmed, index = librosa.effects.trim(audio_data, top_db=15)

        # トリミングした部分に元の無音を確認
        margin_duration = 0.02
        start_margin = max(0, index[0] - int(margin_duration * sampling_rate))  # トリミング開始位置にマージン
        end_margin = min(len(audio_data), index[1] + int(margin_duration * sampling_rate))  # 終了位置にマージン

        # 音声データをトリミング後の範囲に拡張
        audio_data_with_margin = audio_data[start_margin:end_margin]

        # 出力ファイルパスを生成
        base_filename = os.path.splitext(os.path.basename(audio_file_path))[0]
        output_file_path = os.path.join(output_dir, f"{base_filename}_trimmed.wav")

        # マージン追加後の音声データを保存
        sf.write(output_file_path, audio_data_with_margin, sampling_rate)

        print(f"無音部分の削除に成功しました。 '{audio_file_path}' そして、'{output_file_path}'として保存されました！！")

    except Exception as e:
        print(f"むむ、エラーが発生したようでごわす {audio_file_path}: {e}")

        
def main():
    # 音声ファイルのパスを指定
    dir_path = '/Users/Tsubasa/Desktop/librosa/original_voice_record'
    output_dir = '/Users/Tsubasa/Desktop/librosa/trimmed_voice_record'
    audio_files = get_audio_files(dir_path)

    # 処理件数をカウントする変数を初期化
    processed_count = 0 

    # 音声ファイルから無音を削除する
    for file in audio_files: 
        print(file)
        trim_silence(file, output_dir)
        processed_count += 1 

    print(f'{processed_count}件の処理が完了しましたッ！！')

if __name__ == "__main__":
    main()