import os
from pathlib import Path
import sys

CWD = Path(os.path.dirname(os.path.realpath(__file__)))
SRC = CWD.parent / "scrapl"
sys.path.append(str(SRC))

