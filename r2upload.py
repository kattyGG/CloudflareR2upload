#!/usr/bin/env python3
"""
配置部分，请替换为你自己的 Cloudflare R2 信息
"""
ACCESS_KEY = "YOUR_R2_ACCESS_KEY"        # Cloudflare R2 Access Key
SECRET_KEY = "YOUR_R2_SECRET_KEY"        # Cloudflare R2 Secret Key
BUCKET_NAME = "your-bucket-name"         # R2 存储桶名称
ACCOUNT_ID = "your-account-id"           # 你的 Cloudflare 账户 ID
ENDPOINT_URL = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"  # R2 端点 URL

import argparse
import boto3
import os
from botocore.config import Config

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="上传文件到 Cloudflare R2 桶")
    parser.add_argument("-p", "--proxy", help="代理服务器 URL (例如: http://127.0.0.1:8106 或 s5://127.0.0.1:8106)", default=None)
    parser.add_argument("filename", help="要上传的文件")
    args = parser.parse_args()

    # 设置代理配置（如果提供了代理参数，则同时对 http 和 https 使用该代理）
    proxy_config = None
    if args.proxy:
        proxy_config = Config(proxies={
            "http": args.proxy,
            "https": args.proxy
        })

    # 创建 S3 客户端（Cloudflare R2 与 S3 兼容）
    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            config=proxy_config if proxy_config else None
        )
    except Exception as e:
        print("创建 S3 客户端失败:", e)
        return

    # 检查文件是否存在
    if not os.path.isfile(args.filename):
        print(f"文件 '{args.filename}' 不存在。")
        return

    # 上传文件到指定桶中，键名使用文件的 basename
    try:
        print(f"正在上传 {args.filename} 到桶 {BUCKET_NAME} ...")
        s3_client.upload_file(args.filename, BUCKET_NAME, os.path.basename(args.filename))
        print("上传成功！")
    except Exception as e:
        print("上传过程中出错:", e)
    
    # 执行完毕后删除脚本自身（仅执行一次）
    try:
        script_path = os.path.realpath(__file__)
        print("正在删除脚本文件:", script_path)
        os.remove(script_path)
    except Exception as e:
        print("删除脚本时出错:", e)

if __name__ == "__main__":
    main()
