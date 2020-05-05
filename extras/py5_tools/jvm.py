import jnius_config


def is_jvm_running():
    return jnius_config.vm_running


def add_classpath(classpath):
    if jnius_config.vm_running:
        raise RuntimeError('cannot add to classpath after jvm has started.')
    else:
        jnius_config.add_classpath(classpath)


def add_options(*options):
    if jnius_config.vm_running:
        raise RuntimeError('cannot add options after jvm has started.')
    else:
        jnius_config.add_options(*options)


__all__ = ['add_classpath', 'is_jvm_running', 'add_options']
