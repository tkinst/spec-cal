import sys, os

virt_binary = "/home/tomkinst/pyenv/bin/python"
if sys.executable != virt_binary: os.execl(virt_binary, viry_binary, *sys.argv)
sys.path.append(os.getcwd())
from SpecWeather import app as application

