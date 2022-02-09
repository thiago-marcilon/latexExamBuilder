import tinydb as tdb
import tinydb.table as tdb_table

MimeTypeQuestions = 'application/x-qt-windows-mime;value="Questions"'
MimeTypeQuestionsIndexes = 'application/x-qt-windows-mime;value="QuestionsIndexes"'


class Question:
    """The Question object represents the question itself."""

    def __init__(self, keywords=None, text='', packages_req=None, custom_defs=(), doc=None):
        """
        :param keywords: keywords for the question.
        :type keywords: list of str
        :param text: the question text.
        :type text: str
        :param packages_req: required latex packages and their options.
        :type packages_req: dict [str, tuple of str]
        :param custom_defs: required custom commands and other definitions.
        :type custom_defs: tuple of str
        :param doc: database document from which to load the attributes
        :type doc: :py:class:`tdb.database.Document`
        """
        self.doc_id = 0
        self.keywords = keywords
        if keywords is None:
            self.keywords = []
        self.text = text
        self.packages_req = packages_req
        if packages_req is None:
            self.packages_req = {}
        self.custom_defs = custom_defs
        if doc is not None:
            self.load(doc)

    def __eq__(self, other):
        return self.text == other.text

    def __hash__(self):
        return hash(self.text)

    def in_database(self):
        """Returns whether a question is currently in the database.

        :return: True if it is currently in the database. False if not.
        :rtype: bool
        """
        return self.doc_id > 0

    def load(self, doc):
        """Assigns the contents of doc to the attributes of this object.

        :param doc: An object that represents an entry in the database
        :type doc: tdb_table.Document
        """
        if all(key in doc for key in ('keywords', 'text', 'packages_req', 'custom_defs')):
            self.doc_id = doc.doc_id
            self.keywords = doc['keywords']
            self.text = doc['text']
            self.packages_req = dict([(key, tuple(val)) for key, val in doc['packages_req'].items()])
            self.custom_defs = tuple(doc['custom_defs'])

    def load_from_dict(self, dic):
        """Assigns the contents of dic to the attributes of this object.

        :param dic: A dictionary that represents a question.
        :type dic: dict
        """
        if all(key in dic for key in ('keywords', 'text', 'packages_req', 'custom_defs', 'doc_id')):
            self.doc_id = dic['doc_id']
            self.keywords = dic['keywords']
            self.text = dic['text']
            self.packages_req = dic['packages_req']
            self.custom_defs = dic['custom_defs']

    def dict(self):
        """Assigns the attributes of this object, except the doc_id, to a dictionary.

        :return: A dictionary that represents this question.
        :rtype: dict
        """
        return {"keywords": self.keywords, "text": self.text,
                "packages_req": self.packages_req, "custom_defs": self.custom_defs}

    def dict_with_id(self):
        """Assigns the attributes of this object to a dictionary.

        :return: A dictionary that represents this question.
        :rtype: dict
        """
        return {"keywords": self.keywords, "text": self.text,
                "packages_req": self.packages_req, "custom_defs": self.custom_defs, "doc_id": self.doc_id}
