# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        MainWindow.setAutoFillBackground(True)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableview_search = QtWidgets.QTableView(self.verticalLayoutWidget)
        self.tableview_search.setMinimumSize(QtCore.QSize(0, 0))
        self.tableview_search.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableview_search.setProperty("showDropIndicator", False)
        self.tableview_search.setDragEnabled(True)
        self.tableview_search.setDragDropOverwriteMode(False)
        self.tableview_search.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.tableview_search.setAlternatingRowColors(True)
        self.tableview_search.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableview_search.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableview_search.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableview_search.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableview_search.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableview_search.setGridStyle(QtCore.Qt.SolidLine)
        self.tableview_search.setObjectName("tableview_search")
        self.tableview_search.horizontalHeader().setCascadingSectionResizes(True)
        self.tableview_search.horizontalHeader().setStretchLastSection(True)
        self.tableview_search.verticalHeader().setVisible(True)
        self.tableview_search.verticalHeader().setCascadingSectionResizes(True)
        self.tableview_search.verticalHeader().setDefaultSectionSize(150)
        self.tableview_search.verticalHeader().setMinimumSectionSize(50)
        self.verticalLayout_3.addWidget(self.tableview_search)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 80))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 70))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.radiobutton_bytext = QtWidgets.QRadioButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radiobutton_bytext.sizePolicy().hasHeightForWidth())
        self.radiobutton_bytext.setSizePolicy(sizePolicy)
        self.radiobutton_bytext.setObjectName("radiobutton_bytext")
        self.buttongroup_search = QtWidgets.QButtonGroup(MainWindow)
        self.buttongroup_search.setObjectName("buttongroup_search")
        self.buttongroup_search.addButton(self.radiobutton_bytext)
        self.verticalLayout_6.addWidget(self.radiobutton_bytext)
        self.radioButton_bykeywords = QtWidgets.QRadioButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_bykeywords.sizePolicy().hasHeightForWidth())
        self.radioButton_bykeywords.setSizePolicy(sizePolicy)
        self.radioButton_bykeywords.setChecked(True)
        self.radioButton_bykeywords.setObjectName("radioButton_bykeywords")
        self.buttongroup_search.addButton(self.radioButton_bykeywords)
        self.verticalLayout_6.addWidget(self.radioButton_bykeywords)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.lineedit_search = QtWidgets.QLineEdit(self.groupBox)
        self.lineedit_search.setMinimumSize(QtCore.QSize(0, 26))
        self.lineedit_search.setMaximumSize(QtCore.QSize(16777215, 26))
        self.lineedit_search.setObjectName("lineedit_search")
        self.horizontalLayout.addWidget(self.lineedit_search)
        self.pushbutton_advanced_search = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_advanced_search.sizePolicy().hasHeightForWidth())
        self.pushbutton_advanced_search.setSizePolicy(sizePolicy)
        self.pushbutton_advanced_search.setMinimumSize(QtCore.QSize(25, 20))
        self.pushbutton_advanced_search.setMaximumSize(QtCore.QSize(25, 20))
        self.pushbutton_advanced_search.setIconSize(QtCore.QSize(16, 16))
        self.pushbutton_advanced_search.setFlat(False)
        self.pushbutton_advanced_search.setObjectName("pushbutton_advanced_search")
        self.horizontalLayout.addWidget(self.pushbutton_advanced_search)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableview_selected = QtWidgets.QTableView(self.groupBox_2)
        self.tableview_selected.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableview_selected.setDragEnabled(True)
        self.tableview_selected.setDragDropOverwriteMode(False)
        self.tableview_selected.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.tableview_selected.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.tableview_selected.setAlternatingRowColors(True)
        self.tableview_selected.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableview_selected.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableview_selected.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableview_selected.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableview_selected.setObjectName("tableview_selected")
        self.tableview_selected.horizontalHeader().setCascadingSectionResizes(True)
        self.tableview_selected.horizontalHeader().setStretchLastSection(True)
        self.tableview_selected.verticalHeader().setVisible(True)
        self.tableview_selected.verticalHeader().setCascadingSectionResizes(True)
        self.tableview_selected.verticalHeader().setDefaultSectionSize(150)
        self.tableview_selected.verticalHeader().setMinimumSectionSize(50)
        self.verticalLayout_2.addWidget(self.tableview_selected)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pushbutton_generate_tex_pdf = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_generate_tex_pdf.sizePolicy().hasHeightForWidth())
        self.pushbutton_generate_tex_pdf.setSizePolicy(sizePolicy)
        self.pushbutton_generate_tex_pdf.setObjectName("pushbutton_generate_tex_pdf")
        self.horizontalLayout_7.addWidget(self.pushbutton_generate_tex_pdf)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 22))
        self.menubar.setAutoFillBackground(True)
        self.menubar.setStyleSheet("")
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menu_actions = QtWidgets.QMenu(self.menubar)
        self.menu_actions.setObjectName("menu_actions")
        MainWindow.setMenuBar(self.menubar)
        self.action_load_database = QtWidgets.QAction(MainWindow)
        self.action_load_database.setObjectName("action_load_database")
        self.action_settings = QtWidgets.QAction(MainWindow)
        self.action_settings.setObjectName("action_settings")
        self.action_close_program = QtWidgets.QAction(MainWindow)
        self.action_close_program.setMenuRole(QtWidgets.QAction.QuitRole)
        self.action_close_program.setObjectName("action_close_program")
        self.action_new_question = QtWidgets.QAction(MainWindow)
        self.action_new_question.setObjectName("action_new_question")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_new_database = QtWidgets.QAction(MainWindow)
        self.action_new_database.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.action_new_database.setObjectName("action_new_database")
        self.action_new_profile = QtWidgets.QAction(MainWindow)
        self.action_new_profile.setObjectName("action_new_profile")
        self.action_delete_all_search = QtWidgets.QAction(MainWindow)
        self.action_delete_all_search.setObjectName("action_delete_all_search")
        self.action_preview_all_search = QtWidgets.QAction(MainWindow)
        self.action_preview_all_search.setObjectName("action_preview_all_search")
        self.action_add_selected_search = QtWidgets.QAction(MainWindow)
        self.action_add_selected_search.setObjectName("action_add_selected_search")
        self.action_load_profile = QtWidgets.QAction(MainWindow)
        self.action_load_profile.setObjectName("action_load_profile")
        self.action_edit_profile = QtWidgets.QAction(MainWindow)
        self.action_edit_profile.setObjectName("action_edit_profile")
        self.action_unselect_questions_selected = QtWidgets.QAction(MainWindow)
        self.action_unselect_questions_selected.setObjectName("action_unselect_questions_selected")
        self.action_preview_selected_questions_selected = QtWidgets.QAction(MainWindow)
        self.action_preview_selected_questions_selected.setObjectName("action_preview_selected_questions_selected")
        self.menuFile.addAction(self.action_new_database)
        self.menuFile.addAction(self.action_load_database)
        self.menuFile.addAction(self.action_settings)
        self.menuFile.addAction(self.action_close_program)
        self.menuHelp.addAction(self.action_about)
        self.menu_actions.addAction(self.action_new_profile)
        self.menu_actions.addAction(self.action_edit_profile)
        self.menu_actions.addAction(self.action_new_question)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_actions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.action_close_program.triggered.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Latex Exam Builder"))
        self.groupBox.setTitle(_translate("MainWindow", "Search"))
        self.radiobutton_bytext.setText(_translate("MainWindow", "by text"))
        self.radioButton_bykeywords.setText(_translate("MainWindow", "by keywords"))
        self.lineedit_search.setPlaceholderText(_translate("MainWindow", "Type all the keywords, separated by comma, the questions must have."))
        self.pushbutton_advanced_search.setText(_translate("MainWindow", "..."))
        self.groupBox_2.setTitle(_translate("MainWindow", "Selected Questions"))
        self.pushbutton_generate_tex_pdf.setText(_translate("MainWindow", "Generate tex and pdf"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menu_actions.setTitle(_translate("MainWindow", "Actions"))
        self.action_load_database.setText(_translate("MainWindow", "Load Database..."))
        self.action_load_database.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.action_settings.setText(_translate("MainWindow", "Settings..."))
        self.action_settings.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_close_program.setText(_translate("MainWindow", "Exit"))
        self.action_new_question.setText(_translate("MainWindow", "New Question..."))
        self.action_new_question.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_about.setText(_translate("MainWindow", "About"))
        self.action_new_database.setText(_translate("MainWindow", "New Database..."))
        self.action_new_database.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.action_new_profile.setText(_translate("MainWindow", "New Profile..."))
        self.action_delete_all_search.setText(_translate("MainWindow", "Delete All in Selection"))
        self.action_preview_all_search.setText(_translate("MainWindow", "Preview Selected Questions"))
        self.action_preview_all_search.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.action_add_selected_search.setText(_translate("MainWindow", "Add to Selected Questions"))
        self.action_load_profile.setText(_translate("MainWindow", "Load Profile Directory..."))
        self.action_edit_profile.setText(_translate("MainWindow", "Edit Profile..."))
        self.action_unselect_questions_selected.setText(_translate("MainWindow", "Deselect Questions"))
        self.action_preview_selected_questions_selected.setText(_translate("MainWindow", "Preview Selected Questions"))
