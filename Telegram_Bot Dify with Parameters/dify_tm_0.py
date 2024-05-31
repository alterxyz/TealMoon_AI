import requests
import json
from datetime import datetime

api_key = "app-xxxxxxxxxxxxxxxxxx"
base_url = "https://api.dify.ai/v1"
endpoint = "/parameters"
summary_file_path = "api_info.json"


def api_info_getter(api_key, base_url, endpoint, summary_file_path):
    url = f"{base_url}{endpoint}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # 获取当前时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = response.json()

        # 创建要存储的数据
        result = {
            "api_key": api_key,
            "base_url": base_url,
            "timestamp": timestamp,
            "response": data,
        }

        # 读取现有文件内容
        try:
            with open(summary_file_path, "r") as file:
                summary_data = json.load(file)
        except FileNotFoundError:
            summary_data = []

        # 追加新的响应内容
        summary_data.append(result)

        # 保存回文件
        with open(summary_file_path, "w") as file:
            json.dump(summary_data, file, indent=4)
    else:
        print(f"Request failed with status code: {response.status_code}")


api_info_getter(api_key, base_url, endpoint, summary_file_path)
