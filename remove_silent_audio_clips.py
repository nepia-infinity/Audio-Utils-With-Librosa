import librosa
import os
from datetime import datetime
import matplotlib.pyplot as plt



def rename_file(audio_file_path):
    """
    音声ファイルの作成日時を取得し、ファイル名を変更する関数

    Args:
        audio_file_path (str): 音声ファイルのパス
    """

    try:
        # macOSの場合、os.statを使って作成日時を取得
        stat = os.stat(audio_file_path)
        try:
            creation_timestamp = stat.st_birthtime
        except AttributeError:
            # st_birthtimeが存在しない場合は、最終更新時刻を使用
            creation_timestamp = stat.st_mtime

        # Unixタイムスタンプをdatetimeオブジェクトに変換
        creation_datetime = datetime.fromtimestamp(creation_timestamp)

        # 新しいファイル名を生成
        new_filename = f"voiceover_{creation_datetime.strftime('%Y%m%d_%H%M')}.wav"

        # ファイル名を変更
        new_file_path = os.path.join(os.path.dirname(audio_file_path), new_filename)
        os.rename(audio_file_path, new_file_path)

        print(f"Renamed '{audio_file_path}' to '{new_file_path}'")

    except OSError as e:
        print(f"Error renaming file: {e}")



def show_graph(audio_data, sampling_rate):
    """
    音声データを波形グラフとして表示する関数

    Args:
        audio_data (numpy.ndarray): 音声データ
        sampling_rate (int): サンプリングレート
    """

    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(audio_data, sr=sampling_rate)
    plt.title('Audio waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()



def main():
    # 音声ファイルのパスを指定
    file = '/Users/Tsubasa/Desktop/python/sample_audio_files/voiceover_20240817_2009.wav' 

    # librosaを使って音声ファイルを読み込む
    audio_data, sampling_rate = librosa.load(file)
    print(f'audio_data shape: {audio_data.shape}, sampling_rate: {sampling_rate}')

    # 読み込んだデータの情報を確認
    duration = librosa.get_duration(y=audio_data, sr=sampling_rate)
    print(f'再生時間: {round(duration)}秒')

    # audioファイルをリネームする
    rename_file(file)

    # 音声データを可視化
    show_graph(audio_data, sampling_rate)

if __name__ == "__main__":
    main()