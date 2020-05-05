import jnius_config


def add_classpath(classpath):
    if jnius_config.vm_running:
        raise RuntimeError('cannot add to classpath after jvm has started.')
    else:
        jnius_config.add_classpath(classpath)


def is_jvm_running():
    return jnius_config.vm_running


__all__ = ['add_classpath', 'is_jvm_running']
