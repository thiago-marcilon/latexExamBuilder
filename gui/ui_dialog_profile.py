# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_dialog_profile.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProfileDialog(object):
    def setupUi(self, ProfileDialog):
        ProfileDialog.setObjectName("ProfileDialog")
        ProfileDialog.resize(731, 650)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProfileDialog.sizePolicy().hasHeightForWidth())
        ProfileDialog.setSizePolicy(sizePolicy)
        ProfileDialog.setMinimumSize(QtCore.QSize(0, 650))
        ProfileDialog.setMaximumSize(QtCore.QSize(16777215, 650))
        self.verticalLayout = QtWidgets.QVBoxLayout(ProfileDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(ProfileDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineedit_class_name = QtWidgets.QLineEdit(ProfileDialog)
        self.lineedit_class_name.setObjectName("lineedit_class_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineedit_class_name)
        self.label_2 = QtWidgets.QLabel(ProfileDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineedit_class_options = QtWidgets.QLineEdit(ProfileDialog)
        self.lineedit_class_options.setObjectName("lineedit_class_options")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineedit_class_options)
        self.label_3 = QtWidgets.QLabel(ProfileDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.textedit_preamble = QtWidgets.QPlainTextEdit(ProfileDialog)
        self.textedit_preamble.setObjectName("textedit_preamble")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.textedit_preamble)
        self.label_4 = QtWidgets.QLabel(ProfileDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.textedit_header = QtWidgets.QPlainTextEdit(ProfileDialog)
        self.textedit_header.setObjectName("textedit_header")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.textedit_header)
        self.label_5 = QtWidgets.QLabel(ProfileDialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineedit_name = QtWidgets.QLineEdit(ProfileDialog)
        self.lineedit_name.setPlaceholderText("")
        self.lineedit_name.setObjectName("lineedit_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineedit_name)
        self.label_6 = QtWidgets.QLabel(ProfileDialog)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.listwidget_envs = QtWidgets.QListWidget(ProfileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_envs.sizePolicy().hasHeightForWidth())
        self.listwidget_envs.setSizePolicy(sizePolicy)
        self.listwidget_envs.setMaximumSize(QtCore.QSize(300, 16777215))
        self.listwidget_envs.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listwidget_envs.setAlternatingRowColors(True)
        self.listwidget_envs.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.listwidget_envs.setObjectName("listwidget_envs")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.listwidget_envs)
        self.label_7 = QtWidgets.QLabel(ProfileDialog)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.listwidget_pckg_required = QtWidgets.QListWidget(ProfileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listwidget_pckg_required.sizePolicy().hasHeightForWidth())
        self.listwidget_pckg_required.setSizePolicy(sizePolicy)
        self.listwidget_pckg_required.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listwidget_pckg_required.setAlternatingRowColors(True)
        self.listwidget_pckg_required.setObjectName("listwidget_pckg_required")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.listwidget_pckg_required)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ProfileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ProfileDialog)
        self.buttonBox.accepted.connect(ProfileDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(ProfileDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ProfileDialog)

    def retranslateUi(self, ProfileDialog):
        _translate = QtCore.QCoreApplication.translate
        ProfileDialog.setWindowTitle(_translate("ProfileDialog", "New Profile"))
        self.label.setWhatsThis(_translate("ProfileDialog", "Name of the document class."))
        self.label.setText(_translate("ProfileDialog", "Document Class name:"))
        self.lineedit_class_name.setWhatsThis(_translate("ProfileDialog", "Name of the document class."))
        self.label_2.setWhatsThis(_translate("ProfileDialog", "Options for the document class separated by comma."))
        self.label_2.setText(_translate("ProfileDialog", "Document Class options:"))
        self.lineedit_class_options.setWhatsThis(_translate("ProfileDialog", "Options for the document class separated by comma."))
        self.lineedit_class_options.setPlaceholderText(_translate("ProfileDialog", "Options for the document class separated by comma."))
        self.label_3.setWhatsThis(_translate("ProfileDialog", "Everything that comes after the last usepackage and before begin{document}. You can add placeholders between two % symbols which can be replaced by strings of your choice at compilation time."))
        self.label_3.setText(_translate("ProfileDialog", "Preamble:"))
        self.textedit_preamble.setWhatsThis(_translate("ProfileDialog", "Everything that comes after the last usepackage and before begin{document}. You can add placeholders between two % symbols which can be replaced by strings of your choice at compilation time."))
        self.textedit_preamble.setPlaceholderText(_translate("ProfileDialog", "Everything that comes after the last \\usepackage and before \\begin{document}. It supports placeholders."))
        self.label_4.setWhatsThis(_translate("ProfileDialog", "Everything that comes after begin{document} and before the questions themselves. You can add placeholders between two % symbols which can be replaced by strings of your choice at compilation time."))
        self.label_4.setText(_translate("ProfileDialog", "Header:"))
        self.textedit_header.setWhatsThis(_translate("ProfileDialog", "Everything that comes after begin{document} and before the questions themselves. You can add placeholders between two % symbols which can be replaced by strings of your choice at compilation time."))
        self.textedit_header.setPlaceholderText(_translate("ProfileDialog", "Everything that comes after \\begin{document} and before the questions themselves. It supports placeholders."))
        self.label_5.setText(_translate("ProfileDialog", "Name:"))
        self.label_6.setWhatsThis(_translate("ProfileDialog", "Environments that will wrap the questions. You must define these in the preamble."))
        self.label_6.setText(_translate("ProfileDialog", "Question environments:"))
        self.listwidget_envs.setWhatsThis(_translate("ProfileDialog", "Environments that will wrap the questions. You must define these in the preamble."))
        self.label_7.setWhatsThis(_translate("ProfileDialog", "Latex packages required by the profile."))
        self.label_7.setText(_translate("ProfileDialog", "Required packages:"))
        self.listwidget_pckg_required.setWhatsThis(_translate("ProfileDialog", "Latex packages required by the profile."))
