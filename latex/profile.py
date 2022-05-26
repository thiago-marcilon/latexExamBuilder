import os
import os.path
import json
import stat

import common.settings as setts
import common.question as quest


class Profile:
    """The Profile object represents the entire context which he questions are inserted."""

    def __init__(self, name, path=None):
        """
        :param name: the name of the profile. Also, the name of its file.
        :type name: str
        :param path: the file's path.
        :type path: str
        """
        if path is None:
            self.__path = setts.profile_default_path
        else:
            self.__path = os.path.abspath(path)
        self.__name = name
        self.__preamble_placeholders = set()
        self.__header_placeholders = set()
        self.__preamble = ''
        self.__header = ''
        self.__packages = {}
        self.__question_environments = {}
        self.__document_class_name = ''
        self.__document_class_options = ()

    @classmethod
    def preview(cls):
        """Builds the profile used for previewing pdfs.

        :return: The profile used for previewing pdfs.
        :rtype: Profile
        """
        profile = cls('preview', os.path.abspath('./'))
        profile.set_document_class(setts.preview_profile_document_class, setts.preview_profile_document_options)
        for pckg, options in setts.preview_profile_packages_required.items():
            profile.add_package(pckg, options)
        profile.preamble = setts.preview_profile_preamble
        profile.header = setts.preview_profile_header
        for env, options in setts.preview_profile_environments.items():
            profile.add_question_environment(env, options[0], options[1])
        return profile

    @property
    def preamble(self):
        """Profile's preamble."""
        return self.__preamble

    @preamble.setter
    def preamble(self, preamble):
        self.__preamble_placeholders = self.find_placeholders(preamble)
        self.__preamble = preamble

    @property
    def header(self):
        """Profile's header."""
        return self.__header

    @header.setter
    def header(self, header):
        self.__header_placeholders = self.find_placeholders(header)
        self.__header = header

    @property
    def placeholders(self):
        """Profile's preamble's and header's placeholders."""
        return self.__preamble_placeholders | self.__header_placeholders

    def filled_preamble(self, fillers):
        """Fills preamble's placeholders.

        :param fillers: dictionary mapping placeholders to their fillers. If a filler is empty, its respective
         placeholder remains unchanged.
        :type fillers: dict [str, str]
        :return: the string consisting of the preamble filled according to fillers.
        :rtype: str
        """
        preamble = self.preamble
        if fillers is not None:
            for ph, fill in fillers.items():
                if ph in self.__preamble_placeholders and fill.strip() != '':
                    preamble = preamble.replace('%'+ph+'%', fill)
        return preamble

    def filled_header(self, fillers):
        """Fills header's placeholders.

        :param fillers: dictionary mapping placeholders to their fillers. If a filler is empty, its respective
         placeholder remains unchanged.
        :type fillers: dict [str, str]
        :return: the string consisting of the header filled according to fillers.
        :rtype: str
        """
        header = self.header
        if fillers is not None:
            for ph, fill in fillers.items():
                if ph in self.__header_placeholders and fill.strip() != '':
                    header = header.replace('%'+ph+'%', fill)
        return header

    @classmethod
    def find_placeholders(cls, text):
        """Find all placeholders in text."""
        ret = set()
        i = 0
        length = len(text)
        while i < length:
            if text[i] == '%':
                placeholder_name = ''
                i += 1
                while i < length and text[i] != '\n' and text[i] != '%':
                    placeholder_name += text[i]
                    i += 1
                if i < length and text[i] == '%' and placeholder_name.strip() != '':
                    ret.add(placeholder_name)
            i += 1
        return ret

    def load(self):
        """Load the contents of the profile file represented by this object."""
        filepath = os.path.abspath(os.path.join(self.__path, self.__name + '.prof'))
        size = os.path.getsize(filepath)
        if not size <= setts.profile_file_max_size:
            raise MemoryError(
                f'''Profile {filepath} file size({size}) exceeds max size ({setts.profile_file_max_size})''')
        with open(filepath, 'r', encoding="utf-8") as profile_file:
            profile_dict = json.load(profile_file)
        self.__document_class_name = profile_dict["document_class_name"]
        self.__document_class_options = tuple(profile_dict["document_class_options"])
        self.header = profile_dict["header"]
        self.preamble = profile_dict["preamble"]
        self.__question_environments = dict(
            [(name, tuple(options)) for name, options in profile_dict["question_environments"].items()])
        self.__packages = dict([(name, tuple(options)) for name, options in profile_dict["packages"].items()])

    def dump(self):
        """Stores the contents of this object in its profile file."""
        if not os.path.isdir(os.path.abspath(self.__path)):
            os.mkdir(os.path.abspath(self.__path), stat.S_IRWXG | stat.S_IRWXU)
        filepath = os.path.abspath(os.path.join(self.__path, self.__name + '.prof'))
        json_dict = {"packages": self.__packages, "document_class_name": self.document_class_name,
                     "document_class_options": self.document_class_options, "preamble": self.preamble,
                     "question_environments": self.__question_environments, "header": self.header}
        with open(filepath, 'w', encoding="utf-8") as profile_file:
            json.dump(json_dict, profile_file, ensure_ascii=False)

    def add_question_environment(self, name, opt_opt_qty=0, mand_args_qty=0):
        """Adds a new question environment to the profile.

        :param name: name of the environment
        :type name: str
        :param opt_opt_qty: Number of optional arguments
        :type opt_opt_qty: int
        :param mand_args_qty: Number of mandatory arguments
        :type mand_args_qty: int
        """
        self.__question_environments[name] = (opt_opt_qty, mand_args_qty)

    def delete_question_environment(self, name):
        """Removes a question environment to the profile.

        :param name: name of the environment to be removed
        :type name: str
        """
        self.__question_environments.pop(name, ())

    @property
    def name(self):
        """Represents the name of the profile.

        :rtype: str
        """
        return self.__name

    @property
    def question_environment_list(self):
        """Represents the list of question environments in this profile.

        :rtype: list [tuple [str, tuple [int, int]]]
        """
        return [(name, options) for name, options in self.__question_environments.items()]

    def set_document_class(self, name, options=()):
        """Sets the current document class name and options of this profile.

        :param name: name of the document class
        :type name: str
        :param options: options for the document class
        :type options: tuple of str
        """
        self.__document_class_name = name
        if options == '':
            options = ()
        if isinstance(options, str):
            options = (s.strip() for s in options.split(','))
        self.__document_class_options = tuple(set(options))

    @property
    def document_class_name(self):
        """Represents the profile's document class name.

        :rtype: str
        """
        return self.__document_class_name

    @property
    def document_class_options(self):
        """Represents the profile's document class options.

        :rtype: tuple[str]
        """
        return self.__document_class_options

    @property
    def package_list(self):
        """Represents the list of required packages in this profile.

        :rtype: list [tuple [str, tuple of str]]
        """
        return [(name, options) for name, options in self.__packages.items()]

    def add_package(self, name, options=()):
        """Adds a new required package to this profile.

        :param name: name of the package
        :type name: str
        :param options: options of the package
        :type options: tuple of str
        """
        if options == '':
            options = ()
        if isinstance(options, str):
            options = (s.strip() for s in options.split(','))
        self.__packages[name] = tuple(set(self.__packages.get(name, ()) + tuple(options)))

    def delete_package(self, name):
        """Removes a required package of this profile.

        :param name: name of the package
        :type name: str
        """
        self.__packages.pop(name, '')


