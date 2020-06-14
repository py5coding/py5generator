import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

import javax.lang.model.SourceVersion;
import javax.lang.model.element.Element;
import javax.lang.model.element.TypeElement;
import javax.lang.model.util.ElementFilter;
import javax.tools.Diagnostic.Kind;

import jdk.javadoc.doclet.Doclet;
import jdk.javadoc.doclet.DocletEnvironment;
import jdk.javadoc.doclet.Reporter;

import com.sun.source.util.DocTrees;
import com.sun.source.doctree.DocCommentTree;

public class Py5Doclet implements Doclet {
  Reporter reporter;
  @Override
  public void init(Locale locale, Reporter reporter) {
      reporter.print(Kind.NOTE, "Doclet using locale: " + locale);
      this.reporter = reporter;
  }

  public void printElement(DocTrees trees, Element e) {
      DocCommentTree docCommentTree = trees.getDocCommentTree(e);
      if (docCommentTree != null) {
          System.out.println("Element (" + e.getKind() + ": "
                  + e + ") has the following comments:");
          System.out.println("Entire body: " + docCommentTree.getFullBody());
          System.out.println("Block tags: " + docCommentTree.getBlockTags());
      }
  }

  @Override
  public boolean run(DocletEnvironment docEnv) {
      DocTrees docTrees = docEnv.getDocTrees();
      for (TypeElement t : ElementFilter.typesIn(docEnv.getIncludedElements())) {
          System.out.println(t.getKind() + ":" + t);
          for (Element e : t.getEnclosedElements()) {
              printElement(docTrees, e);
          }
      }
      return true;
  }

  @Override
  public String getName() {
      return "Py5Doclet";
  }

  @Override
  public Set<? extends Option> getSupportedOptions() {
      Option[] options = {
          new Option() {
              private final List<String> someOption = Arrays.asList(
                      "-overviewfile",
                      "--overview-file",
                      "-o"
              );

              @Override
              public int getArgumentCount() {
                  return 1;
              }

              @Override
              public String getDescription() {
                  return "an option with aliases";
              }

              @Override
              public Option.Kind getKind() {
                  return Option.Kind.STANDARD;
              }

              @Override
              public List<String> getNames() {
                  return someOption;
              }

              @Override
              public String getParameters() {
                  return "file";
              }

              @Override
              public boolean process(String opt, List<String> arguments) {
                  return true;
              }
          }
      };
      return new HashSet<Option>(Arrays.asList(options));
  }

  @Override
  public SourceVersion getSupportedSourceVersion() {
      // support the latest release
      return SourceVersion.latest();
  }
}
