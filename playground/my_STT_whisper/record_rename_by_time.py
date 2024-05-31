import subprocess
import os
import shutil
from datetime import datetime
import sys


def get_media_creation_date(file_path):
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format_tags=creation_time",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]
    result = subprocess.run(cmd, text=True, capture_output=True)
    # 将字符串转换为 datetime 对象
    try:
        media_creation_date = datetime.strptime(
            result.stdout.strip(), "%Y-%m-%dT%H:%M:%S.%fZ"
        )
    except ValueError:
        print(f"Error: Invalid date format: {result.stdout.strip()}")
        return None

    return media_creation_date


def are_files_identical(file1, file2):
    """比较两个文件内容是否完全一致."""
    # 首先比较文件大小
    if os.path.getsize(file1) != os.path.getsize(file2):
        return False

    # 逐块比较字节流
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        while True:
            chunk1 = f1.read(4096)  # 每次读取 4KB
            chunk2 = f2.read(4096)
            if chunk1 != chunk2:
                return False
            if not chunk1:  # 文件读取完毕
                break
    return True


def rename_and_copy_files(source_folder, destination_folder):
    """
    重命名并复制音频文件，根据文件重名情况和内容是否相同进行处理。

    Args:
        source_folder (str): 源文件夹路径。
        destination_folder (str): 目标文件夹路径。
    """
    # 初始化文件夹和计数器
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    error_folder = os.path.join(destination_folder, "error")
    if not os.path.exists(error_folder):
        os.makedirs(error_folder)
    copied_count = 0
    renamed_count = 0
    duplicate_count = 0
    error_count = 0
    same_name_count = 0

    for filename in os.listdir(source_folder):
        if filename.endswith((".m4a", ".mp3", ".wav", ".flac")):
            source_file = os.path.join(source_folder, filename)
            media_creation_date = get_media_creation_date(source_file)

            if media_creation_date:
                new_filename = (
                    media_creation_date.strftime("%Y-%m-%dT%H_%M_%S")
                    + os.path.splitext(filename)[1]
                )
                destination_file = os.path.join(destination_folder, new_filename)

                # 文件名已存在
                if os.path.exists(destination_file):
                    # 文件内容相同，跳过
                    if are_files_identical(source_file, destination_file):
                        print(f"Skipping duplicate file: {filename}")
                        duplicate_count += 1
                    # 文件内容不同，文件名添加 "_1" 后缀
                    else:
                        new_filename = (
                            media_creation_date.strftime("%Y-%m-%dT%H_%M_%S")
                            + "_1"
                            + os.path.splitext(filename)[1]
                        )
                        destination_file = os.path.join(
                            destination_folder, new_filename
                        )

                        shutil.copy2(source_file, destination_file)
                        same_name_count += 1
                        copied_count += 1
                        print(f"Copied and renamed: {filename} -> {new_filename}")
                # 文件名不存在，直接复制
                else:
                    shutil.copy2(source_file, destination_file)
                    copied_count += 1
                    print(f"Copied and renamed: {filename} -> {new_filename}")
            # 无法获取创建日期，移动到 error 文件夹
            else:
                print(
                    f"Media creation date not found for {filename}, moving to error folder."
                )
                shutil.copy2(source_file, os.path.join(error_folder, filename))
                error_count += 1

    print("\n----- Statistics -----")
    print(f"Successfully copied and renamed: {copied_count}")
    print(f"Files renamed due to same name: {renamed_count}")
    print(f"Files with same name after renaming: {same_name_count}")
    print(f"Skipped duplicate files: {duplicate_count}")
    print(f"Files with errors: {error_count}")


if __name__ == "__main__":

    if len(sys.argv) == 3:
        source_directory = sys.argv[1]
        destination_directory = sys.argv[2]
    else:

        current_directory = os.path.dirname(os.path.abspath(__file__))
        source_directory = os.path.join(current_directory, "source")
        destination_directory = os.path.join(current_directory, "renamed")
        if not os.path.exists(source_directory):
            print("Error: 'source' directory does not exist in the current directory.")
            print("Usage: python script.py <source_directory> <destination_directory>")
            print(
                "Or place the source files in a directory named 'source' in the current directory."
            )
            sys.exit(1)

    rename_and_copy_files(source_directory, destination_directory)
