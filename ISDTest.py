import missionEXE
import os

cwd=os.getcwd()

missionEXE.ISA500(runtime=20, directory=cwd, port="/dev/ttyUSB2")