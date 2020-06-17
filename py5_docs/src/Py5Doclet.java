import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import javax.lang.model.SourceVersion;
import javax.lang.model.element.Element;
import javax.lang.model.element.ElementKind;
import javax.lang.model.element.ExecutableElement;
import javax.lang.model.element.TypeElement;
import javax.lang.model.element.VariableElement;
import javax.lang.model.util.ElementFilter;

import jdk.javadoc.doclet.Doclet;
import jdk.javadoc.doclet.DocletEnvironment;
import jdk.javadoc.doclet.Reporter;

import com.sun.source.util.DocTrees;
import com.sun.source.doctree.DocTree;
import com.sun.source.doctree.ParamTree;
import com.sun.source.doctree.SeeTree;
import com.sun.source.doctree.ReturnTree;
import com.sun.source.doctree.DeprecatedTree;
import com.sun.source.doctree.ThrowsTree;
import com.sun.source.doctree.UnknownBlockTagTree;
import com.sun.source.doctree.DocCommentTree;

public class Py5Doclet implements Doclet {
    protected Reporter reporter;
    private final Pattern LINK_REGEX;
    private final Pattern DOT_REGEX;
    private PrintWriter paramPrinter;

    public Py5Doclet() {
        LINK_REGEX = Pattern.compile("<a href=\"([^\"]*)\">([^<]*)</a>", Pattern.CASE_INSENSITIVE);
        DOT_REGEX = Pattern.compile("\\.");
    }

    @Override
    public void init(Locale locale, Reporter reporter) {
        this.reporter = reporter;
    }

    private String fixLinks(String text) {
        while (true) {
            Matcher m = LINK_REGEX.matcher(text);
            if (m.find()) {
                text = text.replace(m.group(0), String.format(" [%s](%s) ", m.group(2), m.group(1)));
            } else {
                return text;
            }
        }
    }

    private String removePackage(String str) {
        String[] tokens = DOT_REGEX.split(str);
        return tokens[tokens.length - 1];
    }

    private String listToString(List<String> list) {
        return list.stream().map(this::removePackage).collect(Collectors.joining(","));
    }

    public void processElement(DocTrees trees, String partOf, Element e) {
        ElementKind kind = e.getKind();
        String name = e.getSimpleName().toString();

        if (kind == ElementKind.METHOD) {
            System.out.println("{{parameters}}");
            List<String> paramTypes = new ArrayList<String>();
            List<String> paramNames = new ArrayList<String>();
            ExecutableElement ee = (ExecutableElement) e;
            for (VariableElement pe : ee.getParameters()) {
                paramTypes.add(pe.asType().toString());
                paramNames.add(pe.toString());
            }
            if (paramPrinter != null) {
                paramPrinter.printf("%s|%s|%s|%s|%s\n", removePackage(partOf), name, listToString(paramTypes),
                        listToString(paramNames), removePackage(ee.getReturnType().toString()));
            }
        }

        DocCommentTree docCommentTree = trees.getDocCommentTree(e);
        if (docCommentTree != null) {
            System.out.println("******************************************");
            System.out.println("(" + kind + ") " + partOf + "." + name);

            System.out.println("{{Entire body}}");
            StringBuilder sb = new StringBuilder();
            for (DocTree tree : docCommentTree.getFullBody()) {
                String s = tree.toString();
                s = s.replaceAll("\\( begin auto-generated from .*?\\)", "");
                s = s.replaceAll("\\( end auto-generated \\)", "");
                s = s.trim();
                s = s.replace("\n", "");
                s = s.replace("<br/>", "\n");
                s = s.replace("<BR>", "\n");
                s = s.replace("<nobr>", "");
                s = s.replace("</nobr>", "");
                s = s.replace("<NOBR>", "");
                s = s.replace("</NOBR>", "");
                s = s.replace("<b>", " `");
                s = s.replace("</b>", "` ");
                s = s.replace("<PRE>", "\n\n```\n");
                s = s.replace("</PRE>", "\n```\n\n");
                s = s.replace("<TT>", "\n\n```\n");
                s = s.replace("</TT>", "\n```\n\n");
                s = s.replace("<h3>", "\n\n");
                s = s.replace("</h3>", "\n--------\n\n");
                s = s.replace("<P>", "\n\n");
                s = s.replace("<p>", "\n\n");
                s = s.replace("<p/>", "\n\n");
                sb.append(s);
            }
            System.out.print(fixLinks(sb.toString()));

            System.out.println("\n{{Block tags}}");
            for (DocTree tree : docCommentTree.getBlockTags()) {
                switch (tree.getKind()) {
                    case PARAM:
                        ParamTree param = (ParamTree) tree;
                        String pname = param.getName().toString();
                        String desc = param.getDescription().toString();
                        String istype = param.isTypeParameter() ? " (type)" : "";
                        System.out.println("Param: " + pname + istype + ": " + desc);
                        break;
                    case SEE:
                        SeeTree see = (SeeTree) tree;
                        String reference = see.getReference().toString();
                        System.out.println("See Also: " + reference);
                        break;
                    case RETURN:
                        ReturnTree ret = (ReturnTree) tree;
                        String retDesc = ret.getDescription().toString();
                        System.out.println("Returns: " + retDesc);
                        break;
                    case THROWS:
                        ThrowsTree throwsTree = (ThrowsTree) tree;
                        String throwDesc = throwsTree.getDescription().toString();
                        String eName = throwsTree.getExceptionName().toString();
                        System.out.println("Throws: " + eName + " " + throwDesc);
                        break;
                    case DEPRECATED:
                        DeprecatedTree dep = (DeprecatedTree) tree;
                        String reason = dep.getBody().toString();
                        System.out.println("Deprecated: " + reason);
                        break;
                    case UNKNOWN_BLOCK_TAG:
                        UnknownBlockTagTree unknown = (UnknownBlockTagTree) tree;
                        String tagname = unknown.getTagName().toString();
                        String content = unknown.getContent().toString();
                        System.out.println("Unknown: " + tagname + " " + content);
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
        try {
            paramPrinter = new PrintWriter(new File(paramFile));
        } catch (FileNotFoundException e) {
            System.err.println(String.format("Param file %s cannot be found", paramFile));
        }

        DocTrees docTrees = docEnv.getDocTrees();
        for (TypeElement t : ElementFilter.typesIn(docEnv.getIncludedElements())) {
            System.out.println(t.getKind() + ":" + t);
            for (Element e : t.getEnclosedElements()) {
                processElement(docTrees, t.toString(), e);
            }
        }

        if (paramPrinter != null) {
            paramPrinter.close();
        }

        return true;
    }

    @Override
    public String getName() {
        return "Py5Doclet";
    }

    @Override
    public SourceVersion getSupportedSourceVersion() {
        // support the latest release
        return SourceVersion.latest();
    }

    private String paramFile;

    @Override
    public Set<? extends Option> getSupportedOptions() {
        Option[] options = { new Option() {
            private final List<String> methodParamOption = Arrays.asList("-paramfile", "--param-file", "-p");

            @Override
            public int getArgumentCount() {
                return 1;
            }

            @Override
            public String getDescription() {
                return "output file for method parameter names";
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
                paramFile = arguments.get(0);
                return true;
            }
        } };
        return new HashSet<>(Arrays.asList(options));
    }
}
