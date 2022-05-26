import os
import tempfile
import subprocess
import errno
import asyncio
import latex.profile as prof
import common.settings as setts


class LatexCompileError(Exception):
    pass


class LatexPdfBuilder:
    """The LatexPdfBuilder object's function is to generate LaTeX documents and pdfs and preview pdfs."""

    def __init__(self, name, path, profile=None, latex_questions=None, fillers=None):
        """
        :param name: the name of the generated .tex and .pdf files.
        :type name: str
        :param path: the default path of the generated .tex and .pdf files.
        :type path: str
        :param profile: profile of the generated .tex file.
        :type profile: :py:class:`prof.Profile`
        :param latex_questions: questions to be added to the .tex file.
        :type latex_questions: list of prof.LatexQuestion
        :param fillers: dictionary mapping placeholders in the profile's preamble and header to their fillers.
        :type fillers: dict [str, str]
        """
        self.name = name
        self.path = path
        self.profile = profile
        self.latex_questions = latex_questions
        self.fillers = fillers
        if self.fillers is None:
            self.fillers = {}

    @property
    def fullpath(self):
        """The full path of the documents without the extension tex or pdf."""
        return os.path.abspath(os.path.join(self.path, self.name))

    async def pdf_preview(self, filepath=None):
        """Opens the pdf with the reader selected in the settings.

        :param filepath: The name of the file without the .pdf to be opened. If it is None, the
            default path will be selected.
        :type filepath: str
        """
        if not setts.pdf_viewer_path:
            raise LatexCompileError("Pdf viewer application is not set.")
        elif not os.path.isfile(setts.pdf_viewer_path):
            raise LatexCompileError("Pdf viewer not found in the specified path.")
        path = self.__select_filepath(filepath)
        proc = await asyncio.create_subprocess_exec(setts.pdf_viewer_path, path + '.pdf')
        await proc.wait()

    async def temp_pdf_preview(self):
        """Builds a temporary tex and pdf of the document and opens the pdf with the reader selected in the settings."""
        if not setts.pdf_viewer_path:
            raise LatexCompileError("Pdf viewer application is not set.")
        elif not os.path.isfile(setts.pdf_viewer_path):
            raise LatexCompileError("Pdf viewer not found in the specified path.")
        with tempfile.TemporaryDirectory('_dir', 'temp_', './/', True) as tmpdirname:
            fullpath = os.path.abspath(os.path.join(tmpdirname, self.name))
            self.generate_tex(fullpath)
            self.generate_pdf(fullpath)
            proc = await asyncio.create_subprocess_exec(setts.pdf_viewer_path, fullpath + '.pdf')
            await proc.wait()

    def dumps(self):
        """Builds the document as a string in LaTeX syntax.

        :return: the string that represents the latex document.
        :rtype: str
        """
        if self.profile.document_class_options:
            latex_string = f'\\documentclass[{", ".join(self.profile.document_class_options)}]' \
                           f'{{{self.profile.document_class_name}}}\n'
        else:
            latex_string = f'\\documentclass{{{self.profile.document_class_name}}}\n'

        packages = {}
        for pckg_name, pckg_options in self.profile.package_list:
            packages[pckg_name] = packages.get(pckg_name, set()) | set(pckg_options)

        custom_defs = set()
        for latex_question in self.latex_questions:
            for pckg_name, pckg_options in latex_question.packages_req:
                packages[pckg_name] = packages.get(pckg_name, set()) | set(pckg_options)
            custom_defs.update(set(latex_question.custom_defs))

        for name, options in packages.items():
            if options != set():
                latex_string += f'\\usepackage[{", ".join(options)}]{{{name}}}\n'
            else:
                latex_string += f'\\usepackage{{{name}}}\n'
        preamble = '\n' + self.profile.filled_preamble(self.fillers) + '\n\n'
        for definition in custom_defs:
            preamble += definition + '\n'
        if custom_defs:
            preamble += '\n'

        latex_string += f'{preamble}\\begin{{document}}\n'
        latex_string += f'{self.profile.filled_header(self.fillers)}\n'
        for q in self.latex_questions:
            latex_string += f'\n{q.dumps()}\n'
        latex_string += '\n\\end{document}\n'
        return latex_string

    def __select_filepath(self, filepath=None):
        """Selects the filepath based in the parameter filepath and the property self.fullpath.

        :param filepath: The name of the file without the .pdf. If it is None, the
            default path will be selected.
        :type filepath: str
        """
        if filepath is None:
            filepath = self.fullpath
        elif os.path.basename(filepath) == '':
            filepath = os.path.abspath(os.path.join(filepath, self.name))
        return os.path.abspath(filepath)

    def generate_tex(self, filepath=None):
        """Generates the tex file from the document.

        :param filepath: The name of the file without the .pdf. If it is None, the
            default path will be used.
        :type filepath: str
        """
        if self.profile is not None and self.latex_questions is not None:
            filepath = self.__select_filepath(filepath)
            with open(filepath + '.tex', 'w', encoding='utf-8') as texfile:
                texfile.write(self.dumps())

    def generate_pdf(self, filepath=None, *, compiler_args=None):
        """Generates the pdf file from the document.

        :param filepath: The name of the file without the .pdf. If it is None, the
            default path will be used.
        :type filepath: str
        :param compiler_args: Extra arguments that should be passed to the LaTeX compiler. If
            this is None it defaults to an empty list.
        :type compiler_args: list[str] or None
        """
        if compiler_args is None:
            compiler_args = []
        filepath = self.__select_filepath(filepath)
        dest_dir = os.path.dirname(filepath)
        compiler = 'pdflatex'
        main_arguments = ['--interaction=nonstopmode', filepath + '.tex']
        check_output_kwargs = {'cwd': dest_dir, 'text': True}
        command = [compiler] + compiler_args + main_arguments
        try:
            subprocess.check_output(command, stderr=subprocess.STDOUT, **check_output_kwargs)
        except subprocess.CalledProcessError as err:
            if err.output.find('! ') >= 0:
                raise (LatexCompileError(
                    '\n'.join([line for line in err.output.split('\n') if line.startswith('! ')])))
            raise
        except FileNotFoundError as err:
            if err.errno == errno.ENOENT:
                raise (LatexCompileError('Pdflatex not found! Make sure you have pdfLaTex installed.'))
            raise
