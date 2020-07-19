import numpy as np
import py5  # noqa
import jpype  # noqa
import jpype.imports  # noqa
from jpype.types import JClass, JInt, JArray


MyTest = JClass('py5.core.MyTest')


# create integer array
foo = np.array([0xFF00CC00, 0xFFAA8833], dtype=np.int32)
# gets read correctly, java int array is returned
out = MyTest.test1(foo)

# can easily create a memoryview to convert to bytes but has endian issues
np.frombuffer(memoryview(out), dtype=np.uint8)

# direct buffer created in Java
java = jpype.JPackage('java')
jb = java.nio.ByteBuffer.allocateDirect(80)
db = jb.asDoubleBuffer()
a = np.asarray(db)


# direct buffer created in Python
bb = bytearray(80)
jb = jpype.nio.convertToDirectBuffer(bb)
db = jb.asDoubleBuffer()
a = np.asarray(db)
