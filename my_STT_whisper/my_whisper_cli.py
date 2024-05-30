import sys
import subprocess
import os


def transcribe_directory(
    directory, model="medium", device="cuda", output_formats=["txt", "srt", "vtt"]
):
    # 拼接输出格式参数
    format_string = ",".join(output_formats)

    # 初始化命令行基本命令
    command = [
        "whisper",
        "--model",
        model,
        "--device",
        device,
        "--output_dir",
        directory,
        "--output_format",
        format_string,
        "--verbose",
        "True",
    ]

    # 遍历目录中的所有音频文件
    for filename in os.listdir(directory):
        if filename.endswith(".m4a"):
            filepath = os.path.join(directory, filename)
            # 将音频文件路径添加到命令中
            complete_command = command + [filepath]
            # 执行命令
            subprocess.run(complete_command, check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        source_directory = os.path.realpath(input_path)  # 使用 realpath 处理路径
    else:
        source_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"源目录: {source_directory}")
    input("按 Enter 键继续, 按 Ctrl+C 退出...")
    transcribe_directory(source_directory)
