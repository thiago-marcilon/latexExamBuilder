import os
import os.path
import PyQt5.QtCore as qcore
import json
import latex.profile as prof

profile_file_max_size = 1024 ** 3
profile_default_path = os.path.abspath('./profiles')
settings_file_name = 'settings'

preview_profile_document_class = 'article'
preview_profile_document_options = ('oneside', 'a4paper', '10pt')
preview_profile_packages_required = {}
preview_profile_preamble = r'\newenvironment{question}{' \
                           r'\noindent' \
                           r'}' \
                           r'{' \
                           r'\\\\' \
                           r'}'
preview_profile_header = ''
preview_profile_environments = {"question": (0, 0)}


def search_path(oss, name_path_list):
    sep = '\\' if oss == 'win' else '/'
    for name, path_list in name_path_list:
        for path in path_list:
            path = path.split(sep)[1:]
            current = os.path.abspath(os.sep)
            for index, pathd in enumerate(path):
                for dirc in os.listdir(current):
                    if os.path.exists(os.path.join(current, dirc)) and dirc.startswith(pathd):
                        if index < len(path) - 1 or oss != 'win' or dirc.endswith('.exe'):
                            current = os.path.join(current, dirc)
                            break
                else:
                    break
            else:
                return current
    return ''


def search_pdf_viewers():
    """Tries to find the path to a pdf reader.

    :return: the path to a pdf reader or an empty string if it does not succeed in finding one.
    :rtype: str
    """
    op_sys = qcore.QSysInfo.productType()
    kernel = qcore.QSysInfo.kernelType()
    if op_sys == 'windows' or op_sys == 'winrt':
        return search_path('win',
                           [('Acrobat Reader', [rf'{os.environ["PROGRAMFILES"]}\Adobe\Acrobat\Acrobat\Acrobat.exe']),
                            ('Foxit Reader',
                             [rf'{os.environ["PROGRAMFILES"]}\Foxit Software\Foxit Reader\FoxitReader.exe'])])
    elif kernel == 'linux':
        return search_path('linux',
                           [('Foxit Reader', [rf'{os.environ["HOME"]}/opt/foxitsoftware/foxitreader/FoxitReader',
                                              rf'/opt/foxitsoftware/foxitreader/FoxitReader'])])
    return ''


pdf_viewer_path = search_pdf_viewers()


def load_preview_profile(profile):
    """Loads the contents of the profile to the setting variables regarding the preview profile.

    :param profile: profile to be used when previewing pdfs.
    :type profile: prof.Profile
    """
    global preview_profile_document_class, preview_profile_document_options, preview_profile_packages_required, \
        preview_profile_preamble, preview_profile_header, preview_profile_environments
    preview_profile_document_class = profile.document_class_name
    preview_profile_document_options = profile.document_class_options
    preview_profile_packages_required = dict(profile.package_list)
    preview_profile_preamble = profile.preamble
    preview_profile_header = profile.header
    preview_profile_environments = dict(profile.question_environment_list)


def dump():
    """Stores the contents of the setting variables to the file with name in the settings_file_name variable"""
    global profile_file_max_size, profile_default_path, pdf_viewer_path, \
        preview_profile_document_class, preview_profile_document_options, preview_profile_packages_required, \
        preview_profile_preamble, preview_profile_header, preview_profile_environments
    json_dict = {"profile_file_max_size": profile_file_max_size, "profile_default_path": profile_default_path,
                 "pdf_viewer_path": pdf_viewer_path, "preview_profile_document_class": preview_profile_document_class,
                 "preview_profile_document_options": preview_profile_document_options,
                 "preview_profile_packages_required": preview_profile_packages_required,
                 "preview_profile_preamble": preview_profile_preamble, "preview_profile_header": preview_profile_header,
                 "preview_profile_environments": preview_profile_environments}
    with open(os.path.abspath(settings_file_name), 'w', encoding="utf-8") as profile_file:
        json.dump(json_dict, profile_file, ensure_ascii=False)


def load():
    """Loads the contents of the file with name in the settings_file_name variable to the setting variables"""
    global profile_file_max_size, profile_default_path, pdf_viewer_path, settings_file_name, \
        preview_profile_document_class, preview_profile_document_options, preview_profile_packages_required, \
        preview_profile_preamble, preview_profile_header, preview_profile_environments
    if not os.path.exists(os.path.abspath(os.path.join('./', settings_file_name))):
        dump()
    else:
        with open(settings_file_name, 'r', encoding="utf-8") as settings_file:
            json_dict = json.load(settings_file)
        profile_file_max_size = json_dict.get('profile_file_max_size', profile_file_max_size)
        profile_default_path = json_dict.get('profile_default_path', profile_default_path)
        pdf_viewer_path = json_dict.get('pdf_viewer_path', pdf_viewer_path)
        preview_profile_document_class = json_dict.get('preview_profile_document_class', preview_profile_document_class)
        preview_profile_document_options = json_dict.get('preview_profile_document_options', preview_profile_document_options)
        preview_profile_packages_required = json_dict.get('preview_profile_packages_required', preview_profile_packages_required)
        preview_profile_preamble = json_dict.get('preview_profile_preamble', preview_profile_preamble)
        preview_profile_header = json_dict.get('preview_profile_header', preview_profile_header)
        preview_profile_environments = json_dict.get('preview_profile_environments', preview_profile_environments)
