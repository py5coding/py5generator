import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

import javax.lang.model.SourceVersion;
import javax.lang.model.element.Element;
import javax.lang.model.element.ElementKind;
import javax.lang.model.element.TypeElement;
import javax.lang.model.util.ElementFilter;
// import javax.tools.Diagnostic.Kind;

import jdk.javadoc.doclet.Doclet;
import jdk.javadoc.doclet.DocletEnvironment;
import jdk.javadoc.doclet.Reporter;

import com.sun.source.util.DocTrees;
import com.sun.source.doctree.DocTree;
// import com.sun.source.doctree.DocTree.Kind;
import com.sun.source.doctree.ParamTree;
import com.sun.source.doctree.SeeTree;
import com.sun.source.doctree.UnknownBlockTagTree;
import com.sun.source.doctree.DocCommentTree;

public class Py5Doclet implements Doclet {
    Reporter reporter;

    @Override
    public void init(Locale locale, Reporter reporter) {
        // reporter.print(Kind.NOTE, "Doclet using locale: " + locale);
        this.reporter = reporter;
    }

    public void printElement(DocTrees trees, Element e) {
        ElementKind kind = e.getKind();
        String name = e.getSimpleName().toString();

        DocCommentTree docCommentTree = trees.getDocCommentTree(e);
        if (docCommentTree != null) {
            System.out.println("******************************************");
            System.out.println(name + "(" + kind + ")");

            System.out.println("Entire body:");
            for (DocTree tree : docCommentTree.getFullBody()) {
                System.out.print(tree.toString().trim().replace("<br/>", "\n"));
            }

            System.out.println("\nBlock tags:");
            for (DocTree tree : docCommentTree.getBlockTags()) {
                switch (tree.getKind()) {
                    case PARAM:
                        ParamTree param = (ParamTree) tree;
                        String pname = param.getName().toString();
                        String desc = param.getDescription().toString();
                        String istype = param.isTypeParameter() ? " (type)" : "";
                        System.out.println(pname + istype + ": " + desc);
                        break;
                    case SEE:
                        SeeTree see = (SeeTree) tree;
                        String reference = see.getReference().toString();
                        System.out.println("See Also: " + reference);
                        break;
                    case UNKNOWN_BLOCK_TAG:
                        UnknownBlockTagTree unknown = (UnknownBlockTagTree) tree;
                        String tagname = unknown.getTagName().toString();
                        String content = unknown.getContent().toString();
                        System.out.println(tagname + " " + content);
                        break;
                    default:
                        System.out.println("???? DEFAULT ????");
                        System.out.println(tree.getKind());
                        System.out.println(tree.toString());
                }
            }
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
        Option[] options = { new Option() {
            private final List<String> someOption = Arrays.asList("-overviewfile", "--overview-file", "-o");

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
        } };
        return new HashSet<Option>(Arrays.asList(options));
    }

    @Override
    public SourceVersion getSupportedSourceVersion() {
        // support the latest release
        return SourceVersion.latest();
    }
}
