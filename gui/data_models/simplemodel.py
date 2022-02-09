import PyQt5.QtCore as qcore
import ast
import common.question as ques


class SimpleModel(qcore.QAbstractTableModel):

    def __init__(self, parent):
        super().__init__(parent)
        self.__headers_text = ['Id', 'Keywords', 'Question Text',
                               'packages required', 'custom definitions']
        self.question_list = []
        self.__font_size = 8

    def get_question_by_index(self, index):
        return self.question_list[index]

    def remove(self, indxmodel_list):
        indx_list = [item.row() for item in indxmodel_list]
        indx_list = sorted(indx_list, reverse=True)
        for indx in indx_list:
            self.beginRemoveRows(qcore.QModelIndex(), indx, indx)
            del self.question_list[indx]
            self.endRemoveRows()

    def add_question(self, keywords, text, packages_req, custom_defs, doc_id):
        row = self.rowCount()
        self.beginInsertRows(qcore.QModelIndex(), row, row)
        self.question_list[row:row] = [ques.Question(keywords, text, packages_req, custom_defs)]
        self.question_list[row].doc_id = doc_id
        self.endInsertRows()

    def edit_question(self, keywords, text, packages_req, custom_defs, index):
        row = index.row()
        if self.question_list[row].doc_id > 0:
            self.question_list[row].doc_id = -self.question_list[row].doc_id
        self.question_list[row].keywords = keywords
        self.question_list[row].text = text
        self.question_list[row].packages_req = packages_req
        self.question_list[row].custom_defs = custom_defs
        self.dataChanged.emit(self.createIndex(row, 0), self.createIndex(row, self.columnCount() - 1),
                              [qcore.Qt.DisplayRole])

    def insertRows(self, row, count, parent=qcore.QModelIndex()):
        try:
            self.beginInsertRows(parent, row, row + count - 1)
            self.question_list[row:row] = [ques.Question()] * count
            self.endInsertRows()
            return True
        finally:
            return False

    def removeRows(self, row, count, parent=qcore.QModelIndex()):
        try:
            self.beginRemoveRows(parent, row, row + count - 1)
            del self.question_list[row:row + count]
            self.endRemoveRows()
            return True
        finally:
            return False

    def get_info_by_index(self, index):
        keywords = self.question_list[index].keywords
        text = self.question_list[index].text
        pckgs_req = self.question_list[index].packages_req
        defs_req = self.question_list[index].custom_defs
        return keywords, text, pckgs_req, defs_req

    def headerData(self, section, orientation, role=qcore.Qt.DisplayRole):
        if role == qcore.Qt.DisplayRole:
            if orientation == qcore.Qt.Horizontal:
                return self.__headers_text[section]
            else:
                return section + 1
        elif role == qcore.Qt.TextAlignmentRole:
            return qcore.Qt.Alignment(qcore.Qt.AlignCenter)
        elif role == qcore.Qt.FontRole:
            font = self.parent().tableview_search.font()
            font.setPointSize(self.__font_size)
            font.setBold(True)
            return font
        return qcore.QVariant()

    def rowCount(self, parent=qcore.QModelIndex()):
        return len(self.question_list)

    def columnCount(self, parent=qcore.QModelIndex()):
        return len(self.__headers_text)

    def data(self, index, role=qcore.Qt.DisplayRole):
        if not index.isValid():
            return qcore.QVariant()

        if index.row() >= len(self.question_list):
            return qcore.QVariant()

        if role == qcore.Qt.DisplayRole:
            question = self.question_list[index.row()]
            column = index.column()
            if column == 0:
                if question.doc_id >= 0:
                    return str(question.doc_id)
                return f'{str(-question.doc_id)}\u02DF'
            elif column == 1:
                return ', '.join(question.keywords)
            elif column == 2:
                return question.text
            elif column == 3:
                return str(question.packages_req)
            elif column == 4:
                return str(question.custom_defs)
        elif role == qcore.Qt.ToolTipRole:
            return 'Double click to edit details "on the fly". Press del to unselect.'
        elif role == qcore.Qt.TextAlignmentRole:
            return qcore.Qt.Alignment(qcore.Qt.AlignCenter)
        elif role == qcore.Qt.FontRole:
            font = self.parent().tableview_selected.font()
            font.setPointSize(self.__font_size)
            return font
        else:
            return qcore.QVariant()

    def flags(self, index):
        if index.isValid():
            return qcore.Qt.ItemIsEnabled | qcore.Qt.ItemIsSelectable | qcore.Qt.ItemNeverHasChildren |\
                   qcore.Qt.ItemIsDragEnabled | qcore.Qt.ItemIsDropEnabled
        else:
            return qcore.Qt.ItemNeverHasChildren | qcore.Qt.ItemIsDropEnabled

    def supportedDragActions(self):
        return qcore.Qt.MoveAction

    def supportedDropActions(self):
        return qcore.Qt.MoveAction | qcore.Qt.CopyAction

    def mimeTypes(self):
        return [ques.MimeTypeQuestions, ques.MimeTypeQuestionsIndexes]

    def canDropMimeData(self, data, action, row, column, parent):
        return (data.hasFormat(ques.MimeTypeQuestionsIndexes) and action == qcore.Qt.MoveAction) or \
               (data.hasFormat(ques.MimeTypeQuestions) and action == qcore.Qt.CopyAction)

    def mimeData(self, indexes):
        mime_data = qcore.QMimeData()
        encoded_data = qcore.QByteArray()
        stream = qcore.QDataStream(encoded_data, qcore.QIODevice.WriteOnly)
        row_indexes = set([index.row() for index in indexes if index.isValid()])
        for row in row_indexes:
            stream.writeQString(str(self.question_list[row].dict_with_id()))
            stream.writeInt(row)
        mime_data.setData(ques.MimeTypeQuestionsIndexes, encoded_data)
        return mime_data

    def dropMimeData(self, data, action, row, column, parent):
        if not self.canDropMimeData(data, action, row, column, parent):
            return False
        if action == qcore.Qt.CopyAction:
            encoded_data = data.data(ques.MimeTypeQuestions)
        else:
            encoded_data = data.data(ques.MimeTypeQuestionsIndexes)
        if row < 0:
            if parent.isValid():
                row = parent.row()
            else:
                row = len(self.question_list)
        stream = qcore.QDataStream(encoded_data, qcore.QIODevice.ReadOnly)
        questions_list = []
        rows = 0
        rows_at_least_row = 0
        while not stream.atEnd():
            question = ques.Question()
            qstring = stream.readQString()
            qdic = ast.literal_eval(qstring)
            question.load_from_dict(qdic)
            if action == qcore.Qt.CopyAction:
                questions_list.append(question)
            else:
                ind = stream.readInt()
                questions_list.append((ind, question))
                if ind <= row:
                    rows_at_least_row += 1
            rows += 1
        if action == qcore.Qt.CopyAction:
            self.insertRows(row, rows)
            self.question_list[row:row + rows] = questions_list
            self.dataChanged.emit(self.createIndex(row, 0),
                                  self.createIndex(row + rows - 1, self.columnCount() - 1),
                                  [qcore.Qt.DisplayRole])
        else:
            row -= rows_at_least_row
            questions_list = sorted(questions_list, reverse=True)
            self.beginResetModel()
            for ind, _ in questions_list:
                del self.question_list[ind]
            list_add = [question for _, question in questions_list]
            list_add.reverse()
            self.question_list[row:row + rows - 1] = list_add
            self.endResetModel()
        return True

    def index(self, row, column, parent=qcore.QModelIndex()):
        return self.createIndex(row, column, parent)
