# ui.py

import tkinter as tk
from tkinter import ttk, font
import importlib
import global_vars  # 导入全局变量模块
import os

def calculate_values(*args):
    """
    根据输入值更新全局变量
    """
    try:
        # 获取输入值
        base_s_value = float(base_s_entry.get()) if base_s_entry.get() else 0
        cd_a_value = float(cd_a_entry.get()) if cd_a_entry.get() else 0
        cd_b_value = float(cd_b_entry.get()) if cd_b_entry.get() else 0
        vd_a_value = float(vd_a_entry.get()) if vd_a_entry.get() else 0
        vd_b_value = float(vd_b_entry.get()) if vd_b_entry.get() else 0

        # 重新加载 global_vars 模块以获取最新值
        importlib.reload(global_vars)

        # 更新 global_vars 中的 base_s、cd_a、cd_b、vd_a 和 vd_b
        with open("global_vars.py", "w") as f:
            f.write(f"# 全局变量\n")
            f.write(f"crew_deal = {global_vars.crew_deal}\n")
            f.write(f"vehicles_deal = {global_vars.vehicles_deal}\n")
            f.write(f"base_s = {base_s_value}\n")
            f.write(f"cd_a = {cd_a_value}\n")
            f.write(f"cd_b = {cd_b_value}\n")
            f.write(f"vd_a = {vd_a_value}\n")
            f.write(f"vd_b = {vd_b_value}\n")

        # 更新显示
        base_s_label.config(text=f"基础强度")
        cd_a_label.config(text=f"成员死亡数乘区 通道A")
        cd_b_label.config(text=f"成员死亡数乘区 通道B")
        vd_a_label.config(text=f"载具被摧毁强度 通道A")
        vd_b_label.config(text=f"载具被摧毁强度 通道B")
    except ValueError:
        base_s_label.config(text="输入值无效，请检查输入")
        cd_a_label.config(text="成员死亡数乘区 通道A")
        cd_b_label.config(text="成员死亡数乘区 通道B")
        vd_a_label.config(text="载具被摧毁强度 通道A")
        vd_b_label.config(text="载具被摧毁强度 通道B")

# 创建主窗口
root = tk.Tk()
root.title("War Thunder X 郊狼 V3")
root.geometry("400x450")  # 调整窗口大小以适应新增的输入框

# 设置窗口居中对齐
window_width = 400
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 加载自定义字体
try:
    # 使用 tkinter 的 font 模块加载自定义字体
    if os.path.exists("./Ubuntu-R.ttf"):
        # 使用 tkinter 的 font 模块加载字体文件
        custom_font = font.Font(family="Ubuntu", size=12)
        root.tk.call("font", "create", "Ubuntu", "-family", "Ubuntu", "-size", 12, "-file", "Ubuntu-R.ttf")
        custom_font = font.Font(family="Ubuntu", size=12)
    else:
        raise FileNotFoundError("字体文件 Ubuntu-R.ttf 未找到")
except Exception as e:
    print(f"字体加载失败: {e}")
    custom_font = font.Font(size=12)  # 回退到默认字体

# 左侧区域：输入和计算
left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# 第一排：标题
title_label = ttk.Label(left_frame, text="War Thunder X 郊狼 V3", font=("Ubuntu", 16))
title_label.pack(pady=10)

# 第二排：基础强度
base_s_frame = ttk.Frame(left_frame)
base_s_frame.pack(pady=5)

base_s_label = ttk.Label(base_s_frame, text="基础强度", font=custom_font)
base_s_label.pack(side=tk.LEFT, padx=5)

base_s_entry = ttk.Entry(base_s_frame, width=10, font=custom_font)
base_s_entry.insert(0, str(global_vars.base_s))  # 从 global_vars.py 中加载默认值
base_s_entry.pack(side=tk.LEFT, padx=5)
base_s_entry.bind("<KeyRelease>", calculate_values)  # 输入时自动计算

# 第三排：成员死亡数乘区 通道A
cd_a_frame = ttk.Frame(left_frame)
cd_a_frame.pack(pady=5)

cd_a_label = ttk.Label(cd_a_frame, text="成员死亡数乘区 通道A", font=custom_font)
cd_a_label.pack(side=tk.LEFT, padx=5)

cd_a_entry = ttk.Entry(cd_a_frame, width=10, font=custom_font)
cd_a_entry.insert(0, str(global_vars.cd_a))  # 从 global_vars.py 中加载默认值
cd_a_entry.pack(side=tk.LEFT, padx=5)
cd_a_entry.bind("<KeyRelease>", calculate_values)  # 输入时自动计算

# 第四排：成员死亡数乘区 通道B
cd_b_frame = ttk.Frame(left_frame)
cd_b_frame.pack(pady=5)

cd_b_label = ttk.Label(cd_b_frame, text="成员死亡数乘区 通道B", font=custom_font)
cd_b_label.pack(side=tk.LEFT, padx=5)

cd_b_entry = ttk.Entry(cd_b_frame, width=10, font=custom_font)
cd_b_entry.insert(0, str(global_vars.cd_b))  # 从 global_vars.py 中加载默认值
cd_b_entry.pack(side=tk.LEFT, padx=5)
cd_b_entry.bind("<KeyRelease>", calculate_values)  # 输入时自动计算

# 第五排：载具被摧毁强度 通道A
vd_a_frame = ttk.Frame(left_frame)
vd_a_frame.pack(pady=5)

vd_a_label = ttk.Label(vd_a_frame, text="载具被摧毁强度 通道A", font=custom_font)
vd_a_label.pack(side=tk.LEFT, padx=5)

vd_a_entry = ttk.Entry(vd_a_frame, width=10, font=custom_font)
vd_a_entry.insert(0, str(global_vars.vd_a))  # 从 global_vars.py 中加载默认值
vd_a_entry.pack(side=tk.LEFT, padx=5)
vd_a_entry.bind("<KeyRelease>", calculate_values)  # 输入时自动计算

# 第六排：载具被摧毁强度 通道B
vd_b_frame = ttk.Frame(left_frame)
vd_b_frame.pack(pady=5)

vd_b_label = ttk.Label(vd_b_frame, text="载具被摧毁强度 通道B", font=custom_font)
vd_b_label.pack(side=tk.LEFT, padx=5)

vd_b_entry = ttk.Entry(vd_b_frame, width=10, font=custom_font)
vd_b_entry.insert(0, str(global_vars.vd_b))  # 从 global_vars.py 中加载默认值
vd_b_entry.pack(side=tk.LEFT, padx=5)
vd_b_entry.bind("<KeyRelease>", calculate_values)  # 输入时自动计算

# 运行主循环
root.mainloop()