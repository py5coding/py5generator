py5_java_src = $(shell find py5_jar/src/ -name "*.java")
py5_jar_file = py5_jar/dist/py5.jar

py5_py_src = $(shell find py5_resources/ -name "*.py*") $(shell find py5_resources/ -name "*.csv")
py5_build_dir = build

py5_doclet_java_src = $(shell find py5_docs/src/ -name "*.java")
py5_doclet_jar_file = py5_docs/dist/py5doclet.jar
py5_method_param_names_file = py5_docs/docfiles/method_parameter_names.psv
py5_javadoc_file = py5_docs/docfiles/javadocs.xml

py5_generator = generate_py5.py
generator_src = $(shell find generator/ -name "*.py*")
py5_installed = .install_py5.nogit

all: install_py5

py5_jar: $(py5_jar_file)
$(py5_jar_file): $(py5_java_src)
	ant -f py5_jar/build.xml -Dprocessing_dir=$(realpath $(processing_dir))

generate_py5: $(py5_build_dir)
$(py5_build_dir): $(py5_jar_file) $(py5_py_src) $(py5_generator) $(generator_src) $(py5_method_param_names_file)
	python generate_py5.py -r $(processing_dir) -p $(py5_method_param_names_file)

install_py5: $(py5_installed)
$(py5_installed): $(py5_build_dir)
	cd build/ && python setup.py build && pip install .
	touch $(py5_installed)

docletjar: $(py5_doclet_jar_file)
$(py5_doclet_jar_file) : $(py5_doclet_java_src)
	ant -f py5_docs/build.xml

create_docfiles: $(py5_method_param_names_file) $(py5_javadoc_file)
$(py5_method_param_names_file) $(py5_javadoc_file): $(py5_doclet_jar_file)
	javadoc -doclet py5.javadocs.Py5Doclet \
		-docletpath py5_docs/dist/py5doclet.jar \
		--source-path $(processing_dir)/core/src/ \
		-classpath "$(processing_dir)/core/library/*" \
		--show-members public \
		--param-file $(py5_method_param_names_file) \
		--javadoc-file $(py5_javadoc_file) \
		"processing.core" "processing.opengl"

.PHONY: clean
clean:
	rm -Rf build/
	rm -f $(py5_installed)
	ant -f py5_jar/build.xml clean
	ant -f py5_docs/build.xml clean
