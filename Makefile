py5_jar_file = py5jar/dist/py5.jar
py5_java_src = $(shell find py5jar/src/ -name "*.java")

all: install_py5

generate_py5: py5jar
	python generate_py5.py $(py5_dir) --exist_ok -r $(processing_dir)

install_py5: generate_py5
	cd $(py5_dir)/py5/ && python setup.py build && pip install -e .

py5jar: $(py5_jar_file)
$(py5_jar_file): $(py5_java_src)
	ant -f py5jar/build.xml -Dprocessing_dir=$(realpath $(processing_dir))

.PHONY: clean
clean:
	ant -f py5jar/build.xml clean
