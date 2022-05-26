import pytest
import common.question as quest
import latex.profile as prof
import latex.latexpdfbuilder as bld
import os.path
import errno
import glob


@pytest.fixture(autouse=True, scope='class')
def context_class(request):
    profile = prof.Profile('profile_TestLatexPdfBuilder_dumps', 'resources')
    profile.set_document_class('article', ('oneside', '12pt', 'a4paper'))
    profile.add_package('float')
    profile.add_package('babel')
    profile.add_package('setspace')
    profile.add_question_environment('env1', 2, 4)
    profile.add_question_environment('env2', 0, 1)
    profile.preamble = '\\pagenumbering{gobble}\n\\setlength{\\parskip}{10 pt}\n\\newcounter{cquestion}\n' \
                       '\\newcommand{\\pts}{}\n' \
                       '\\newenvironment{question}[1][0]{\\refstepcounter{cquestion}\\par\\medskip\\noindent' \
                       '\\textbf{\\thecquestion)\\hspace{1pt}}' \
                       '\\renewcommand{\\pts}{#1}\\ifdim \\pts pt=0 pt\\hspace{3,1pt}\\fi}' \
                       '{\\ifdim \\pts pt>0 pt\\ifdim \\pts pt< 2 pt\\textbf{(\\pts{} pt)}' \
                       '\\else\\textbf{(\\pts{} pts)}\\fi\\else\\space\\fi}\n' \
                       '\\newcommand{\\university}{University of Testing Everything}\n' \
                       '\\newcommand{\\department}{Testing Software Department}\n' \
                       '\\newcommand{\\course}{Testing 101}\n' \
                       '\\newcommand{\\professor}{Dr. McNeeley}\n' \
                       '\\newcommand{\\dates}{%date%}'
    profile.header = '\\onehalfspacing\n' \
                     '\\noindent\\space\\\\\n' \
                     '\\textbf{\\university}\\\\\n' \
                     '\\textbf{Course:} \\course\\\\\n' \
                     '\\textbf{Professor:} \\professor\\\\\n' \
                     '\\textbf{Date:} \\dates\\\\\n' \
                     '\\vspace{15pt}\n' \
                     '\\begin{center}\n' \
                     '\\LARGE{\\textbf{Assessment %assess_number%}}\n' \
                     '\\end{center}\n' \
                     '\\vspace{10pt}\n'
    question1 = quest.Question(['key1', 'key2'], '\\hello \\bye', {'babel': ('brazilian', 'english')},
                               ('\\newcommand{\\hello}{Olá, Mundo!}', '\\newcommand{\\bye}{bye bye!}'))
    question2 = quest.Question(['key1', 'key3'],
                               'Consider the following graph:\n'
                               '\\begin{figure}[H]\n'
                               '\t\\centering\n'
                               '\t\\begin{tikzpicture}[auto]\n'
                               '\t\t\\tikzstyle{vertex}=[draw,circle,fill=black!25,minimum size=14pt,inner sep=1pt]\n'
                               '\t\t\\node[vertex] (v11) at (0,0) {$1$};\n'
                               '\t\t\\node[vertex] (v12) at (3,0) {$2$};\n'
                               '\t\t\\node[vertex] (v13) at (1.5,3) {$3$};\n'
                               '\t\t\\node[vertex] (v14) at (1.5,1.5) {$4$};\n'
                               '\t\t\\path[-] (v11) edge[below] node {$e_1$} (v12) edge[left] node[pos=0.5]'
                               ' {$e_2$} (v13) edge node[below] {$e_3$} (v14)\n'
                               '\t\t\t\t(v12) edge[right] node {$e_4$} (v13) edge[below] node[below,pos=0.8] {$e_5$} (v14);\n'
                               '\t\\end{tikzpicture}\n'
                               '\\end{figure}\n'
                               'Prove that it is not bipartite.',
                               {'tikz': (), 'float': (), 'babel': ('english',)}, ('\\newcommand{\\hello}{Olá, Mundo!}',))
    latex_questions = [prof.LatexQuestion(question1, 'question', (), ()),
                       prof.LatexQuestion(question2, 'question', ('1,5',), ())]
    fillers = {'date': '29/02/1600', 'assess_number': '1'}
    builder = bld.LatexPdfBuilder('profile_TestLatexPdfBuilder_dumps', 'resources', profile, latex_questions, fillers)

    dcs = ['\\documentclass[a4paper, 12pt, oneside]{article}\n',
           '\\documentclass[a4paper, oneside, 12pt]{article}\n',
           '\\documentclass[12pt, a4paper, oneside]{article}\n',
           '\\documentclass[12pt, oneside, a4paper]{article}\n',
           '\\documentclass[oneside, 12pt, a4paper]{article}\n',
           '\\documentclass[oneside, a4paper, 12pt]{article}\n']

    pcks = [
        '\\usepackage{float}\n\\usepackage[english, brazilian]{babel}\n\\usepackage{setspace}\n\\usepackage{tikz}\n',
        '\\usepackage{float}\n\\usepackage[brazilian, english]{babel}\n\\usepackage{setspace}\n\\usepackage{tikz}\n']

    pre1 = '\n' \
           '\\pagenumbering{gobble}\n' \
           '\\setlength{\\parskip}{10 pt}\n' \
           '\\newcounter{cquestion}\n' \
           '\\newcommand{\\pts}{}\n' \
           '\\newenvironment{question}[1][0]{\\refstepcounter{cquestion}\\par' \
           '\\medskip\\noindent\\textbf{\\thecquestion)\\hspace{1pt}}' \
           '\\renewcommand{\\pts}{#1}\\ifdim \\pts pt=0 pt\\hspace{3,1pt}\\fi}' \
           '{\\ifdim \\pts pt>0 pt\\ifdim \\pts pt< 2 pt\\textbf{(\\pts{} pt)}' \
           '\\else\\textbf{(\\pts{} pts)}\\fi\\else\\space\\fi}\n' \
           '\\newcommand{\\university}{University of Testing Everything}\n' \
           '\\newcommand{\\department}{Testing Software Department}\n' \
           '\\newcommand{\\course}{Testing 101}\n' \
           '\\newcommand{\\professor}{Dr. McNeeley}\n' \
           '\\newcommand{\\dates}{29/02/1600}\n' \
           '\n'
    defs = ['\\newcommand{\\hello}{Olá, Mundo!}\n\\newcommand{\\bye}{bye bye!}\n',
            '\\newcommand{\\bye}{bye bye!}\n\\newcommand{\\hello}{Olá, Mundo!}\n']
    pre2 = '\n' \
           '\\begin{document}\n' \
           '\\onehalfspacing\n' \
           '\\noindent\\space\\\\\n' \
           '\\textbf{\\university}\\\\\n' \
           '\\textbf{Course:} \\course\\\\\n' \
           '\\textbf{Professor:} \\professor\\\\\n' \
           '\\textbf{Date:} \\dates\\\\\n' \
           '\\vspace{15pt}\n' \
           '\\begin{center}\n' \
           '\\LARGE{\\textbf{Assessment 1}}\n' \
           '\\end{center}\n' \
           '\\vspace{10pt}\n' \
           '\n' \
           '\n' \
           '\\begin{question}\n' \
           '\\hello \\bye\n' \
           '\\end{question}\n' \
           '\n' \
           '\\begin{question}[1,5]\n' \
           'Consider the following graph:\n' \
           '\\begin{figure}[H]\n' \
           '\t\\centering\n' \
           '\t\\begin{tikzpicture}[auto]\n' \
           '\t\t\\tikzstyle{vertex}=[draw,circle,fill=black!25,minimum size=14pt,inner sep=1pt]\n' \
           '\t\t\\node[vertex] (v11) at (0,0) {$1$};\n' \
           '\t\t\\node[vertex] (v12) at (3,0) {$2$};\n' \
           '\t\t\\node[vertex] (v13) at (1.5,3) {$3$};\n' \
           '\t\t\\node[vertex] (v14) at (1.5,1.5) {$4$};\n' \
           '\t\t\\path[-] (v11) edge[below] node {$e_1$} (v12) edge[left] node[pos=0.5] {$e_2$} (v13) edge node[below] {$e_3$} (v14)\n' \
           '\t\t\t\t(v12) edge[right] node {$e_4$} (v13) edge[below] node[below,pos=0.8] {$e_5$} (v14);\n' \
           '\t\\end{tikzpicture}\n' \
           '\\end{figure}\n' \
           'Prove that it is not bipartite.\n' \
           '\\end{question}\n' \
           '\n' \
           '\\end{document}\n'

    expected_dumps = []
    for s1 in dcs:
        for s2 in pcks:
            for s3 in defs:
                expected_dumps.append(s1 + s2 + pre1 + s3 + pre2)
    request.cls.builder, request.cls.expected_dumps = builder, tuple(expected_dumps)


@pytest.mark.usefixtures("context_class")
class TestLatexPdfBuilder:

    def test_build_dumps(self):
        assert self.builder.dumps() in self.expected_dumps

    def test_generate_tex(self):
        self.builder.generate_tex()
        assert os.path.getsize(self.builder.fullpath + ".tex") == 1741
        with open(self.builder.fullpath + ".tex", encoding="utf-8") as tex:
            file_dumps = tex.read()
        assert file_dumps in self.expected_dumps
        os.remove(self.builder.fullpath + '.tex')

    def test_generate_pdf(self):
        try:
            self.builder.generate_tex()
            self.builder.generate_pdf()
            assert os.path.exists(self.builder.fullpath + ".pdf") and os.path.isfile(self.builder.fullpath + ".pdf")
        finally:
            extensions = ['aux', 'log', 'out', 'fls', 'bib']
            os.remove(self.builder.fullpath + ".tex")
            os.remove(self.builder.fullpath + ".pdf")
            for ext in extensions:
                try:
                    for file in glob.glob(os.path.abspath(os.path.join(self.builder.path, '*.' + ext))):
                        os.remove(file)
                except FileNotFoundError as e:
                    if e.errno != errno.ENOENT:
                        raise
