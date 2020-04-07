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


def get_signature(cls_tp):
    tp = cls_tp.getName()
    if tp[0] == '[':
        return tp.replace('.', '/')
    signatures = {
        'void': 'V', 'boolean': 'Z', 'byte': 'B',
        'char': 'C', 'short': 'S', 'int': 'I',
        'long': 'J', 'float': 'F', 'double': 'D'}
    ret = signatures.get(tp)
    if ret:
        return ret
    # don't do it in recursive way for the moment,
    # error on the JNI/android: JNI ERROR (app bug): local reference table
    # overflow (max=512)

    # ensureclass(tp)
    return 'L{0};'.format(tp.replace('.', '/'))


clsname = 'processing.core.PApplet'
jniname = clsname.replace('.', '/')
cls = MetaJavaClass.get_javaclass(jniname)


classDict = {}

# c = Class.forName(clsname)
c = find_javaclass(clsname)
if c is None:
    raise Exception('Java class {0} not found'.format(c))

constructors = []
for constructor in c.getConstructors():
    sig = '({0})V'.format(
        ''.join([get_signature(x) for x in constructor.getParameterTypes()]))
    constructors.append((sig, constructor.isVarArgs()))
classDict['__javaconstructor__'] = constructors

cls = c


methods = cls.getDeclaredMethods()
methods_name = [x.getName() for x in methods]

name = 'background'


signatures = []
for index, subname in enumerate(methods_name):
    if subname != name:
        continue
    method = methods[index]
    sig = '({0}){1}'.format(
        ''.join([get_signature(x) for x in method.getParameterTypes()]),
        get_signature(method.getReturnType()))

    signatures.append((sig, Modifier.isStatic(method.getModifiers()), method.isVarArgs()))

signatures
