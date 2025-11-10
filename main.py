#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chatgpt_help.py
----------------
一個利用反射（reflection）與 inspect 模組，
自動解析並說明任意 Python 模組結構的工具。

📦 功能：
- 顯示模組名稱、說明文件、來源檔案
- 列出該模組中的類別、函式、常數
- 提供簡短解釋與簽章（signature）
- 可被 import 或直接在命令列使用

🧠 作者：ChatGPT (自動生成)
📅 版本：1.0
"""

import inspect
import importlib
import sys

def explain_module(module_name: str):
    """反射說明模組結構與內容"""
    try:
        mod = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"❌ 找不到模組：{module_name}")
        return

    print(f"\n📦 模組：{module_name}")
    print("-" * (len(module_name) + 6))

    doc = (mod.__doc__ or "").strip().split("\n")[0]
    print(f"🧾 模組說明：{doc or '（無說明文件）'}")

    print(f"📂 來源檔案：{getattr(mod, '__file__', '（內建模組或已編譯為 C）')}")

    print("\n📘 類別（Classes）：")
    classes = [
        (name, obj) for name, obj in inspect.getmembers(mod, inspect.isclass)
        if obj.__module__ == mod.__name__
    ]
    if not classes:
        print("  （無類別）")
    for name, obj in classes:
        brief = inspect.getdoc(obj).splitlines()[0] if obj.__doc__ else ""
        print(f"  🏷 {name}  →  {brief}")

    print("\n⚙️ 函式（Functions）：")
    funcs = [
        (name, obj) for name, obj in inspect.getmembers(mod, inspect.isfunction)
        if obj.__module__ == mod.__name__
    ]
    if not funcs:
        print("  （無函式）")
    for name, obj in funcs:
        sig = str(inspect.signature(obj))
        doc = inspect.getdoc(obj)
        brief = doc.split("\n")[0] if doc else "（無說明）"
        print(f"  🔹 {name}{sig}  →  {brief}")

    print("\n📄 常數或變數（Others）：")
    others = [
        (name, obj) for name, obj in inspect.getmembers(mod)
        if not (inspect.isclass(obj) or inspect.isfunction(obj) or name.startswith("__"))
    ]
    if not others:
        print("  （無其他項目）")
    for name, obj in others:
        value = repr(obj)
        if len(value) > 80:
            value = value[:77] + "..."
        print(f"  📍 {name} = {value}")

# 命令列模式
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python chatgpt_help.py <模組名稱>")
        print("例如：python chatgpt_help.py pandas")
    else:
        explain_module(sys.argv[1])
