# c2dglab.py

import asyncio
import logging
import pydglab
from pydglab import model_v3
import importlib
import global_vars  # 从 global_vars.py 中导入全局变量

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(module)s [%(levelname)s]: %(message)s",
    level=logging.INFO
)

def map_strength(value):
    """
    将强度值映射到设备的有效范围（0 到 100 的整数）
    """
    if value < 0:
        return 0
    elif value > 100:
        return 100
    return int(value)

async def connect_to_device(dglab_instance):
    """
    尝试连接到设备，如果失败则重试
    """
    retry_count = 0
    max_retries = 5  # 最大重试次数
    retry_delay = 5  # 重试间隔时间（秒）

    while retry_count < max_retries:
        try:
            logging.info("正在连接到 郊狼 3.0...")
            await dglab_instance.create()
            logging.info("成功连接到 郊狼 3.0！")
            return True  # 连接成功
        except Exception as e:
            retry_count += 1
            logging.error(f"连接失败（尝试 {retry_count}/{max_retries}）：{e}")
            if retry_count < max_retries:
                logging.info(f"{retry_delay} 秒后重试...")
                await asyncio.sleep(retry_delay)
            else:
                logging.error("已达到最大重试次数，连接失败。")
                return False  # 连接失败

async def connect_and_set_strength():
    """
    连接到 郊狼 3.0 并持续检测 global_vars 中的 s_a 和 s_b，动态更新通道强度
    """
    # 创建 DGLab 实例
    dglab_instance = pydglab.dglab_v3()
    last_s_a, last_s_b = None, None  # 记录上一次的强度值

    # 尝试连接到设备
    if not await connect_to_device(dglab_instance):
        return  # 连接失败，退出函数

    # 设置波形参数
    try:
        await dglab_instance.set_wave_sync(1, 9, 20, 5, 35, 20)
        logging.info("波形参数设置成功：1, 9, 20, 5, 35, 20")
    except Exception as e:
        logging.error(f"设置波形参数时发生错误: {e}")

    # 主循环：持续检测 s_a 和 s_b 的变化
    while True:
        try:
            # 重新加载 global_vars 模块以获取最新值
            importlib.reload(global_vars)

            # 获取最新的 s_a 和 s_b
            current_s_a = global_vars.s_a
            current_s_b = global_vars.s_b

            # 如果 s_a 或 s_b 发生变化，更新设备强度
            if current_s_a != last_s_a or current_s_b != last_s_b:
                # 映射强度值到设备的有效范围
                mapped_s_a = map_strength(current_s_a)
                mapped_s_b = map_strength(current_s_b)

                # 更新设备强度
                await dglab_instance.set_strength_sync(mapped_s_a, mapped_s_b)
                logging.info(f"更新通道强度：A={mapped_s_a}, B={mapped_s_b}")

                # 更新记录值
                last_s_a, last_s_b = current_s_a, current_s_b

            # 等待 1 秒后再次检测
            await asyncio.sleep(1)

        except Exception as e:
            logging.error(f"检测或更新强度时发生错误: {e}")
            await asyncio.sleep(1)  # 发生错误时等待 1 秒后重试

async def main():
    """
    主函数
    """
    await connect_and_set_strength()

if __name__ == "__main__":
    asyncio.run(main())