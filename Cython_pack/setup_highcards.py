from distutils.core import setup
from Cython.Build import cythonize
import os
os.chdir(r"C:\Users\Mathi\Desktop\cards7\Cython_pack")
setup(name = "highcards", ext_modules=cythonize("highcards.pyx"))
