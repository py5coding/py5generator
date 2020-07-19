import numpy as np
import py5  # noqa
import jpype  # noqa
import jpype.imports  # noqa
from jpype.types import JClass, JInt, JArray

java = jpype.JPackage('java')

MyTest = JClass('py5.core.MyTest')

bb = bytearray(5 * 6 * 4)
jb = jpype.nio.convertToDirectBuffer(bb)
# jb = java.nio.ByteBuffer.allocateDirect(5 * 6 * 4)
arr = np.asarray(bb, dtype=np.uint8).reshape(5, 6, 4)

myTest = MyTest(jb)

#############
# this works

# # direct buffer created in Java
# jb = java.nio.ByteBuffer.allocateDirect(80)
# ib = jb.asIntBuffer()
# a = np.asarray(ib)


# # direct buffer created in Python
# ib = jb.asIntBuffer()
# a = np.asarray(ib)

# MyTest.test3(jb)
# # a now contains 42

# print(a)
# a[:10] = 50

# MyTest.test2(jb)
# # prints 50


##############
# this works also

# set each pixel to something
myTest.resetPixels()
print(list(myTest.pixels))

# copy from pixel array to arr
myTest.getPixels()

# arr now contains 255, 128, 16, 1
print(arr)

# change arr
arr[:, :, 3] = 255

# update pixel array from arr
myTest.setPixels()

# pixel array is now different
print(list(myTest.pixels))
