import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from gcc_phat import gcc_phat


# 读取.wav文件的函数
def read_wav(file_path):
    sample_rate, data = wavfile.read(file_path)
    if data.ndim != 2:  # 确保是立体声
        raise ValueError("The audio file is not stereo.")
    return sample_rate, data


# 计算TDOA的函数
def calculate_tdoa(signal_left, signal_right, sample_rate):
    tau, _ = gcc_phat(signal_left, signal_right, fs=sample_rate)
    return tau


# 主函数
def main():
    # 生成音频文件名列表
    num_files = 140
    audio_files = [f'audio/ex_xie_{i}.wav' for i in range(1, num_files + 1)]
    tdoas = []  # 存储每段音频的TDOA

    for file_path in audio_files:
        try:
            sample_rate, data = read_wav(file_path)
            left_channel = data[:, 0]  # 左声道
            right_channel = data[:, 1]  # 右声道

            # 计算TDOA
            tdoa = calculate_tdoa(left_channel, right_channel, sample_rate)
            tdoas.append(tdoa)
            print(f"The TDOA for {file_path} is: {tdoa} seconds")

            # 将结果写入文件
            with open('tdoa_results.txt', 'a') as f:  # 'a' 模式表示追加模式
                f.write(f"{tdoa},\n")  # 同时写入文件名和TDOA值

        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    # 绘制TDOA折线图
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, len(tdoas) + 1), tdoas, marker='o', linestyle='-')
    plt.title('TDOA Across Audio Files')
    plt.xlabel('File Index')
    plt.ylabel('TDOA (seconds)')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()