# file: geometry.py

import ctypes as C

CLIB = C.CDLL('./libgeometry.so')
CLIB.area.argtypes = [C.Structure]
CLIB.area.restype = C.c_float

class Rectangle(C.Structure):
  _fields_ = [("height", C.c_float),
              ("width", C.c_float)]

  def __init__(self, height, width):
    self.height = height
    self.width = width

  def area(self):
    return CLIB.area(self)
