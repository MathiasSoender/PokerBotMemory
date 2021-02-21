from distutils.core import setup
from Cython.Build import cythonize
import os
os.chdir(r"C:\Users\Mathi\Desktop\cards7\Cython_pack")
setup(name = "hand_rankings", ext_modules=cythonize("hand_rankings.pyx"))
