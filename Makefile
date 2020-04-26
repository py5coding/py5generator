all: generate_py5

generate_py5: py5jar
	python generate_py5.py ../py5build/ --exist_ok -r ../sam_processing4

sam_processing4_jar:
	ant -f ../sam_processing4/core/build.xml

py5jar: sam_processing4_jar
	ant -f py5jar/build.xml -Dprocessing_lib_dir=/home/jim/Projects/ITP/pythonprocessing/sam_processing4/core/library/

# processing3_jar:
# 	(JAVA_HOME="/usr/lib/jvm/jdk1.8.0_74"; ant -f /home/jim/Projects/ITP/pythonprocessing/processing/core/build.xml)

.PHONY: clean
clean:
	ant -f py5jar/build.xml clean
	ant -f ../sam_processing4/core/build.xml clean

