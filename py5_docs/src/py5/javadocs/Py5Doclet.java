package py5.javadocs;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.lang.model.SourceVersion;
import javax.lang.model.element.Element;
import javax.lang.model.element.ElementKind;
import javax.lang.model.element.TypeElement;
import javax.lang.model.util.ElementFilter;
import javax.tools.Diagnostic;

import jdk.javadoc.doclet.Doclet;
import jdk.javadoc.doclet.DocletEnvironment;
import jdk.javadoc.doclet.Reporter;

import com.sun.source.util.DocTrees;
import com.sun.source.doctree.DocTree;
import com.sun.source.doctree.DocCommentTree;

public class Py5Doclet implements Doclet {
    protected Reporter reporter;
    private final Pattern LINK_REGEX;
    private PrintWriter javadocPrinter;
    private Py5DocletOption javadocFileOption;

    public Py5Doclet() {
        LINK_REGEX = Pattern.compile("<a href=\"([^\"]*)\">([^<]*)</a>", Pattern.CASE_INSENSITIVE);

        javadocFileOption = new Py5DocletOption("output file for javadoc comments and block tags",
                new String[] { "-javadocfile", "--javadoc-file" });
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

    private String cleanupText(String s) {
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
        s = s.replace("<UL>", "\n");
        s = s.replace("<LI>", "\n* ");
        s = s.replace("</UL>", "\n");
        s = s.replace("<PRE>", "\n\n```\n");
        s = s.replace("</PRE>", "\n```\n\n");
        s = s.replace("<TT>", "\n\n```\n");
        s = s.replace("</TT>", "\n```\n\n");
        s = s.replace("<h3>", "\n\n");
        s = s.replace("</h3>", "\n--------\n\n");
        s = s.replace("<P>", "\n\n");
        s = s.replace("</P>", "\n\n");
        s = s.replace("<p>", "\n\n");
        s = s.replace("<p/>", "\n\n");
        s = s.replace("</T>", "\n\n");

        s = s.replace(">", "&gt;");
        s = s.replace("<", "&lt;");
        s = s.replace("&rarr;", "");
        s = s.replace("&deg;", "°");

        return s;
    }

    public void processElement(DocTrees trees, String partOf, Element e) {
        ElementKind kind = e.getKind();
        String name = e.getSimpleName().toString().replace("<", "").replace(">", "");

        DocCommentTree docCommentTree = trees.getDocCommentTree(e);
        if (javadocPrinter != null && docCommentTree != null) {

            javadocPrinter.printf("<commenttree class=\"%s\" name=\"%s\" kind=\"%s\">\n", partOf, name, kind);

            javadocPrinter.println("<body>");
            StringBuilder sb = new StringBuilder();
            javadocPrinter.printf("<first>%s</first>\n", cleanupText(docCommentTree.getFirstSentence().toString()));
            javadocPrinter.println("<full>");
            for (DocTree tree : docCommentTree.getFullBody()) {
                String s = tree.toString();
                s = s.replaceAll("\\( begin auto-generated from .*?\\)", "");
                s = s.replaceAll("\\( end auto-generated \\)", "");
                s = cleanupText(s);
                sb.append(s);
            }
            javadocPrinter.println(fixLinks(sb.toString()));
            javadocPrinter.println("</full>");
            javadocPrinter.println("</body>");

            javadocPrinter.println("<blocktags>");
            for (DocTree tree : docCommentTree.getBlockTags()) {
                javadocPrinter.printf("<blocktag>%s</blocktag>\n", cleanupText(tree.toString()));
            }
            javadocPrinter.println("</blocktags>");
            javadocPrinter.println("</commenttree>");
        }
    }

    private PrintWriter openPrintWriter(Py5DocletOption docletOption) {
        PrintWriter printWriter = null;
        try {
            if (docletOption.filename != null) {
                printWriter = new PrintWriter(new File(docletOption.filename));
                reporter.print(Diagnostic.Kind.NOTE,
                        String.format("Writing %s to %s ", docletOption.getDescription(), docletOption.filename));
            }
        } catch (FileNotFoundException e) {
            reporter.print(Diagnostic.Kind.ERROR,
                    String.format("Param file %s cannot be written to", docletOption.filename));
        }
        return printWriter;
    }

    @Override
    public boolean run(DocletEnvironment docEnv) {
        javadocPrinter = openPrintWriter(javadocFileOption);

        if (javadocPrinter != null) {
            javadocPrinter.println("<?xml version=\"1.0\" standalone=\"yes\" ?>");
            javadocPrinter.println("<commenttrees>");
        }

        DocTrees docTrees = docEnv.getDocTrees();
        for (TypeElement t : ElementFilter.typesIn(docEnv.getIncludedElements())) {
            for (Element e : t.getEnclosedElements()) {
                processElement(docTrees, t.toString(), e);
            }
        }

        if (javadocPrinter != null) {
            javadocPrinter.println("</commenttrees>");
            javadocPrinter.close();
        }

        return true;
    }

    @Override
    public String getName() {
        return "Py5Doclet";
    }

    @Override
    public SourceVersion getSupportedSourceVersion() {
        return SourceVersion.latest();
    }

    @Override
    public Set<? extends Option> getSupportedOptions() {
        return new HashSet<Option>(Arrays.asList(new Option[] { javadocFileOption }));
    }
}
