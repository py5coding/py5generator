import jnius_config
jnius_config.set_classpath(
    '.', '/home/jim/Projects/git/processing/core/library/*')
from jnius import autoclass, JavaClass, JavaStaticMethod, MetaJavaClass, find_javaclass, with_metaclass  # noqa


class Modifier(with_metaclass(MetaJavaClass, JavaClass)):
    __javaclass__ = 'java/lang/reflect/Modifier'

    isAbstract = JavaStaticMethod('(I)Z')
    isFinal = JavaStaticMethod('(I)Z')
    isInterface = JavaStaticMethod('(I)Z')
    isNative = JavaStaticMethod('(I)Z')
    isPrivate = JavaStaticMethod('(I)Z')
    isProtected = JavaStaticMethod('(I)Z')
    isPublic = JavaStaticMethod('(I)Z')
    isStatic = JavaStaticMethod('(I)Z')
    isStrict = JavaStaticMethod('(I)Z')
    isSynchronized = JavaStaticMethod('(I)Z')
    isTransient = JavaStaticMethod('(I)Z')
    isVolatile = JavaStaticMethod('(I)Z')


PythonPApplet = autoclass('processing.core.PythonPApplet', public_only=True)
_papplet = PythonPApplet()

cls = find_javaclass('processing.core.PythonPApplet')

while cls is not None:
    print(cls.getName())
    print("=" * 20)
    for method in cls.getDeclaredMethods():
        name = method.getName()
        modifiers = method.getModifiers()
        print(name, Modifier.isPublic(modifiers))

    _cls = cls.getSuperclass()
    if not _cls and cls.isInterface():
        cls = find_javaclass('java.lang.Object')
    else:
        cls = _cls

    print('\n')