class LatexQuestion:
    """The LatexQuestion object represents an object of the class Question in the context of an environment."""

    def __init__(self, question, question_environment, opt_opts=(), mand_opts=()):
        """
        :param question: the underlining question.
        :type question: :py:class:`quest.Question`
        :param question_environment: environment of the question.
        :type question_environment: str
        :param opt_opts: optional options to the environment.
        :type opt_opts: tuple of str
        :param mand_opts: mandatory options to the environment.
        :type mand_opts: tuple of str
        """
        self.question = question
        self.question_environment = question_environment
        self.optional_options = opt_opts
        self.mandatory_options = mand_opts

    def dumps(self):
        """Builds the question as a string in LaTeX syntax.

        :return: the string that represents the question in LaTeX syntax.
        :rtype: str
        """
        latex_string = '\\begin{' + self.question_environment + '}'
        if self.optional_options:
            latex_string += '[' + ']['.join(self.optional_options) + ']'
        if self.mandatory_options:
            latex_string += '{' + '}{'.join(self.mandatory_options) + '}'
        latex_string += '\n' + self.question.text + '\n'
        latex_string += '\\end{' + self.question_environment + '}'
        return latex_string

    @property
    def packages_req(self):
        """Represents the question's required packages.

        :return: the list with the question's required packages.
        :rtype: list [tuple[str, tuple of str]]
        """
        return self.question.packages_req.items()

    @property
    def custom_defs(self):
        """Represents the question's required custom definitions.

        :return: the tuple with the question's required custom definitions.
        :rtype: tuple of str
        """
        return self.question.custom_defs
