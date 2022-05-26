from PyQt5.QtWidgets import *
import PyQt5.QtCore as qcore
import gui.ui_generate_window as gw
import common.settings as setts
import latex.latexpdfbuilder as build
import latex.profile as prof
import os.path
import qasync
import asyncio


class GenerateWindow(QMainWindow, gw.Ui_GenerateWindow):
    def __init__(self, parent, questions):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Generate tex and pdf')
        self.setWindowModality(qcore.Qt.WindowModal)
        self.__profile = None
        self.__question_list = questions
        self.__question_hlayouts = []
        self.groupbox_placeholders = None
        for question in questions:
            horizontallayout_question = QHBoxLayout(self.groupbox_questions)
            self.__question_hlayouts.append(horizontallayout_question)
            textedit_question = QTextEdit()
            textedit_question.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
            textedit_question.setMinimumSize(200, 200)
            textedit_question.setMaximumSize(300, 40000)
            textedit_question.setText(question.text)
            textedit_question.setEnabled(False)
            horizontallayout_question.addWidget(textedit_question)
            self.verticallayout_questions.addLayout(horizontallayout_question)

        path = setts.profile_default_path
        profiles_list = [file.removesuffix('.prof') for file in os.listdir(path)
                         if os.path.isfile(os.path.join(path, file)) and file.endswith('.prof')]
        if len(profiles_list) > 0:
            self.combobox_profile.addItems(profiles_list)
            self.combobox_profile.setCurrentIndex(-1)
            self.combobox_profile.currentTextChanged.connect(self.__change_profile)
            self.combobox_profile.setCurrentIndex(0)

        self.pushbutton_tex.pressed.connect(self.__generate_tex)
        self.pushbutton_pdf.pressed.connect(self.__generate_pdf)
        self.pushbutton_tex_pdf.pressed.connect(self.__generate_tex_pdf)

    @staticmethod
    def __dialog_async_exec(dialog, mode):
        dialog.setModal(True)
        dialog.setAcceptMode(mode)
        future = asyncio.get_running_loop().create_future()
        dialog.finished.connect(lambda r: future.set_result(r))
        dialog.open()
        dialog.setVisible(True)
        return future

    @qasync.asyncSlot()
    async def __generate_tex(self, checked=False):
        if self.__profile is None:
            QMessageBox.warning(self, 'No Profile Selected!', 'A profile must be selected.')
            return False
        if any([hlayout.itemAt(1).widget().currentText().strip() == ''
                for hlayout in self.__question_hlayouts]):
            QMessageBox.warning(self, 'No Environment Selected!', 'A environment must be selected for all questions.')
            return False
        if any([hlayout.itemAt(3).widget().layout().itemAt(ind, QFormLayout.FieldRole).widget().text().strip() == ''
                for hlayout in self.__question_hlayouts
                for ind in range(hlayout.itemAt(3).widget().layout().rowCount())]):
            QMessageBox.warning(self, 'Mandatory arguments empty!', 'All mandatory arguments fields must be filled.')
            return False

        fillers = {}
        if self.groupbox_placeholders is not None:
            fillers = dict([(vbox.itemAt(0).widget().text(), vbox.itemAt(1).widget().text())
                            for vbox in self.groupbox_placeholders.layout().children()])
        latex_questions = []
        for ind, question in enumerate(self.__question_list):
            hlayout = self.__question_hlayouts[ind]
            env_name = hlayout.itemAt(1).widget().currentText()
            opt_options = []
            for opt_ind in range(hlayout.itemAt(2).widget().layout().rowCount()):
                text = hlayout.itemAt(2).widget().layout().itemAt(opt_ind,
                                                                  QFormLayout.FieldRole).widget().text().strip()
                if text != '':
                    opt_options.append(text)
            opt_options = tuple(opt_options)
            mand_options = tuple(
                [hlayout.itemAt(3).widget().layout().itemAt(mand_ind, QFormLayout.FieldRole).widget().text().strip()
                 for mand_ind in range(hlayout.itemAt(3).widget().layout().rowCount())])
            latex_questions.append(prof.LatexQuestion(question, env_name, opt_options, mand_options))

        dialog = QFileDialog(self, "Save tex", os.getcwd(), "Latex files (*.tex)")
        result = await GenerateWindow.__dialog_async_exec(dialog, QFileDialog.AcceptSave)
        tex_path = ''
        if result == QFileDialog.Accepted and dialog.selectedFiles():
            tex_path = dialog.selectedFiles()[0]
        if tex_path != '':
            self.current_builder = build.LatexPdfBuilder(os.path.basename(tex_path).removesuffix('.tex'),
                                                         os.path.dirname(tex_path),
                                                         self.__profile, latex_questions, fillers)
            try:
                self.current_builder.generate_tex()
                QMessageBox.information(self, 'Success!', 'The tex file was generated with success!')
                return True
            except Exception as err:
                QMessageBox.critical(self, 'Error!', str(err.args))
                return False

    @qasync.asyncSlot()
    async def __generate_pdf(self, checked=False):
        dialog = QFileDialog(self, "Compile tex", os.getcwd(), "Latex files (*.tex)")
        result = await GenerateWindow.__dialog_async_exec(dialog, QFileDialog.AcceptOpen)
        tex_path = ''
        if result == QFileDialog.Accepted and dialog.selectedFiles():
            tex_path = dialog.selectedFiles()[0]
        if tex_path != '':
            self.current_builder = build.LatexPdfBuilder(os.path.basename(tex_path).removesuffix('.tex'),
                                                         os.path.dirname(tex_path))
            try:
                self.current_builder.generate_pdf()
                QMessageBox.information(self, 'Success!', 'The pdf file was generated with success!')
                await self.current_builder.pdf_preview()
                return True
            except Exception as err:
                QMessageBox.critical(self, 'Error!', str(err.args))
                return False

    @qasync.asyncSlot()
    async def __generate_tex_pdf(self, checked=False):
        result = await self.__generate_tex()
        if result:
            try:
                self.current_builder.generate_pdf()
                QMessageBox.information(self, 'Success!', 'The pdf file was generated with success!')
                await self.current_builder.pdf_preview()
                return True
            except Exception as err:
                QMessageBox.critical(self, 'Error!', str(err.args))
                return False

    @property
    def hlayouts(self):
        return self.__question_hlayouts

    def __change_profile(self, text):
        self.__profile = prof.Profile(text, setts.profile_default_path)
        try:
            self.__profile.load()
        except Exception as err:
            QMessageBox.critical(self, 'Error!', str(err.args))
            self.combobox_profile.setCurrentIndex(-1)
        else:
            if self.groupbox_placeholders is not None:
                self.verticalLayout_2.removeWidget(self.groupbox_placeholders)
                self.groupbox_placeholders.deleteLater()
                self.groupbox_placeholders = None
            if self.__profile.placeholders:
                self.groupbox_placeholders = QGroupBox(self.scrollAreaWidgetContents)
                self.groupbox_placeholders.setObjectName("groupbox_placeholders")
                self.groupbox_placeholders.setTitle(qcore.QCoreApplication.translate("GenerateWindow", "Profile Placeholders"))
                self.verticalLayout_2.insertWidget(1, self.groupbox_placeholders)
                horizontallayout_placeholders = QHBoxLayout(self.groupbox_placeholders)
                for placeholder in self.__profile.placeholders:
                    layout = QVBoxLayout()
                    layout.addWidget(QLabel(placeholder))
                    layout.addWidget(QLineEdit())
                    horizontallayout_placeholders.addLayout(layout)

            for q_index, hlayout in enumerate(self.__question_hlayouts):
                for index in range(hlayout.count() - 1, 0, -1):
                    hlayout.removeWidget(hlayout.itemAt(index).widget())
                combobox_env_question = QComboBox(hlayout.parentWidget())
                combobox_env_question.addItems([env for env, _ in self.__profile.question_environment_list])
                hlayout.addWidget(combobox_env_question)

                def change_environment(playout):
                    def slot_change_environment(current_index):
                        for ind in range(playout.count() - 1, 1, -1):
                            playout.removeWidget(playout.itemAt(ind).widget())

                        group_box_opt = QGroupBox('Optional arguments', self)
                        group_box_opt.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
                        group_box_opt.setMinimumSize(200, 200)
                        group_box_opt.setMaximumSize(40000, 40000)
                        formlayout_opt = QFormLayout(group_box_opt)
                        if self.__profile.question_environment_list[current_index][1][0] > 0:
                            for ind in range(self.__profile.question_environment_list[current_index][1][0]):
                                formlayout_opt.addRow(f'Argument {ind + 1}: ', QLineEdit())
                        group_box_opt.setLayout(formlayout_opt)
                        playout.addWidget(group_box_opt)

                        group_box_mand = QGroupBox('Mandatory arguments', self)
                        group_box_mand.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
                        group_box_mand.setMinimumSize(200, 200)
                        group_box_mand.setMaximumSize(40000, 40000)
                        formlayout_mand = QFormLayout(group_box_mand)
                        if self.__profile.question_environment_list[current_index][1][1] > 0:
                            for ind in range(self.__profile.question_environment_list[current_index][1][1]):
                                formlayout_mand.addRow(f'Argument {ind + 1}: ', QLineEdit())
                        group_box_mand.setLayout(formlayout_mand)
                        playout.addWidget(group_box_mand)

                    return slot_change_environment

                combobox_env_question.setCurrentIndex(-1)
                combobox_env_question.currentIndexChanged.connect(change_environment(hlayout))
                combobox_env_question.setCurrentIndex(0)
