import PyQt5.QtCore as qcore
import database.dbhandler as dtb
import common.question as ques


class DBModel(qcore.QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)
        self.__headers_text = ['Id', 'Keywords', 'Question Text', '', '']
        self.__dbhandler = None
        self.__question_list = []
        self.__font_size = 8

    def remove(self, indxmodel_list):
        indx_list = [item.row() for item in indxmodel_list]
        indx_list = sorted(indx_list, reverse=True)
        question_list_remove = [self.__question_list[indx] for indx in indx_list]
        self.__dbhandler.remove(question_list_remove)
        for indx in indx_list:
            self.beginRemoveRows(qcore.QModelIndex(), indx, indx)
            del self.__question_list[indx]
            self.endRemoveRows()

    def get_question_by_index(self, index):
        return self.__question_list[index]

    def get_all_questions(self):
        return self.__question_list

    def get_info_by_index(self, index):
        keywords = self.__question_list[index].keywords
        text = self.__question_list[index].text
        pckgs_req = self.__question_list[index].packages_req
        defs_req = self.__question_list[index].custom_defs
        doc_id = self.__question_list[index].doc_id
        return keywords, text, pckgs_req, defs_req, doc_id

    def search_all(self):
        self.beginResetModel()
        self.__question_list = self.__dbhandler.get_all()
        self.endResetModel()

    def search_by_text(self, text):
        self.beginResetModel()
        self.__question_list = self.__dbhandler.get_by_text(text)
        self.endResetModel()

    def search_by_keywords_simple(self, text):
        keywords_list = [[(True, keyword.strip()) for keyword in text.split(',')]]
        self.beginResetModel()
        self.__question_list = self.__dbhandler.get_by_keywords(keywords_list)
        self.endResetModel()

    def search_by_keywords_advanced(self, text):
        search_list = []
        clauses = [line.strip() for line in text.split('\n') if line.strip() != '']
        for clause in clauses:
            literals = [lits.strip() for lits in clause.split(',')]
            clause_list = []
            for literal in literals:
                if literal.startswith('!'):
                    clause_list.append((False, literal[1:]))
                else:
                    clause_list.append((True, literal))
            search_list.append(clause_list)
        self.beginResetModel()
        self.__question_list = self.__dbhandler.get_by_keywords(search_list)
        self.endResetModel()

    def edit_question(self, keywords, text, packages_req, custom_defs, index_model):
        row = index_model.row()
        self.__question_list[row].keywords = keywords
        self.__question_list[row].text = text
        self.__question_list[row].packages_req = packages_req
        self.__question_list[row].custom_defs = custom_defs
        self.__dbhandler.upsert(self.__question_list[row])
        self.dataChanged.emit(self.createIndex(row, 0), self.createIndex(row, self.columnCount() - 1),
                              [qcore.Qt.DisplayRole])

    def add_question(self, keywords, text, packages_req, custom_defs):
        question = ques.Question(keywords, text, packages_req, custom_defs)
        self.__dbhandler.upsert(question)
        self.beginInsertRows(qcore.QModelIndex(), 0, 0)
        self.__question_list = [question] + self.__question_list
        self.endInsertRows()

    def is_loaded(self):
        return self.__dbhandler is not None

    def load(self, fullpath):
        self.beginResetModel()
        self.__dbhandler = dtb.DBHandler(fullpath)
        self.__question_list = self.__dbhandler.get_all()
        self.endResetModel()

    def headerData(self, section, orientation, role=qcore.Qt.DisplayRole):
        if role == qcore.Qt.DisplayRole and orientation == qcore.Qt.Horizontal:
            return self.__headers_text[section]
        elif role == qcore.Qt.TextAlignmentRole:
            return qcore.Qt.Alignment(qcore.Qt.AlignCenter)
        elif role == qcore.Qt.FontRole:
            font = self.parent().tableview_search.font()
            font.setPointSize(self.__font_size)
            font.setBold(True)
            return font
        return qcore.QVariant()

    def rowCount(self, parent=qcore.QModelIndex()):
        return len(self.__question_list)

    def columnCount(self, parent=qcore.QModelIndex()):
        return len(self.__headers_text)

    def data(self, index_model, role=qcore.Qt.DisplayRole):
        if not index_model.isValid():
            return qcore.QVariant()

        if index_model.row() >= len(self.__question_list):
            return qcore.QVariant()

        if role == qcore.Qt.DisplayRole:
            question = self.__question_list[index_model.row()]
            column = index_model.column()
            if column == 0:
                return question.doc_id
            elif column == 1:
                return ', '.join(question.keywords)
            elif column == 2:
                return question.text
            elif column == 3:
                return str(question.packages_req)
            elif column == 4:
                return str(question.custom_defs)
        elif role == qcore.Qt.ToolTipRole:
            return 'Double click to edit in the database. Press del to delete from the database.'
        elif role == qcore.Qt.TextAlignmentRole:
            return qcore.Qt.Alignment(qcore.Qt.AlignCenter)
        elif role == qcore.Qt.FontRole:
            font = self.parent().tableview_search.font()
            font.setPointSize(self.__font_size)
            return font
        else:
            return qcore.QVariant()

    def flags(self, index_model):
        if index_model.isValid():
            return qcore.Qt.ItemIsEnabled | qcore.Qt.ItemIsSelectable | qcore.Qt.ItemIsDragEnabled

    def supportedDragActions(self):
        return qcore.Qt.CopyAction

    def mimeData(self, indexes_model):
        mime_data = qcore.QMimeData()
        encoded_data = qcore.QByteArray()
        stream = qcore.QDataStream(encoded_data, qcore.QIODevice.WriteOnly)
        row_set = set()
        for index_model in indexes_model:
            if index_model.isValid():
                row_set.add(index_model.row())
        for row in row_set:
            stream.writeQString(str(self.__question_list[row].dict_with_id()))
        mime_data.setData(ques.MimeTypeQuestions, encoded_data)
        return mime_data
