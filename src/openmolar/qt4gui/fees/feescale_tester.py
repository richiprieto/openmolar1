# -*- coding: utf-8 -*-
# Copyright (c) 2009 Neil Wallace. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# See the GNU General Public License for more details.

import re, sys
from xml.dom import minidom
from PyQt4 import QtGui, QtCore
from openmolar.settings import localsettings
from openmolar.dbtools.patient_class import mouth, decidmouth
from openmolar.qt4gui.compiled_uis import Ui_codeChecker

from openmolar.dbtools.treatment_course import CURRTRT_NON_TOOTH_ATTS

DECIDMOUTH = []
for tooth in decidmouth:
    if tooth != "***":
        DECIDMOUTH.append(tooth)
ADULTMOUTH = []
for tooth in mouth:
    ADULTMOUTH.append(tooth)

class DeciduousAttributeModel(QtCore.QAbstractTableModel):
    def __init__(self, table, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.attributes = DECIDMOUTH
        self.table = table
        self.code = None
        self._rowcount = None

    def get_value(self, row):
        tooth = self.attributes[row]
        code = self.table.getToothCode(tooth, self.code.upper())
        if code:
            return self.table.feesDict[code].description
        return "-"

    def rowCount(self, index):
        if self._rowcount is None:
            self._rowcount = len(self.attributes)//2
        return self._rowcount

    def columnCount(self, index):
        return 4

    def data(self, index,role):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if index.column() == 0:
            return self.attributes[index.row()].upper()
        if index.column() == 1:
            return self.get_value(index.row())
        if index.column() == 2:
            return self.attributes[index.row() + self._rowcount].upper()
        if index.column() == 3:
            return self.get_value(index.row() + self._rowcount)


class AdultAttributeModel(DeciduousAttributeModel):
    def __init__(self, table, parent=None):
        DeciduousAttributeModel.__init__(self, table, parent)
        self.attributes = ADULTMOUTH


class test_dialog(Ui_codeChecker.Ui_Dialog, QtGui.QDialog):
    def __init__(self, tables, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.table_list = []
        tablenames = []
        for table in tables.values():
            self.table_list.append(table)
            tablenames.append(table.briefName)
        self.comboBox.addItems(tablenames)

        self.model2 = DeciduousAttributeModel(self.current_table)
        self.model3 = AdultAttributeModel(self.current_table)

        self.dec_tableView.setModel(self.model2)
        self.adult_tableView.setModel(self.model3)

        self.dec_tableView.horizontalHeader().setStretchLastSection(True)
        self.adult_tableView.horizontalHeader().setStretchLastSection(True)

        self.setWindowTitle(_("Shortcut tester"))

        self.connect(self.comboBox, QtCore.SIGNAL("currentIndexChanged (int)"),
            self.change_table)

        self.pushButton.clicked.connect(self.check_codes)

        self.quit_pushButton.clicked.connect(self.accept)

        self.line_edits = {}
        form_layout = QtGui.QFormLayout(self.frame)

        for att in CURRTRT_NON_TOOTH_ATTS:
            widg = QtGui.QLineEdit()
            self.line_edits[att] = widg
            form_layout.addRow(att, widg)

        self.lineEdit.setText("P")
        self.check_codes()

    def check_codes(self):
        tx = str(self.lineEdit.text().toAscii())
        for att in CURRTRT_NON_TOOTH_ATTS:
            usercode = "%s %s"% (att, tx.upper())
            code = self.current_table.getItemCodeFromUserCode(usercode)
            description = self.current_table.getItemDescription(code)
            self.line_edits[att].setText("%s %s"%(code, description))
        for model in (self.model2, self.model3):
            model.code = tx
            model.reset()

    @property
    def current_table(self):
        return self.table_list[self.comboBox.currentIndex()]

    def change_table(self, i):
        self.model2.table = self.current_table
        self.model3.table = self.current_table

        self.check_codes()

if __name__ == "__main__":
    localsettings.initiate()
    localsettings.loadFeeTables()
    tables = localsettings.FEETABLES.tables

    app = QtGui.QApplication([])
    dl = test_dialog(tables)
    dl.exec_()
    app.closeAllWindows()
