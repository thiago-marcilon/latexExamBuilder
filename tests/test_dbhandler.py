import common.question as quest
import database.dbhandler as dbh
import os
import pytest


@pytest.fixture(autouse=True, scope='class')
def context_class(request):
    try:
        os.remove(os.path.abspath(os.path.join("", 'test_db.json')))
    except FileNotFoundError:
        pass
    finally:
        request.cls.db = dbh.DBHandler('./test_db.json')
        request.cls.questions = [quest.Question(['key1', 'key2'], 'texttexttext',
                                                {"pckg1": ('opt1', 'opt2'), "pckg2": ()}, ('def1', 'def2')),
                                 quest.Question(['key1', 'key3'], 'texttexttext2',
                                                {"pckg1": ('opt1',), "pckg2": ('opt2',)}, ()),
                                 quest.Question(['key2'], 'texttexttext3', {}, ('def3',))]
        yield
        fullpath = request.cls.db.fullpath
        request.cls.db.close()
        os.remove(fullpath)


@pytest.fixture(autouse=True, scope='function')
def context_method(request):
    yield
    request.cls.db.clear()


@pytest.mark.usefixtures("context_class", "context_method")
class TestDBHandler:

    def upsert_all_questions(self):
        self.db.upsert(self.questions[0])
        self.db.upsert(self.questions[1])
        self.db.upsert(self.questions[2])

    def test_upsert_question(self):
        self.db.upsert(self.questions[0])
        self.db.upsert(self.questions[1])
        question_list = self.db.get_all()
        assert len(question_list) == 2 and set(question_list) == set(self.questions[0:2])
        self.upsert_all_questions()
        question_list = self.db.get_all()
        assert len(question_list) == 3 and set(question_list) == set(self.questions)
        self.questions[2].text = 'testtesttest3'
        self.db.upsert(self.questions[2])
        question_list = self.db.get_all()
        assert len(question_list) == 3 and set(question_list) == set(self.questions)

    def test_remove_question(self):
        self.upsert_all_questions()
        self.db.remove([self.questions[0], self.questions[1]])
        assert len(self.db) == 1 and self.db.get_all()[0].doc_id == self.questions[2].doc_id
        self.db.remove([self.questions[0]])
        self.db.remove([self.questions[2]])
        assert len(self.db) == 0

    def test_clear(self):
        self.upsert_all_questions()
        self.db.clear()
        assert len(self.db) == 0

    def test_get_all(self):
        assert set() == set(self.db.get_all())
        self.upsert_all_questions()
        assert set(self.questions) == set(self.db.get_all())

    def test_get_by_text(self):
        question_list = self.db.get_by_text("noquestionissupossedtomatchthis")
        assert len(question_list) == 0
        self.upsert_all_questions()
        question_list = self.db.get_by_text(self.questions[1].text[4:])
        assert len(question_list) == 1 and self.questions[1] == question_list[0]

    def test_get_by_keywords(self):
        question_set1 = {self.questions[0], self.questions[1]}
        question_set2 = {self.questions[0], self.questions[2]}
        question_set3 = {self.questions[2]}
        self.upsert_all_questions()
        assert set(self.questions) == set(self.db.get_all())
        assert question_set1 == set(self.db.get_by_keywords([[(True, 'key1')]]))
        assert question_set2 == set(self.db.get_by_keywords([[(True, 'key2')]]))
        assert question_set3 == set(self.db.get_by_keywords([[(True, 'key2'), (False, 'key1')]]))
        assert question_set2 == set(self.db.get_by_keywords([[(True, 'notkey')], [(True, 'key1'), (False, 'key3')],
                                                             [(True, 'key2')]]))
