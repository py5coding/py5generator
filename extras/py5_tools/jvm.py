from pathlib import Path

import jnius_config


py5_started = False


def check_jvm_running():
    if jnius_config.vm_running:
        raise RuntimeError("the jvm is already running, started at "
                           + jnius_config.vm_started_at)


def get_options():
    return jnius_config.get_options()


def set_options(*options):
    check_jvm_running()
    jnius_config.set_options(*options)


def add_options(*options):
    check_jvm_running()
    jnius_config.add_options(*options)


def get_classpath():
    return jnius_config.get_classpath()


def set_classpath(*classpath):
    check_jvm_running()
    jnius_config.set_classpath(*classpath)


def add_classpath(*classpath):
    check_jvm_running()
    jnius_config.add_classpath(*classpath)


def add_jars(path):
    check_jvm_running()
    if not isinstance(path, Path):
        path = Path(path)
    if path.exists():
        for jarfile in path.glob("**/*.[Jj][Aa][Rr]"):
            jnius_config.add_classpath(str(jarfile))


__all__ = ['py5_started', 'check_jvm_running',
           'get_options', 'set_options', 'add_options',
           'get_classpath', 'set_classpath', 'add_classpath',
           'add_jars']
