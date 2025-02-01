#!/bin/bash

# 启动 data_fetcher.py 在后台运行，并丢弃其输出
python3 data_fetcher.py > /dev/null 2>&1 &

# 运行 c2dglab.py 并输出其日志到当前终端
python3 c2dglab.py

# 等待用户按 Enter 键继续
read -p "Press Enter to continue..."