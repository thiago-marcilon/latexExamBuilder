import pytest
import common.question as quest
import latex.profile as prof


class TestProfile:
    def test_dump_load(self):
        profile = prof.Profile('prof1', 'resources')
        profile.set_document_class('classname1', ('opt1', 'opt2'))
        profile.add_package('pckg1', ('opt1', 'opt2'))
        profile.add_package('pckg2', ())
        profile.add_question_environment('env1', 2, 4)
        profile.add_question_environment('env2', 0, 1)
        profile.preamble = 'thisisapreamble'
        profile.header = 'thisisaheader'
        profile.dump()
        profile2 = prof.Profile('prof1', 'resources')
        profile2.load()
        assert profile.document_class_name == profile2.document_class_name and \
               profile.document_class_options == profile2.document_class_options and \
               profile.preamble == profile2.preamble and profile.header == profile2.header and \
               profile.question_environment_list == profile2.question_environment_list and \
               profile.package_list == profile2.package_list

    def test_find_placeholders(self):
        assert prof.Profile.find_placeholders('%%thi%s%\ni%s\na%%%ph1 %\n%ok%') == {'s', 'ph1 ', 'ok'} and\
               prof.Profile.find_placeholders('t%hi%s\ni%%s%%\na%\n% header %th%') == {'hi', ' header '}

    def test_fill_preamble_header(self):
        profile = prof.Profile('prof1', 'resources')
        profile.set_document_class('classname1', ('opt1', 'opt2'))
        profile.add_package('pckg1', ('opt1', 'opt2'))
        profile.add_package('pckg2', ())
        profile.add_question_environment('env1', 2, 4)
        profile.add_question_environment('env2', 0, 1)
        profile.preamble = '% %thi%s%\ni%s\na%%%ph1 %\n%ok%'
        profile.header = 't%hi%s\ni%%s%%\na%\n% header %th%'
        assert profile.filled_preamble({'s': 's', 'ph1 ': 'preamble'}) == '% %this\ni%s\na%%preamble\n%ok%' and \
               profile.filled_header({'hi': ' ', 'notph': 'ignore', ' header ': 'header'}) == 't%hi%s\ni%%s%%\na%\nheaderth%'

    def test_add_question_environment(self):
        profile = prof.Profile('prof1')
        profile.add_question_environment('env1', 2, 3)
        assert len(profile.question_environment_list) == 1 and profile.question_environment_list[0][0] == 'env1' and \
               profile.question_environment_list[0][1] == (2, 3)
        profile.add_question_environment('env1', 4, 1)
        assert len(profile.question_environment_list) == 1 and profile.question_environment_list[0][0] == 'env1' and \
               profile.question_environment_list[0][1] == (4, 1)
        profile.add_question_environment('env2', 1, 3)
        assert len(profile.question_environment_list) == 2 and profile.question_environment_list[1][0] == 'env2' and \
               profile.question_environment_list[1][1] == (1, 3)

    def test_delete_question_environment(self):
        profile = prof.Profile('prof1')
        profile.add_question_environment('env1', 2, 3)
        profile.delete_question_environment('env1')
        assert len(profile.question_environment_list) == 0
        profile.add_question_environment('env1', 2, 3)
        profile.add_question_environment('env2')
        profile.delete_question_environment('env2')
        assert len(profile.question_environment_list) == 1
        profile.delete_question_environment('env1')
        assert len(profile.question_environment_list) == 0

    @pytest.mark.parametrize("name, options, options_expected", [("class1", 'opt1, opt2', ('opt1', 'opt2')),
                                                                 ("class2", ('opt1', 'opt2'), ('opt1', 'opt2')),
                                                                 ("class3", '', ())])
    def test_set_document_class(self, name, options, options_expected):
        profile = prof.Profile('prof1')
        profile.set_document_class(name, options)
        assert profile.document_class_name == name and set(profile.document_class_options) == set(options_expected)

    def test_add_package(self):
        profile = prof.Profile('prof1')
        profile.add_package('pckg1', 'opt1,  opt2')
        pckgs = profile.package_list
        assert len(pckgs) == 1 and pckgs[0][0] == 'pckg1' and set(pckgs[0][1]) == {'opt1', 'opt2'}
        profile.add_package('pckg2')
        pckgs = profile.package_list
        assert len(pckgs) == 2 and pckgs[1][0] == 'pckg2' and set(pckgs[1][1]) == set()
        profile.add_package('pckg1', ('opt1', 'opt3'))
        pckgs = profile.package_list
        assert len(pckgs) == 2 and pckgs[0][0] == 'pckg1' and set(pckgs[0][1]) == {'opt1', 'opt2', 'opt3'}

    def test_add_delete_package(self):
        profile = prof.Profile('prof1')
        profile.add_package('pckg1', 'opt1,  opt2')
        profile.delete_package('pckg1')
        assert len(profile.package_list) == 0
        profile.add_package('pckg1', 'opt1,  opt2')
        profile.add_package('pckg2')
        profile.delete_package('pckg1')
        assert len(profile.package_list) == 1
        profile.delete_package('pckg2')
        assert len(profile.package_list) == 0


class TestLatexQuestion:

    @pytest.mark.parametrize("question, environment_name, opt_options, mand_options, expected_dump",
                             [(quest.Question([], 'texttexttexttext', {}, ()), 'env1', ('opt1',), ('opt2', 'opt3'),
                               '\\begin{env1}[opt1]{opt2}{opt3}\ntexttexttexttext\n\\end{env1}'),
                              (quest.Question([], 'texttexttexttext', {}, ()), 'env1', ('opt1', 'opt2'), (),
                               '\\begin{env1}[opt1][opt2]\ntexttexttexttext\n\\end{env1}')
                              ])
    def test_dumps(self, question, environment_name, opt_options, mand_options, expected_dump):
        latex_question = prof.LatexQuestion(question, environment_name, opt_options, mand_options)
        assert latex_question.dumps() == expected_dump
