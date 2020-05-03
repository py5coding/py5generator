py5_jar_file = py5jar/dist/py5.jar
py5_java_src = $(shell find py5jar/src/ -name "*.java")
py5_py_src = $(shell find py5_resources/ -name "*.py")
py5_build_dir = build/py5

all: generate_py5

py5jar: $(py5_jar_file)
$(py5_jar_file): $(py5_java_src)
	ant -f py5jar/build.xml -Dprocessing_dir=$(realpath $(processing_dir))

generate_py5: $(py5_build_dir)
$(py5_build_dir): $(py5_jar_file) $(py5_py_src)
	python generate_py5.py -r $(processing_dir)
 
install_py5: generate_py5
	cd build/ && python setup.py build && pip install -e .

.PHONY: clean
clean:
	rm -Rf build/
	ant -f py5jar/build.xml clean
