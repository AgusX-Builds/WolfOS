import subprocess
import os
import sys

# WOLF OS main folder
wolfos_folder = os.path.dirname(os.path.abspath(__file__))

# Always use the latest main.py in this folder
main_file = os.path.join(wolfos_folder, "main.py")

# Python 3.14
python_path = "/usr/local/bin/python3.14"

# Make sure main.py exists
if not os.path.isfile(main_file):
    print("ERROR: WOLF OS main.py was not found.")
    sys.exit(1)

# Launch the current WOLF OS
subprocess.Popen(
    [python_path, main_file],
    cwd=wolfos_folder
)
