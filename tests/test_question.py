import pytest
import tinydb.table as tdb_table
import common.question as quest
import copy


@pytest.fixture(autouse=True, scope='class')
def context_class(request):
    request.cls.dict_value = {'keywords': ['key1', 'key2'], 'text': 'texttexttext',
                              'packages_req': {"pckg1": ('opt1', 'opt2'), "pckg2": ()}, 'custom_defs': ('def1', 'def2')}


@pytest.mark.usefixtures("context_class")
class TestQuestion:
    def test_in_database(self):
        question = quest.Question(['key1', 'key2'], 'texttexttext',
                                  {"pckg1": ('opt1', 'opt2'), "pckg2": ()}, ('def1', 'def2'))
        assert not question.in_database()

    def test_load(self):
        doc = tdb_table.Document(self.dict_value, 1)
        question1 = quest.Question(doc=doc)
        assert question1.doc_id == 1
        assert question1.keywords == ['key1', 'key2']
        assert question1.text == 'texttexttext'
        assert question1.packages_req == {"pckg1": ('opt1', 'opt2'), "pckg2": ()}
        assert question1.custom_defs == ('def1', 'def2')
        question2 = quest.Question()
        question2.load(doc)
        assert question2.doc_id == 1
        assert question2.keywords == ['key1', 'key2']
        assert question2.text == 'texttexttext'
        assert question2.packages_req == {"pckg1": ('opt1', 'opt2'), "pckg2": ()}
        assert question2.custom_defs == ('def1', 'def2')

    def test_load_from_dict(self):
        question = quest.Question()
        dictionary = copy.deepcopy(self.dict_value)
        dictionary['doc_id'] = 1
        question.load_from_dict(dictionary)
        assert question.doc_id == 1
        assert question.keywords == ['key1', 'key2']
        assert question.text == 'texttexttext'
        assert question.packages_req == {"pckg1": ('opt1', 'opt2'), "pckg2": ()}
        assert question.custom_defs == ('def1', 'def2')

    def test_dict(self):
        question = quest.Question()
        dictionary = copy.deepcopy(self.dict_value)
        dictionary['doc_id'] = 1
        question.load_from_dict(dictionary)
        assert question.dict() == self.dict_value

    def test_dict_with_id(self):
        question = quest.Question()
        dictionary = copy.deepcopy(self.dict_value)
        dictionary['doc_id'] = 1
        question.load_from_dict(dictionary)
        assert question.dict_with_id() == dictionary
