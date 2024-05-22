import os
from discord import dcsend

# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Run fetch.py
try:
    os.system("fetch.py")
except Exception as e:
    print(f"Error: {e}")

dcsend("")
