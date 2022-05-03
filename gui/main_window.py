from PyQt5.QtWidgets import *
import PyQt5.QtCore as qcore
import gui.data_models.simplemodel as simplemodel
import gui.ui_main_window as mw
import gui.data_models.dbmodel as dbmodel
import gui.dialog_question as dques
import gui.dialog_profile as dprof
import gui.generate_window as gen
import gui.dialog_settings as diag_setts
import latex.latexpdfbuilder as build
import latex.profile as prof
import os
import qasync
import common.settings as setts


class MainWindow(QMainWindow, mw.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))

        self.radioButton_bykeywords.clicked.connect(self.placeholder_search_keywords)
        self.radiobutton_bytext.clicked.connect(self.placeholder_search_text)
        self.pushbutton_advanced_search.pressed.connect(self.__advanced_search)
        self.pushbutton_generate_tex_pdf.pressed.connect(self.__generate_tex_pdf)

        self.simplemodel = simplemodel.SimpleModel(self)
        self.tableview_selected.setModel(self.simplemodel)
        self.tableview_selected.acceptDrops()
        self.tableview_selected.hideColumn(0)
        self.tableview_selected.hideColumn(3)
        self.tableview_selected.hideColumn(4)
        self.tableview_selected.doubleClicked.connect(self.edit_tableselected_slot)
        self.tableview_selected.mouseDoubleClickEvent = self.tableselected_double_click_event
        self.tableview_selected.keyPressEvent = self.key_press_selectedtable
        self.tableview_selected.setContextMenuPolicy(qcore.Qt.CustomContextMenu)
        self.tableview_selected.customContextMenuRequested.connect(self.open_context_menu_selected)

        self.dbmodel = dbmodel.DBModel(self)
        self.tableview_search.setModel(self.dbmodel)
        self.tableview_search.hideColumn(3)
        self.tableview_search.hideColumn(4)
        self.tableview_search.doubleClicked.connect(self.edit_tablesearch_slot)
        self.tableview_search.setContextMenuPolicy(qcore.Qt.CustomContextMenu)
        self.tableview_search.customContextMenuRequested.connect(self.open_context_menu_search)
        self.tableview_search.mouseDoubleClickEvent = self.tablesearch_double_click_event
        self.tableview_search.keyPressEvent = self.key_press_searchtable
        if qcore.QSysInfo.productType() == 'windows' and qcore.QSysInfo.productVersion() == '10':
            sheeth = "QHeaderView::section{" \
                     "border-top:0px solid #D8D8D8;" \
                     "border-left:0px solid #D8D8D8;" \
                     "border-right:1px solid #D8D8D8;" \
                     "border-bottom: 1px solid #D8D8D8;" \
                     "background-color:#CCCCCC;" \
                     "padding:4px;" \
                     "}" \
                     "QTableCornerButton::section{" \
                     "border-top:0px solid #D8D8D8;" \
                     "border-left:0px solid #D8D8D8;" \
                     "border-right:1px solid #D8D8D8;" \
                     "border-bottom: 1px solid #D8D8D8;" \
                     "background-color:white;" \
                     "}"
            sheetv = "QHeaderView::section{" \
                     "border-top:1px solid #D8D8D8;" \
                     "border-left:1px solid #D8D8D8;" \
                     "border-right:0px solid #D8D8D8;" \
                     "border-bottom: 0px solid #D8D8D8;" \
                     "background-color:#CCCCCC;" \
                     "padding:4px;" \
                     "}"
            verticalheader_search = self.tableview_search.verticalHeader()
            verticalheader_selected = self.tableview_selected.verticalHeader()
            horizontalheader_search = self.tableview_search.horizontalHeader()
            horizontalheader_selected = self.tableview_selected.horizontalHeader()
            horizontalheader_search.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            horizontalheader_selected.setSectionResizeMode(0, QHeaderView.ResizeToContents)

            verticalheader_search.setStyleSheet(sheetv)
            verticalheader_selected.setStyleSheet(sheetv)
            horizontalheader_search.setStyleSheet(sheeth)
            horizontalheader_selected.setStyleSheet(sheeth)

        self.lineedit_search.returnPressed.connect(self.__search_database)

        self.action_delete_all_search.setParent(self.tableview_search)
        self.action_add_selected_search.setParent(self.tableview_search)
        self.action_preview_all_search.setParent(self.tableview_search)
        self.tableview_search.addAction(self.action_preview_all_search)
        self.action_delete_all_search.triggered.connect(self.__delete_all_search)
        self.action_add_selected_search.triggered.connect(self.__add_selected_search)
        self.action_preview_all_search.triggered.connect(self.__preview_all_search)

        self.action_unselect_questions_selected.setParent(self.tableview_selected)
        self.action_preview_selected_questions_selected.setParent(self.tableview_selected)
        self.action_unselect_questions_selected.triggered.connect(self.__delete_all_selected)
        self.action_preview_selected_questions_selected.triggered.connect(self.__preview_all_selected)

        self.action_new_question.triggered.connect(self.__diag_question_add_search)
        self.action_new_profile.triggered.connect(self.__diag_new_edit_profile)
        self.action_edit_profile.triggered.connect(self.__diag_edit_profile)
        self.action_new_database.triggered.connect(self.__new_database)
        self.action_load_database.triggered.connect(self.__load_database)
        self.action_settings.triggered.connect(self.__settings)
        self.action_about.triggered.connect(self.__about)

    def __about(self):
        about_string = "Latex Exam Builder 0.9.0\n" \
                       "Using Qt version 5.15.6\n\n" \
                       "Copyright (c) - 2022\n" \
                       "Latex Exam Builder: Thiago Marcilon\n" \
                       "Using qasync: authors Sam McCormack, Gerard Marull-Paretas, Mark Harviston and Arve Knudsen " \
                       "- Copyright (c) - License: BSD License\n" \
                       "Using pytest: authors Holger Krekel and others - Copyright (c) - License: MIT License\n" \
                       "Using tinydb: author Markus Siemens - Copyright (c) - MIT License\n\n" \
                       "Website: https://github.com/thiago-marcilon/latexExamBuilder\n\n" \
                       "This program is licensed under the terms of GNU General Public License Version 3 " \
                       "like is published by the Free Software Foundation"
        QMessageBox.about(self, 'About', about_string)

    def __settings(self):
        settings = diag_setts.SettingsDiag(self)

        def receive_answer(result):
            if result == QDialog.Accepted:
                setts.profile_default_path = settings.lineedit_profile_default_directory.text()
                setts.pdf_viewer_path = settings.lineedit_path_pdf_viewer.text()
                setts.profile_file_max_size = int(settings.spinbox_prof_max_size.text())
                try:
                    setts.dump()
                except Exception as err:
                    QMessageBox.critical(self, 'Error!', err.args[0])

        settings.finished.connect(receive_answer)
        settings.open()

    def __generate_tex_pdf(self, checked=False):
        if self.simplemodel.rowCount() > 0:
            generate_window = gen.GenerateWindow(self, self.simplemodel.question_list)
            generate_window.show()
        else:
            QMessageBox.warning(self, 'No questions selected!', 'At least one question must be selected!')

    @qasync.asyncSlot()
    async def preview_selected_items(self, selected_items, model):
        builder = \
            build.LatexPdfBuilder('preview_selected', '', prof.Profile.preview(),
                                  [prof.LatexQuestion(model.get_question_by_index(item.row()),
                                                      prof.Profile.preview().question_environment_list[0][0])
                                   for item in selected_items])
        try:
            await builder.temp_pdf_preview()
        except Exception as err:
            QMessageBox.critical(self, 'Latex Error!', err.args[0])

    def __delete_all_selected(self, checked=False):
        button = QMessageBox.question(self, 'Unselect questions', 'Are you sure you want to unselect these questions?')
        if button == QMessageBox.Yes:
            selected_items = self.tableview_selected.selectionModel().selectedRows()
            self.simplemodel.remove(selected_items)

    @qasync.asyncSlot()
    async def __preview_all_selected(self, checked=False):
        table = self.tableview_selected
        selected_items = table.selectionModel().selectedRows()
        try:
            await self.preview_selected_items(selected_items, self.simplemodel)
        except Exception as err:
            QMessageBox.critical(self, 'Latex Error!', err.args[0])

    def __delete_all_search(self, checked=False):
        button = QMessageBox.question(self, 'Delete questions',
                                      'Are you sure you want to delete the selected questions '
                                      'from the database?')
        if button == QMessageBox.Yes:
            selected_items = self.tableview_search.selectionModel().selectedRows()
            try:
                self.dbmodel.remove(selected_items)
            except Exception as err:
                QMessageBox.critical(self, 'Error!', err.args[0])

    def __add_selected_search(self, checked=False):
        selected_items = self.tableview_search.selectionModel().selectedRows()
        for index in selected_items:
            keyword, text, pckgs_req, defs_req, doc_id = self.dbmodel.get_info_by_index(index.row())
            self.simplemodel.add_question(keyword, text, pckgs_req, defs_req, doc_id)

    @qasync.asyncSlot()
    async def __preview_all_search(self, checked=False):
        table = self.tableview_search
        selected_items = table.selectionModel().selectedRows()
        try:
            await self.preview_selected_items(selected_items, self.dbmodel)
        except Exception as err:
            QMessageBox.critical(self, 'Latex Error!', err.args[0])

    def open_context_menu_search(self, pos):
        table = self.tableview_search
        index = table.indexAt(pos)
        if index not in table.selectedIndexes():
            table.selectionModel().select(index, qcore.QItemSelectionModel.Rows)
        context_menu = QMenu(table)

        context_menu.addAction(self.action_delete_all_search)
        context_menu.addAction(self.action_add_selected_search)
        context_menu.addAction(self.action_preview_all_search)
        context_menu.popup(table.viewport().mapToGlobal(pos))

    def open_context_menu_selected(self, pos):
        table = self.tableview_selected
        index = table.indexAt(pos)
        if index not in table.selectedIndexes():
            table.selectionModel().select(index, qcore.QItemSelectionModel.Rows)

        context_menu = QMenu(table)

        context_menu.addAction(self.action_unselect_questions_selected)
        context_menu.addAction(self.action_preview_selected_questions_selected)
        context_menu.popup(table.viewport().mapToGlobal(pos))

    def placeholder_search_keywords(self, checked):
        if checked:
            self.lineedit_search.setPlaceholderText(
                'Type all the keywords, separated by comma, the questions must have.')

    def placeholder_search_text(self, checked):
        if checked:
            self.lineedit_search.setPlaceholderText("Type a piece of the question's text.")

    def edit_tablesearch_slot(self, index):
        keywords, text, pckg_req, defs_req, _ = self.dbmodel.get_info_by_index(index.row())
        self.__diag_question_add_search(False, keywords, text, pckg_req, defs_req, index)

    def edit_tableselected_slot(self, index):
        keywords, text, pckg_req, defs_req = self.simplemodel.get_info_by_index(index.row())
        self.__diag_question_selected(keywords, text, pckg_req, defs_req, index)

    def __diag_edit_profile(self, checked=False):
        profile_path = QFileDialog.getOpenFileName(self, "Edit Profile", os.path.abspath(setts.profile_default_path),
                                                   "Profile Files (*.prof)")[0]
        if profile_path != '':
            profile = prof.Profile(os.path.basename(profile_path).removesuffix('.prof'), os.path.dirname(profile_path))
            try:
                profile.load()
            except Exception as err:
                QMessageBox.critical(self, 'Error!', err.args[0])
            else:
                self.__diag_new_edit_profile(False, profile)

    def __diag_new_edit_profile(self, checked=False, profile=None):
        dialog_profile = dprof.ProfileDiag(self, profile)

        def receive_answer(result):
            if result == QDialog.Accepted:
                ret_profile = dialog_profile.unpack()
                try:
                    ret_profile.dump()
                except Exception as err:
                    QMessageBox.critical(self, 'Error!', err.args[0])

        dialog_profile.finished.connect(receive_answer)
        dialog_profile.open()

    def __diag_question_add_search(self, checked=False, keywords=None, text='', packages_req=None, custom_defs=(),
                                   index=None):
        if self.dbmodel.is_loaded():
            dialog_question = dques.QuestionDiag(self, keywords, text, packages_req, custom_defs)

            def receive_answer(result):
                if result == QDialog.Accepted:
                    ret_keywords, ret_text, ret_pckg_req, ret_defs_req = dialog_question.unpack()
                    try:
                        if index is None:
                            self.dbmodel.add_question(ret_keywords, ret_text, ret_pckg_req, ret_defs_req)
                        else:
                            self.dbmodel.edit_question(ret_keywords, ret_text, ret_pckg_req, ret_defs_req, index)
                    except Exception as err:
                        QMessageBox.critical(self, 'Error!', err.args[0])

            dialog_question.finished.connect(receive_answer)
            dialog_question.open()
        else:
            QMessageBox.critical(self, 'No database is loaded!',
                                 'A database must be loaded first before adding a question.')

    def __diag_question_selected(self, keywords=None, text='', packages_req=None, custom_defs=(), index=None):
        dialog_question = dques.QuestionDiag(self, keywords, text, packages_req, custom_defs)

        def receive_answer(result):
            if result == QDialog.Accepted:
                ret_keywords, ret_text, ret_pckg_req, ret_defs_req = dialog_question.unpack()
                self.simplemodel.edit_question(ret_keywords, ret_text, ret_pckg_req, ret_defs_req, index)

        dialog_question.finished.connect(receive_answer)
        dialog_question.open()

    def key_press_searchtable(self, event):
        if event.key() == qcore.Qt.Key_Delete:
            button = QMessageBox.question(self, 'Delete questions',
                                          'Are you sure you want to delete the selected questions from the database?')
            if button == QMessageBox.Yes:
                selected_items = self.tableview_search.selectionModel().selectedRows()
                try:
                    self.dbmodel.remove(selected_items)
                except Exception as err:
                    QMessageBox.critical(self, 'Error!', err.args[0])

    def key_press_selectedtable(self, event):
        if event.key() == qcore.Qt.Key_Delete:
            button = QMessageBox.question(self, 'Unselect questions', 'Are you sure you want to unselect these questions')
            if button == QMessageBox.Yes:
                selected_items = self.tableview_selected.selectionModel().selectedRows()
                self.simplemodel.remove(selected_items)

    def tablesearch_double_click_event(self, event):
        table = self.tableview_search
        table.doubleClicked.emit(table.indexAt(qcore.QPoint(event.pos().x(), event.pos().y())))
        event.accept()

    def tableselected_double_click_event(self, event):
        table = self.tableview_selected
        table.doubleClicked.emit(table.indexAt(qcore.QPoint(event.pos().x(), event.pos().y())))
        event.accept()

    def __new_database(self):
        database_path = QFileDialog.getSaveFileName(self, "New Database", os.getcwd(),
                                                    "Database Files (*.json)", '', QFileDialog.ShowDirsOnly)[0]
        if database_path == '':
            return
        while os.path.splitext(database_path)[1] != '.json':
            QMessageBox.critical(self, 'Wrong extension!', 'The database extension must be ".json".')
            database_path = QFileDialog.getSaveFileName(self, 'New Database', os.getcwd(),
                                                        'Database Files (*.json)', '', QFileDialog.ShowDirsOnly)[0]
            if database_path == '':
                return
        try:
            self.dbmodel.load(database_path)
            self.setWindowTitle(f"Latex Exam Builder: {os.path.basename(database_path).removesuffix('.json')}")
        except Exception as err:
            QMessageBox.critical(self, 'Error!', err.args[0])

    def __load_database(self):
        database_path = QFileDialog.getOpenFileName(self, "Load Database", os.getcwd(), "Database Files (*.json)")[0]
        if database_path != '':
            try:
                self.dbmodel.load(database_path)
                self.setWindowTitle(f"Latex Exam Builder: {os.path.basename(database_path).removesuffix('.json')}")
            except Exception as err:
                QMessageBox.critical(self, 'Error!', err.args[0])

    def __advanced_search(self, checked=False):
        if self.dbmodel.is_loaded():
            explanation_str = 'The format consists in at least one line. Each line is a sequence of keywords or ' \
                              'keywords preceeded by !, all separeted by commas. Example:\n' \
                              '\tkeyword1, !keyword2, keyword3\n' \
                              '\t!keyword4\n' \
                              '\t!keyword1, keyword4\n' \
                              'The example above means that the search must match all questions that:\n' \
                              '\thave "keyword1" and "keyword3", but does not have "keyword2, or\n' \
                              '\tdoes not have keyword4, or\n' \
                              '\thave keyword4, but does not have keyword1.\n'
            search_str, ok = QInputDialog.getMultiLineText(self, 'Advanced search',
                                                           explanation_str, '',
                                                           flags=qcore.Qt.WindowFlags(qcore.Qt.Widget))
            if ok:
                search_str = search_str.strip()
                if search_str != '':
                    try:
                        self.dbmodel.search_by_keywords_advanced(search_str)
                    except Exception as err:
                        QMessageBox.critical(self, 'Error!', err.args[0])
        else:
            QMessageBox.critical(self, 'No database is loaded!', 'A database must be loaded first before a search.')

    def __search_database(self):
        if self.dbmodel.is_loaded():
            try:
                if self.lineedit_search.text().strip() == '':
                    self.dbmodel.search_all()
                elif self.radiobutton_bytext.isChecked():
                    self.dbmodel.search_by_text(self.lineedit_search.text())
                else:
                    self.dbmodel.search_by_keywords_simple(self.lineedit_search.text())
            except Exception as err:
                QMessageBox.critical(self, 'Error!', err.args[0])
        else:
            QMessageBox.critical(self, 'No database is loaded!', 'A database must be loaded first before a search.')
