# -*- coding: utf-8 -*-
import requests
import logging

# 配置日志记录
logging.basicConfig(filename='attendance_log.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_kq_info(headers, url_get_info):
    """
    发送GET请求获取签到信息，并将日志记录到文件。
    """
    try:
        logging.info("开始获取签到信息...")
        response_get_info = requests.get(url_get_info, headers=headers)
        if response_get_info.status_code == 200:
            data_get_info = response_get_info.json()
            if isinstance(data_get_info, dict):  # 确保返回的是字典
                # 提取返回的data部分
                kq_obj = data_get_info.get('data', {})
                logging.info(f"成功获取签到信息：{data_get_info}")
                return kq_obj
            else:
                logging.error(f"返回的数据格式不是字典：{data_get_info}")
                return None
        else:
            logging.error(f"GET 请求失败，状态码：{response_get_info.status_code}")
            return None
    except Exception as e:
        logging.error(f"获取签到信息时发生错误: {str(e)}")
        return None

def post_sign_kq(headers, url_sign, kq_obj):
    """
    发送POST请求进行签到，并将日志记录到文件。
    """
    try:
        # 将 kq_obj 封装为 {"kq_obj": kq_obj} 的格式
        post_data = {
            "kq_obj": kq_obj
        }
        logging.info(f"开始进行签到，发送数据：{post_data}")
        response_sign = requests.post(url_sign, headers=headers, json=post_data)
        if response_sign.status_code == 200:
            logging.info(f"签到成功，返回数据：{response_sign.json()}")
        else:
            logging.error(f"POST 请求失败，状态码：{response_sign.status_code}")
    except Exception as e:
        logging.error(f"签到时发生错误: {str(e)}")

def main():
    # 定义URL
    url_get_info = 'http://sdapp.sandau.edu.cn:8669/kq/kqxx/get_kq_info_kcb/'
    url_sign = 'http://sdapp.sandau.edu.cn:8669/kq/kqxx/sign_kq'

    # 从 auth_token.txt 文件中读取 Authorization
    try:
        with open('auth_token.txt', 'r') as file:
            auth_token = file.read().strip()  # 去掉可能的换行符或空白字符
    except FileNotFoundError:
        logging.error("auth_token.txt 文件未找到，无法继续执行签到任务。")
        return

    # 构造请求头
    headers = {
        'Host': 'sdapp.sandau.edu.cn:8669',
        'Origin': 'http://sdapp.sandau.edu.cn:8667',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 cpdaily/9.6.4 wisedu/9.6.4',
        'Authorization': f'Bearer {auth_token}',
        'Referer': 'http://sdapp.sandau.edu.cn:8667/',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }

    logging.info("开始执行签到任务...")

    # Step 1: 获取签到信息
    kq_obj = get_kq_info(headers, url_get_info)

    # Step 2: 如果获取到有效的签到信息，进行签到
    if kq_obj and isinstance(kq_obj, dict):  # 确保 kq_obj 是字典
        if kq_obj.get('info', '') == 'error':
            logging.info("签到信息为 error")
            return
        logging.info("准备进行签到...")
        post_sign_kq(headers, url_sign, kq_obj)
    else:
        logging.error("未能获取到有效的签到信息，无法进行签到。")

# 只有当直接运行该脚本时，才执行 main 函数
if __name__ == '__main__':
    main()
