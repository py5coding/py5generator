py5jar_file = py5jar/dist/py5.jar

all: generate_py5

generate_py5: py5jar
	python generate_py5.py $(py5_dir) --exist_ok -r $(processing_dir)

py5jar: $(py5jar_file)
$(py5jar_file):
	ant -f py5jar/build.xml -Dprocessing_dir=$(realpath $(processing_dir))

.PHONY: clean
clean:
	ant -f py5jar/build.xml clean

