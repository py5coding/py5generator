package py5.javadocs;

import java.util.Arrays;
import java.util.List;

import jdk.javadoc.doclet.Doclet.Option;

public class Py5DocletOption implements Option {
  private List<String> methodParamOption;
  private String description;
  public String filename;

  public Py5DocletOption(String description, String[] options) {
    this.description = description;
    methodParamOption = Arrays.asList(options);
  }

  @Override
  public int getArgumentCount() {
    return 1;
  }

  @Override
  public String getDescription() {
    return description;
  }

  @Override
  public Option.Kind getKind() {
    return Option.Kind.STANDARD;
  }

  @Override
  public List<String> getNames() {
    return methodParamOption;
  }

  @Override
  public String getParameters() {
    return "file";
  }

  @Override
  public boolean process(String opt, List<String> arguments) {
    filename = arguments.get(0);
    return true;
  }
}
