@echo off
REM 检查并安装依赖
pip install -r requirements.txt

REM 启动 data_fetcher.py 并将日志输出到 data_fetcher.log 文件
start /B python data_fetcher.py > data_fetcher.log 2>&1

REM 运行 c2dglab.py 并输出其日志到当前窗口
python c2dglab.py

REM 暂停，等待用户按任意键继续
pause