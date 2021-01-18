from pathlib import Path


PY5_UTILITIES_CLASS = """package py5.utils;

import processing.core.PApplet;

class Py5Utilities {

  public PApplet papplet;

  public Py5Utilities(PApplet papplet) {
    this.papplet = papplet;
  }

}
"""

DOT_PROJECT = """<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
	<name>py5utilities</name>
	<comment></comment>
	<projects>
	</projects>
	<buildSpec>
		<buildCommand>
			<name>org.eclipse.jdt.core.javabuilder</name>
			<arguments>
			</arguments>
		</buildCommand>
	</buildSpec>
	<natures>
		<nature>org.eclipse.jdt.core.javanature</nature>
	</natures>
	<filteredResources>
		<filter>
			<id>1599075320853</id>
			<name></name>
			<type>30</type>
			<matcher>
				<id>org.eclipse.core.resources.regexFilterMatcher</id>
				<arguments>node_modules|.git|__CREATED_BY_JAVA_LANGUAGE_SERVER__</arguments>
			</matcher>
		</filter>
	</filteredResources>
</projectDescription>
"""

DOT_CLASSPATH_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<classpath>
	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-11"/>
	<classpathentry kind="src" path="src"/>
	<classpathentry kind="lib" path="{path}/core.jar"/>
	<classpathentry kind="lib" path="{path}/jogl-all.jar"/>
	<classpathentry kind="output" path="build"/>
</classpath>
"""

BUILD_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<project name="py5 jar" default="dist">

    <description>
        compile and build the py5 utilities jar.
    </description>

    <property name="src" location="src"/>
    <property name="build" location="build"/>
    <property name="dist" location="jars"/>

    <target name="compile" description="compile the source">
        <mkdir dir="{build}"/>
        <javac source="11" target="11" debug="true" includeantruntime="false" srcdir="{src}" destdir="{build}">
            <classpath>
                <fileset dir="{path}">
                        <include name="**/*.jar"/>
                </fileset>
            </classpath>
        </javac>
    </target>

    <target name="dist" depends="compile" description="make the jar">
        <mkdir dir="{dist}"/>
        <jar destfile="{dist}/py5utilities.jar" basedir="{build}"/>
    </target>

    <target name="clean">
        <delete dir="{build}"/>
        <delete dir="{dist}"/>
    </target>

</project>
"""


def generate_utilities_framework():
    import py5
    jarsdir = Path(py5.__file__).parent / 'jars'

    template_params = {x: f'{chr(36)}{{{x}}}' for x in ['build', 'dist', 'src']}
    template_params['path'] = jarsdir.as_posix()

    with open('build.xml', 'w') as f:
        f.write(BUILD_XML_TEMPLATE.format(**template_params))

    with open('.classpath', 'w') as f:
        f.write(DOT_CLASSPATH_TEMPLATE.format(**template_params))
    
    with open('.project', 'w') as f:
        f.write(DOT_PROJECT)

    src_dir = Path('src/py5/utils')
    src_dir.mkdir(parents=True, exist_ok=True)
    with open(src_dir / 'Py5Utilities.java', 'w') as f:
        f.write(PY5_UTILITIES_CLASS)
