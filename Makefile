py5_jar_file = py5jar/dist/py5.jar
py5_java_src = $(shell find py5jar/src/ -name "*.java")
py5_py_src = $(shell find py5_resources/ -name "*.py")
py5_tools_py_src = $(shell find extras/ -name "*.py")
py5_build_dir = build/py5
py5_installed = .install_py5.nogit
py5_tools_installed = .install_py5_tools.nogit
all_installed = .install_all.nogit

all: install_py5 install_py5_tools

py5jar: $(py5_jar_file)
$(py5_jar_file): $(py5_java_src)
	ant -f py5jar/build.xml -Dprocessing_dir=$(realpath $(processing_dir))

generate_py5: $(py5_build_dir)
$(py5_build_dir): $(py5_jar_file) $(py5_py_src)
	python generate_py5.py -r $(processing_dir)
 
install_py5 : $(py5_installed)
$(py5_installed): $(py5_build_dir)
	cd build/ && python setup.py build && pip install -e .
	touch $(py5_installed)

install_py5_tools : $(py5_tools_installed)
$(py5_tools_installed): $(py5_tools_py_src)
	cd extras/ && python setup.py build && pip install -e .
	touch $(py5_tools_installed)

.PHONY: clean
clean:
	rm -Rf build/
	ant -f py5jar/build.xml clean
