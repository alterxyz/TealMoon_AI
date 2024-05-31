import whisper
import os
import time
from datetime import timedelta
from pydub.utils import mediainfo
import sys

import whisper.utils
from move_audio_with_transcripts import move_audio_with_transcripts as move_a

total_audio_duration = 0
total_transcription_time = 0


def transcribe_audio(file_path, model_size="medium", device="cuda", language="zh"):
    """
    使用 Whisper 模型转录音频文件，并将结果保存为 .txt 和 .srt 文件。

    Args:
        file_path (str): 音频文件的路径。
        model_size (str, optional): Whisper 模型的大小。默认为 "medium"。
        device (str, optional): 使用的设备，可以是 "cuda" 或 "cpu"。默认为 "cuda"。
        language (str, optional): 音频的语言。默认为 "zh" (中文)。
    """
    global total_audio_duration, total_transcription_time

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"Error: 文件 {file_path} 不存在。")
        return

    # 尝试加载 Whisper 模型
    try:
        model = whisper.load_model(model_size, device=device)
    except Exception as e:
        print(f"Error: 无法加载 Whisper 模型：{e}")
        return

    # 获取音频文件的长度
    try:
        audio_info = mediainfo(file_path)
        audio_duration = float(audio_info["duration"])

    except Exception as e:
        print(f"Error: 无法获取音频文件长度：{e}")
        return

    # 开始计时
    start_time = time.time()

    # 转录音频文件
    # print(f"正在使用 Whisper {model_size} 模型在 {device} 上转录 {file_path} ...")
    try:
        result = model.transcribe(file_path, language=language)
    except Exception as e:
        print(f"Error: 转录音频文件时出错：{e}")
        return

    # 结束计时
    end_time = time.time()
    transcription_time = end_time - start_time

    # 计算时间倍数
    time_ratio = audio_duration / transcription_time
    total_audio_duration += audio_duration
    total_transcription_time += transcription_time

    # 使用 whisper.utils 保存转录结果
    output_dir = os.path.dirname(file_path)
    writers = {
        "txt": whisper.utils.WriteTXT(output_dir),
        "srt": whisper.utils.WriteSRT(output_dir),
        "vtt": whisper.utils.WriteVTT(output_dir),
    }
    for ext in writers:
        try:
            writers[ext](result, file_path)
            # print(f"转录结果已保存为 {os.path.splitext(file_path)[0]}.{ext}")
        except Exception as e:
            print(f"Error: 无法保存 .{ext} 文件：{e}")

    # 配置文件名（不包括扩展名）
    # base_name = os.path.splitext(file_path)[0]
    # transcription_text = result["text"]
    # # 保存为 .txt 文件
    # txt_file_path = base_name + ".txt"
    # try:
    #     with open(txt_file_path, "w", encoding="utf-8") as txt_file:
    #         txt_file.write(transcription_text)
    #     # print(f"转录结果已保存为 {txt_file_path}")
    # except Exception as e:
    #     print(f"Error: 无法保存 .txt 文件：{e}")

    # # 生成并保存为 .srt 文件
    # srt_file_path = base_name + ".srt"
    # try:
    #     with open(srt_file_path, "w", encoding="utf-8") as srt_file:
    #         for i, segment in enumerate(result["segments"]):
    #             start_time = segment["start"]
    #             end_time = segment["end"]
    #             text = segment["text"]

    #             start_time_str = format_time(start_time)
    #             end_time_str = format_time(end_time)

    #             srt_file.write(f"{i + 1}\n")
    #             srt_file.write(f"{start_time_str} --> {end_time_str}\n")
    #             srt_file.write(f"{text}\n\n")
    #     # print(f"转录结果已保存为 {srt_file_path}")
    # except Exception as e:
    #     print(f"Error: 无法保存 .srt 文件：{e}")

    # 输出信息
    print(f"{file_path}")
    print(f"耗时: {timedelta(seconds=int(transcription_time))} X{time_ratio:.2f}")


def format_time(seconds):
    """
    将秒转换为 SRT 时间格式。
    """
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def transcribe_all_audios_in_directory(
    directory, model_size="medium", device="cuda", language="zh"
):
    """
    转录指定目录下的所有 m4a 音频文件。
    """

    # 将相对路径转换为绝对路径
    if not os.path.isabs(directory):
        directory = os.path.abspath(directory)
    for file in os.listdir(directory):
        if file.endswith(".m4a"):
            file_path = os.path.join(directory, file)
            transcribe_audio(file_path, model_size, device, language)
    print(f"使用 Whisper {model_size} 模型在 {device} 上转录。")
    print(f"总用时: {timedelta(seconds=int(total_transcription_time))}")
    print(f"平均倍数: {total_audio_duration / total_transcription_time: .2f} X")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        source_directory = os.path.realpath(input_path)  # 使用 realpath 处理路径
    else:
        source_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"源目录: {source_directory}")
    input("按 Enter 键继续, 按 Ctrl+C 退出...")
    transcribe_all_audios_in_directory(source_directory)
    # move_a(source_directory)
