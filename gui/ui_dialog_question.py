# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\ui_dialog_question.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(705, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(500, 400))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Dialog.setBaseSize(QtCore.QSize(700, 700))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_2.setHorizontalSpacing(5)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineedit_keywords = QtWidgets.QLineEdit(Dialog)
        self.lineedit_keywords.setStatusTip("")
        self.lineedit_keywords.setInputMethodHints(QtCore.Qt.ImhLowercaseOnly)
        self.lineedit_keywords.setMaxLength(1000)
        self.lineedit_keywords.setObjectName("lineedit_keywords")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineedit_keywords)
        self.label_2 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.textedit_text = QtWidgets.QPlainTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.textedit_text.sizePolicy().hasHeightForWidth())
        self.textedit_text.setSizePolicy(sizePolicy)
        self.textedit_text.setMinimumSize(QtCore.QSize(0, 200))
        self.textedit_text.setObjectName("textedit_text")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textedit_text)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.listwidget_pckg_required = QtWidgets.QListWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.listwidget_pckg_required.sizePolicy().hasHeightForWidth())
        self.listwidget_pckg_required.setSizePolicy(sizePolicy)
        self.listwidget_pckg_required.setMinimumSize(QtCore.QSize(0, 100))
        self.listwidget_pckg_required.setMaximumSize(QtCore.QSize(16777215, 100))
        self.listwidget_pckg_required.setObjectName("listwidget_pckg_required")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.listwidget_pckg_required)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.listwidget_defs_required = QtWidgets.QListWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.listwidget_defs_required.sizePolicy().hasHeightForWidth())
        self.listwidget_defs_required.setSizePolicy(sizePolicy)
        self.listwidget_defs_required.setMinimumSize(QtCore.QSize(0, 100))
        self.listwidget_defs_required.setMaximumSize(QtCore.QSize(16777215, 150))
        self.listwidget_defs_required.setObjectName("listwidget_defs_required")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.listwidget_defs_required)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.pushbutton_preview = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_preview.sizePolicy().hasHeightForWidth())
        self.pushbutton_preview.setSizePolicy(sizePolicy)
        self.pushbutton_preview.setObjectName("pushbutton_preview")
        self.horizontalLayout_2.addWidget(self.pushbutton_preview)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Question"))
        self.label.setWhatsThis(_translate("Dialog", "Question\'s keywords for searching in the database."))
        self.label.setText(_translate("Dialog", "Keywords:"))
        self.lineedit_keywords.setWhatsThis(_translate("Dialog", "Question\'s keywords for searching in the database."))
        self.lineedit_keywords.setPlaceholderText(_translate("Dialog", "type the keywords in lower case letters separated by comma"))
        self.label_2.setWhatsThis(_translate("Dialog", "The question itself."))
        self.label_2.setText(_translate("Dialog", "Text:"))
        self.textedit_text.setWhatsThis(_translate("Dialog", "The question itself."))
        self.textedit_text.setPlaceholderText(_translate("Dialog", "The question itself."))
        self.label_3.setWhatsThis(_translate("Dialog", "Packages required to compile the question. Definitions required to compile the question. These will be added to the packages used by the document."))
        self.label_3.setText(_translate("Dialog", "Required\n"
"Packages:"))
        self.listwidget_pckg_required.setWhatsThis(_translate("Dialog", "Packages required to compile the question. Definitions required to compile the question. These will be added to the packages used by the document."))
        self.label_4.setWhatsThis(_translate("Dialog", "Definitions required to compile the question. These will be added to the preamble of the document."))
        self.label_4.setText(_translate("Dialog", "Required\n"
"Definitions:"))
        self.listwidget_defs_required.setWhatsThis(_translate("Dialog", "Definitions required to compile the question. These will be added to the preamble of the document."))
        self.pushbutton_preview.setText(_translate("Dialog", "Preview"))
