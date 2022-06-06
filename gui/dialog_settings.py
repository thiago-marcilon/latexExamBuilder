import os.path

from PyQt5.QtWidgets import *
import gui.ui_settings as uisetts
import gui.dialog_profile as dprof
import latex.profile as prof
import common.settings as setts


class SettingsDiag(QDialog, uisetts.Ui_Settings):
    def __init__(self, parent):
        """
        :param parent: parent of this widget
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        self.preview_profile = None
        self.lineedit_profile_default_directory.setReadOnly(True)
        self.lineedit_profile_default_directory.setText(setts.profile_default_path)
        self.lineedit_path_pdf_viewer.setReadOnly(True)
        self.lineedit_path_pdf_viewer.setText(setts.pdf_viewer_path)
        self.spinbox_prof_max_size.setValue(setts.profile_file_max_size)
        self.spinbox_header_font_size.setValue(setts.font_size_header)
        self.spinbox_data_font_size.setValue(setts.font_size_data)
        self.pushbutton_browse_prof_dir.pressed.connect(self.__fill_prof_dir)
        self.pushbutton_browse_pdf_viewer.pressed.connect(self.__fill_pdf_viewer)
        self.pushbutton_preview_profile.pressed.connect(self.__fill_preview_profile)

    def __fill_prof_dir(self):
        profile_directory = QFileDialog.getExistingDirectory(self, "Edit Profile", '')
        if profile_directory != '':
            self.lineedit_profile_default_directory.setText(os.path.abspath(profile_directory))

    def __fill_pdf_viewer(self):
        pdf_viewer = QFileDialog.getOpenFileName(self, "Edit Profile", '')[0]
        if pdf_viewer != '':
            self.lineedit_path_pdf_viewer.setText(os.path.abspath(pdf_viewer))

    def __fill_preview_profile(self):
        dialog_profile = dprof.ProfileDiag(self, prof.Profile.preview(), 1)

        def receive_answer(result):
            if result == QDialog.Accepted:
                ret_profile = dialog_profile.unpack()
                setts.load_preview_profile(ret_profile)
        dialog_profile.finished.connect(receive_answer)
        dialog_profile.open()
