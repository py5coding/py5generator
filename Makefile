py5_jar_file = py5jar/dist/py5.jar
py5_java_src = $(shell find py5jar/src/ -name "*.java")

all: install_p5

generate_py5: py5jar
	python generate_py5.py -r $(processing_dir)

install_p5: generate_py5
	cd build/ && python setup.py build && pip install -e .

py5jar: $(py5_jar_file)
$(py5_jar_file): $(py5_java_src)
	ant -f py5jar/build.xml -Dprocessing_dir=$(realpath $(processing_dir))

.PHONY: clean
clean:
	rm -Rf build/
	ant -f py5jar/build.xml clean
