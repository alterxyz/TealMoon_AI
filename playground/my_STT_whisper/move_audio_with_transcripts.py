import os
import shutil
import sys


def move_audio_with_transcripts(source_dir):
    """
    将具有对应 .txt 或 .srt 转录文件的 .m4a 音频文件移动到 "with_transcripts" 子文件夹。

    Args:
        source_dir (str): 源目录的路径。
    """

    # 使用 os.path.join 确保路径拼接正确，即使在不同操作系统上
    subfolder = os.path.join(source_dir, "with_transcripts")

    # 创建子文件夹（如果不存在）
    os.makedirs(subfolder, exist_ok=True)  # 使用 exist_ok=True 避免重复创建文件夹时报错
    count = 0

    # 遍历源目录下的所有文件和文件夹
    for filename in os.listdir(source_dir):
        # 使用 os.path.join 构建完整的文件路径
        file_path = os.path.join(source_dir, filename)

        # 检查是否是文件（而不是文件夹）
        if os.path.isfile(file_path) and filename.endswith(".m4a"):
            base_name = os.path.splitext(filename)[0]
            txt_file = base_name + ".txt"
            srt_file = base_name + ".srt"

            # 检查 .txt 或 .srt 文件是否存在于源目录中
            if any(
                os.path.exists(os.path.join(source_dir, transcript))
                for transcript in [txt_file, srt_file]
            ):
                # 使用 os.path.join 构建目标文件路径
                dest_file_path = os.path.join(subfolder, filename)

                # 移动 .m4a 文件到子文件夹
                shutil.move(file_path, dest_file_path)
                count += 1
                # print(f"已将 {filename} 移动到 {subfolder}")
    print(f"Total {count} files moved to {subfolder}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        source_directory = os.path.realpath(input_path)  # 使用 realpath 处理路径
    else:
        source_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"源目录: {source_directory}")
    input("按 Enter 键继续...")

    move_audio_with_transcripts(source_directory)
