from PyQt5.QtWidgets import *
import PyQt5.QtCore as qcore
import gui.ui_dialog_profile as uiprofile
import latex.profile as prof
import re

PLACEHOLDER_LIST_ITEM_PCKG = 'Double click here to add a new required package. Format: "Package_name: option1, option2"'
TOOLTIP_LIST_ITEM = 'Double click to edit. Del to delete.'
PLACEHOLDER_LIST_ITEM_ENVS = 'Double click here to add a new question environment.'


class ProfileDiag(QDialog, uiprofile.Ui_ProfileDialog):
    def __init__(self, parent, profile=None, max_envs=1000000):
        """
        :param parent: parent of this widget
        :type parent: QWidget
        :param profile: profile to be edited.
        :type profile: prof.Profile
        """
        super().__init__(parent)
        self.setupUi(self)
        self.__max_envs = max_envs
        self.lineedit_name.setFocus()
        item = QListWidgetItem(PLACEHOLDER_LIST_ITEM_PCKG)
        item.setForeground(qcore.Qt.gray)
        self.listwidget_pckg_required.addItem(item)
        item2 = QListWidgetItem(PLACEHOLDER_LIST_ITEM_ENVS)
        item2.setForeground(qcore.Qt.gray)
        self.listwidget_envs.addItem(item2)
        if profile is not None:
            self.lineedit_name.setText(profile.name)
            self.lineedit_name.setEnabled(False)
            self.lineedit_class_name.setText(profile.document_class_name)
            self.lineedit_class_options.setText(', '.join(profile.document_class_options))
            for pckg, options in profile.package_list:
                if options:
                    self.listwidget_pckg_required.addItem(f'{pckg}: {", ".join(options)}')
                else:
                    self.listwidget_pckg_required.addItem(pckg)
            self.textedit_preamble.setPlainText(profile.preamble)
            self.textedit_header.setPlainText(profile.header)
            for index, (name, tuple_args) in enumerate(profile.question_environment_list):
                if index >= self.__max_envs:
                    break
                self.listwidget_envs.addItem(
                    f'{name}: {tuple_args[0]} optional and {tuple_args[1]} mandatory parameters')
        self.listwidget_pckg_required.itemDoubleClicked.connect(self.double_clicked_pckg_item)
        self.listwidget_pckg_required.keyPressEvent = self.key_press_pckg_list

        self.listwidget_envs.itemDoubleClicked.connect(self.double_clicked_envs_item)
        self.listwidget_envs.keyPressEvent = self.key_press_envs

    def double_clicked_envs_item(self, item):
        diag_text = ''
        item_row = item.listWidget().row(item)
        if item_row == 0 and self.listwidget_envs.count() >= self.__max_envs + 1:
            QMessageBox.warning(self, 'Max number of environments reached!',
                                f'The maximum number of environments for this profile is {self.__max_envs}.')
            return
        if item_row > 0:
            diag_text = item.text()
            match_obj = re.fullmatch(r'(.+?): (\d+) optional and (\d+) mandatory parameters', diag_text)
            diag_text = f'{match_obj.group(1)}: {match_obj.group(2)}, {match_obj.group(3)}'

        match_obj = None
        ok = True
        while not match_obj and ok:
            new_text, ok = QInputDialog.getText(self.listwidget_envs, 'Question Environment',
                                                'Type the environment. The format is: env_name: '
                                                'qty_optional, qty_mandatory', QLineEdit.Normal,
                                                diag_text, flags=qcore.Qt.WindowFlags(qcore.Qt.Widget))
            match_obj = re.fullmatch(r' *(.+?) *: *(\d+) *, *(\d+) *', new_text)
        if ok:
            item.setText(f'{match_obj.group(1)}: {match_obj.group(2)} optional and {match_obj.group(3)} mandatory parameters')
            if item_row == 0:
                item.setForeground(qcore.Qt.black)
                item.setToolTip(TOOLTIP_LIST_ITEM)
                item_pch = QListWidgetItem(PLACEHOLDER_LIST_ITEM_ENVS)
                item_pch.setForeground(qcore.Qt.gray)
                self.listwidget_envs.insertItem(0, item_pch)

    def key_press_envs(self, event):
        if event.key() == qcore.Qt.Key_Delete:
            selected_item = self.listwidget_envs.selectedItems()[0]
            row = selected_item.listWidget().row(selected_item)
            if row != 0:
                self.listwidget_envs.removeItemWidget(selected_item)
                self.listwidget_envs.takeItem(row)

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
        name = self.lineedit_name.text().strip()
        new_profile = prof.Profile(name)
        class_name = self.lineedit_class_name.text().strip()
        class_options = tuple([opt.strip() for opt in self.lineedit_class_options.text().split(',')
                               if opt.strip() != ''])
        new_profile.set_document_class(class_name, class_options)
        for idx in range(1, self.listwidget_pckg_required.count()):
            item_txt = self.listwidget_pckg_required.item(idx).text().strip(',:')
            pckg_lst_str = item_txt.split(':', 1)
            pckg = pckg_lst_str[0]
            options = tuple()
            if len(pckg_lst_str) == 2:
                options = tuple([opt.strip() for opt in pckg_lst_str[1].split(',') if opt.strip() != ''])
            new_profile.add_package(pckg, options)
        new_profile.preamble = self.textedit_preamble.toPlainText().strip()
        new_profile.header = self.textedit_header.toPlainText().strip()
        for idx in range(1, self.listwidget_envs.count()):
            match_obj = re.fullmatch(r'(.+?): (\d+) optional and (\d+) mandatory parameters',
                                     self.listwidget_envs.item(idx).text())
            new_profile.add_question_environment(match_obj.group(1), int(match_obj.group(2)), int(match_obj.group(3)))
        return new_profile
