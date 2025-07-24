import os
import sys
from importlib import resources

if 'aliyun_tablestore.py' not in os.listdir(resources.files("mem0.vector_stores")):
    mem0_wheel_path = resources.files("tablestore_openmemory_mcp").joinpath("mem0_wheel/mem0ai-0.1.114-py3-none-any.whl")
    os.system(f"uv pip install {mem0_wheel_path} --python {sys.executable}")
    os.execv(sys.executable, [sys.executable] + sys.argv)