# data_fetcher.py

import requests
import time
import global_vars  # 导入全局变量模块

# 目标 URL
indicators_url = "http://localhost:8111/indicators"

# 重复执行的间隔时间（秒）
interval = 0.1  # 每 0.1 秒执行一次

def fetch_indicators_data():
    """从 localhost:8111/indicators 提取 crew_total, crew_current, driver_state, gunner_state"""
    try:
        # 发送 GET 请求
        response = requests.get(indicators_url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析 JSON 数据
        data = response.json()

        # 提取 crew_total, crew_current, driver_state, gunner_state
        crew_total = data.get("crew_total")
        crew_current = data.get("crew_current")
        driver_state = data.get("driver_state")
        gunner_state = data.get("gunner_state")

        if (
            crew_total is not None
            and crew_current is not None
            and driver_state is not None
            and gunner_state is not None
        ):
            print(
                f"Extracted crew_total: {crew_total}, crew_current: {crew_current}, "
                f"driver_state: {driver_state}, gunner_state: {gunner_state}"
            )
            return crew_total, crew_current, driver_state, gunner_state
        else:
            print("Missing required fields in the JSON data.")
            return None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from indicators: {e}")
        return None, None, None, None
    except ValueError as e:
        print(f"Error parsing JSON from indicators: {e}")
        return None, None, None, None

def update_crew_deal(crew_total, crew_current):
    """更新全局变量 crew_deal 并写入文件"""
    if crew_total is not None and crew_current is not None:
        # 计算 crew_deal
        crew_deal = crew_total - crew_current
        global_vars.crew_deal = crew_deal  # 更新全局变量
        print(f"Updated crew_deal: {crew_deal}")

        # 计算 s_a 和 s_b
        global_vars.s_a = global_vars.base_s + global_vars.cd_a * crew_deal + global_vars.vehicles_deal * global_vars.vd_a
        global_vars.s_b = global_vars.base_s + global_vars.cd_b * crew_deal + global_vars.vehicles_deal * global_vars.vd_b

        # 将更新后的值写入 global_vars.py
        with open("global_vars.py", "w") as f:
            f.write(f"crew_deal = {crew_deal}\n")
            f.write(f"vehicles_deal = {global_vars.vehicles_deal}\n")
            f.write(f"s_a = {global_vars.s_a}\n")
            f.write(f"s_b = {global_vars.s_b}\n")
            f.write(f"base_s = {global_vars.base_s}\n")
            f.write(f"cd_a = {global_vars.cd_a}\n")
            f.write(f"cd_b = {global_vars.cd_b}\n")
            f.write(f"vd_a = {global_vars.vd_a}\n")
            f.write(f"vd_b = {global_vars.vd_b}\n")
    else:
        print("Failed to extract crew data.")

def update_vehicles_deal(driver_state, gunner_state):
    """更新全局变量 vehicles_deal 并写入文件"""
    if driver_state is not None and gunner_state is not None:
        # 判断条件：driver_state 和 gunner_state 均为 1，且 crew_deal 为 0
        if driver_state == 1 and gunner_state == 1 and global_vars.crew_deal == 0:
            vehicles_deal = 1
        else:
            vehicles_deal = 0
        global_vars.vehicles_deal = vehicles_deal  # 更新全局变量
        print(f"Updated vehicles_deal: {vehicles_deal}")

        # 计算 s_a 和 s_b
        global_vars.s_a = global_vars.base_s + global_vars.cd_a * global_vars.crew_deal + vehicles_deal * global_vars.vd_a
        global_vars.s_b = global_vars.base_s + global_vars.cd_b * global_vars.crew_deal + vehicles_deal * global_vars.vd_b

        # 将更新后的值写入 global_vars.py
        with open("global_vars.py", "w") as f:
            f.write(f"crew_deal = {global_vars.crew_deal}\n")
            f.write(f"vehicles_deal = {vehicles_deal}\n")
            f.write(f"s_a = {global_vars.s_a}\n")
            f.write(f"s_b = {global_vars.s_b}\n")
            f.write(f"base_s = {global_vars.base_s}\n")
            f.write(f"cd_a = {global_vars.cd_a}\n")
            f.write(f"cd_b = {global_vars.cd_b}\n")
            f.write(f"vd_a = {global_vars.vd_a}\n")
            f.write(f"vd_b = {global_vars.vd_b}\n")
    else:
        print("Failed to extract driver_state or gunner_state.")

# 主逻辑
def run_data_fetcher():
    try:
        while True:
            # 获取数据
            crew_total, crew_current, driver_state, gunner_state = fetch_indicators_data()

            # 更新 crew_deal
            update_crew_deal(crew_total, crew_current)

            # 更新 vehicles_deal
            update_vehicles_deal(driver_state, gunner_state)

            # 等待指定时间后再次执行
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Data fetcher stopped by user.")

if __name__ == "__main__":
    run_data_fetcher()