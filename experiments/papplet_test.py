# import os
# os.environ['JAVA_HOME'] = '/usr/lib/jvm/jdk1.8.0_74'

import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')

# jnius_config.set_classpath('.', '/home/jim/Projects/ITP/pythonprocessing/processing/core/library/*')
# jnius_config.set_classpath('.', '/home/jim/Projects/ITP/pythonprocessing/py5/jars/current/*')
# jnius_config.set_classpath('.', '/home/jim/Projects/ITP/pythonprocessing/py5/jars/2.3.2/*')
jnius_config.set_classpath('.', '/home/jim/Projects/ITP/pythonprocessing/py5/jars/2.4/*')
from jnius import autoclass  # noqa


PApplet = autoclass('processing.core.PApplet',
                    include_protected=False, include_private=False)
PAppletTest = autoclass('processing.core.PAppletTest',
                        include_protected=False, include_private=False)

test_applet = PAppletTest()
PApplet.runSketch([''], test_applet)
