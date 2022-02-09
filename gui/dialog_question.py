from PyQt5.QtWidgets import *
import PyQt5.QtCore as qcore
import gui.ui_dialog_question as uiquest
import common.question as ques
import latex.latexpdfbuilder as build
import latex.profile as prof
import qasync

PLACEHOLDER_LIST_ITEM_PCKG = 'Double click here to add a new required package. Format: "Package_name: option1, option2"'
TOOLTIP_LIST_ITEM = 'Double click to edit. Del to delete.'
PLACEHOLDER_LIST_ITEM_DEFS = 'Double click here to add a new required definition/command.'


class QuestionDiag(QDialog, uiquest.Ui_Dialog):
    def __init__(self, parent, keywords=None, text='', packages_req=None, custom_defs=()):
        """
        :param parent: parent of this widget
        :type parent: QWidget
        :param keywords: keywords for the question.
        :type keywords: list of str
        :param text: the question text.
        :type text: str
        :param packages_req: required latex packages and their options.
        :type packages_req: dict [str, tuple of str]
        :param custom_defs: required custom commands and other definitions.
        :type custom_defs: tuple of str
        """
        super().__init__(parent)
        self.setupUi(self)
        item = QListWidgetItem(PLACEHOLDER_LIST_ITEM_PCKG)
        item.setForeground(qcore.Qt.gray)
        self.listwidget_pckg_required.addItem(item)
        item2 = QListWidgetItem(PLACEHOLDER_LIST_ITEM_DEFS)
        item2.setForeground(qcore.Qt.gray)
        self.listwidget_defs_required.addItem(item2)
        if keywords is not None:
            self.lineedit_keywords.setText(', '.join(keywords))
            self.textedit_text.setPlainText(text)
            for pckg, options in packages_req.items():
                if options:
                    self.listwidget_pckg_required.addItem(f'{pckg}: {", ".join(options)}')
                else:
                    self.listwidget_pckg_required.addItem(pckg)
            for defs in custom_defs:
                self.listwidget_defs_required.addItem(defs)
        self.listwidget_pckg_required.itemDoubleClicked.connect(self.double_clicked_pckg_item)
        self.listwidget_pckg_required.keyPressEvent = self.key_press_pckg_list

        self.listwidget_defs_required.itemDoubleClicked.connect(self.double_clicked_defs_item)
        self.listwidget_defs_required.keyPressEvent = self.key_press_defs_list

        self.pushbutton_preview.pressed.connect(self.__build_preview)

    @qasync.asyncSlot()
    async def __build_preview(self, checked=False):
        ret_keywords = [s.strip() for s in self.lineedit_keywords.text().split(',')]
        ret_text = self.textedit_text.toPlainText().strip()
        ret_pckg_req = {}
        for idx in range(1, self.listwidget_pckg_required.count()):
            item_txt = self.listwidget_pckg_required.item(idx).text().strip(',:')
            pckg_lst_str = item_txt.split(':', 1)
            pckg = pckg_lst_str[0].strip()
            ret_pckg_req[pckg] = tuple()
            if len(pckg_lst_str) == 2:
                ret_pckg_req[pckg] = tuple([opt.strip() for opt in pckg_lst_str[1].split(',') if opt.strip() != ''])
        ret_defs_req = tuple([self.listwidget_defs_required.item(idx).text().strip()
                              for idx in range(1, self.listwidget_defs_required.count())])

        builder = \
            build.LatexPdfBuilder('preview_selected', '', prof.Profile.preview(),
                                  [prof.LatexQuestion(ques.Question(ret_keywords, ret_text, ret_pckg_req, ret_defs_req),
                                                      prof.Profile.preview().question_environment_list[0][0])])
        try:
            await builder.temp_pdf_preview()
        except build.LatexCompileError as err:
            QMessageBox.critical(self, 'Latex Error!', err.args[0])

    def double_clicked_defs_item(self, item):
        diag_text = ''
        item_row = item.listWidget().row(item)
        if item_row > 0:
            diag_text = item.text()
        new_text, ok = QInputDialog.getMultiLineText(self.listwidget_defs_required, 'Required Definition/command',
                                                     'Type the required definition or command',
                                                     diag_text, flags=qcore.Qt.WindowFlags(qcore.Qt.Widget))
        new_text = new_text.strip()
        if ok and (new_text != '' or item_row > 0):
            item.setText(new_text)
            if item_row == 0:
                item.setForeground(qcore.Qt.black)
                item.setToolTip(TOOLTIP_LIST_ITEM)
                item_pch = QListWidgetItem(PLACEHOLDER_LIST_ITEM_PCKG)
                item_pch.setForeground(qcore.Qt.gray)
                self.listwidget_defs_required.insertItem(0, item_pch)

    def key_press_defs_list(self, event):
        if event.key() == qcore.Qt.Key_Delete:
            selected_item = self.listwidget_defs_required.selectedItems()[0]
            row = selected_item.listWidget().row(selected_item)
            if row != 0:
                self.listwidget_defs_required.removeItemWidget(selected_item)
                self.listwidget_defs_required.takeItem(row)

    def double_clicked_pckg_item(self, item):
        diag_text = ''
        item_row = item.listWidget().row(item)
        if item_row > 0:
            diag_text = item.text()
        new_text, ok = QInputDialog.getText(self.listwidget_pckg_required, 'Required Package',
                                            'Type the required package', QLineEdit.Normal,
                                            diag_text, flags=qcore.Qt.WindowFlags(qcore.Qt.Widget))
        new_text = new_text.strip()
        if ok and (new_text != '' or item_row > 0):
            item.setText(new_text)
            if item_row == 0:
                item.setForeground(qcore.Qt.black)
                item.setToolTip(TOOLTIP_LIST_ITEM)
                item_pch = QListWidgetItem(PLACEHOLDER_LIST_ITEM_PCKG)
                item_pch.setForeground(qcore.Qt.gray)
                self.listwidget_pckg_required.insertItem(0, item_pch)

    def key_press_pckg_list(self, event):
        if event.key() == qcore.Qt.Key_Delete:
            selected_item = self.listwidget_pckg_required.selectedItems()[0]
            row = selected_item.listWidget().row(selected_item)
            if row != 0:
                self.listwidget_pckg_required.removeItemWidget(selected_item)
                self.listwidget_pckg_required.takeItem(row)

    def unpack(self):
        ret_keywords = [s.strip() for s in self.lineedit_keywords.text().split(',')]
        ret_text = self.textedit_text.toPlainText().strip()
        ret_pckg_req = {}
        for idx in range(1, self.listwidget_pckg_required.count()):
            item_txt = self.listwidget_pckg_required.item(idx).text().strip(',:')
            pckg_lst_str = item_txt.split(':', 1)
            pckg = pckg_lst_str[0].strip()
            ret_pckg_req[pckg] = tuple()
            if len(pckg_lst_str) == 2:
                ret_pckg_req[pckg] = tuple([opt.strip() for opt in pckg_lst_str[1].split(',') if opt.strip() != ''])
        ret_defs_req = tuple([self.listwidget_defs_required.item(idx).text().strip()
                              for idx in range(1, self.listwidget_defs_required.count())])
        return ret_keywords, ret_text, ret_pckg_req, ret_defs_req
