import common.question as quest
import tinydb as tdb
import os.path
import re


class DBHandler:
    """The DBHandler object handles the question database. It interfaces with TinyDB to manage the questions."""

    def __init__(self, fullpath):
        """
        :param fullpath: full path of the database file
        :type fullpath: str
        """
        self.__fullpath = os.path.abspath(fullpath)
        self.__db = tdb.TinyDB(self.fullpath, ensure_ascii=False)

    @property
    def fullpath(self):
        """Represents the full path of the database file.

        :rtype: str
        """
        return self.__fullpath

    def close(self):
        """Closes the database"""
        self.__db.close()

    def upsert(self, question):
        """Inserts or updates a question in the database.
        If the question is not in the database, it is inserted. Otherwise, it is updated.

        :param question: question to be added.
        :type question: :py:class:`quest.Question` or list[:py:class:`quest.Question`]
        """
        if not question.in_database():
            doc_id_list = self.__db.upsert(question.dict(), tdb.where("text") == question.text)
            # if len(doc_id_list) > 1, a crime has been committed! Someone managed
            # to manually insert two or more questions with the exact same text
            # into the database, which shouldn't happen.
            question.doc_id = doc_id_list[0]
        else:
            self.__db.upsert(tdb.database.Document(question.dict(), doc_id=question.doc_id))

    def remove(self, question_list):
        """Removes a question or a list of questions from the database.

        :param question_list: list of questions to be removed.
        :type question_list: :py:class:`quest.Question` or list[:py:class:`quest.Question`]
        """
        if not isinstance(question_list, list):
            question_id_list = [question_list]
        self.__db.remove(doc_ids=[question.doc_id for question in question_list if question.doc_id > 0])
        for question in question_list:
            question.doc_id = 0

    def clear(self):
        """Removes all questions from the database."""
        self.__db.truncate()

    def __len__(self):
        """Length of the database"""
        return len(self.__db)

    def get_all(self):
        """Gets the list of all questions from the database.

        :return: the list of all questions.
        :rtype: list of :py:class:`quest.Question`
        """
        questions_doc_list = self.__db.all()
        return [quest.Question(doc=question_doc) for question_doc in questions_doc_list]

    def get_by_text(self, text):
        """Gets the list of questions from the database that has the parameter
        :py:param:`text` as a substring of its text.

        :param text: the text a question must contain as a substring to be selected.
        :type text: str
        :return: the list of selected questions.
        :rtype: list of :py:class:`quest.Question`
        """
        question_query = tdb.Query()
        questions_doc_list = self.__db.search(question_query['text'].search(re.escape(text), flags=re.IGNORECASE))
        return [quest.Question(doc=question_doc) for question_doc in questions_doc_list]

    def get_by_keywords(self, conditions):
        """Gets the list of questions from the database that matches the parameter :py:param:`conditions`.

        :param conditions: the conditions a question must satisfy to be selected.
            An example for this parameter is
            [[(True,'key1'),(False,'key2')],[(True,'key3')],[(True,'key4'),(False,'key5'),(False,'key6')]],
            which means that a question must be selected if it:
            (has 'key1' and does not have 'key2' in its keywords)
            or (has 'key3' in its keywords)
            or (has 'key4' and does not have 'key5' and 'key6' in its keywords). If it is None, returns all
            in the database.
        :type conditions: list [list [tuple [bool, str]]]
        :return: the list of selected questions.
        :rtype: list of :py:class:`quest.Question`
        """
        question_query = tdb.Query()

        def search(keywords):
            setkeys = set([key.lower() for key in keywords])
            for conjunction in conditions:
                for is_in, keyword in conjunction:
                    if is_in:
                        if keyword.lower() not in setkeys:
                            break
                    elif keyword.lower() in setkeys:
                        break
                else:
                    return True
            return False
        questions_doc_list = self.__db.search(question_query['keywords'].test(search))
        return [quest.Question(doc=question_doc) for question_doc in questions_doc_list]
