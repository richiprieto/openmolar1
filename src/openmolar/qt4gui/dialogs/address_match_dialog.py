#! /usr/bin/python

# ########################################################################### #
# #                                                                         # #
# # Copyright (c) 2009-2016 Neil Wallace <neil@openmolar.com>               # #
# #                                                                         # #
# # This file is part of OpenMolar.                                         # #
# #                                                                         # #
# # OpenMolar is free software: you can redistribute it and/or modify       # #
# # it under the terms of the GNU General Public License as published by    # #
# # the Free Software Foundation, either version 3 of the License, or       # #
# # (at your option) any later version.                                     # #
# #                                                                         # #
# # OpenMolar is distributed in the hope that it will be useful,            # #
# # but WITHOUT ANY WARRANTY; without even the implied warranty of          # #
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           # #
# # GNU General Public License for more details.                            # #
# #                                                                         # #
# # You should have received a copy of the GNU General Public License       # #
# # along with OpenMolar.  If not, see <http://www.gnu.org/licenses/>.      # #
# #                                                                         # #
# ########################################################################### #

import re

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from openmolar.settings import localsettings
from openmolar.qt4gui.dialogs.base_dialogs import BaseDialog
from openmolar.dbtools import families


HEADERS = ['score', 'serialno', _('Title'), _('Forename'), _('Surname'),
           _('dob'), _('Address1'), _('Address2'), _('Address3'), _('Town'),
           _('POSTCODE')]


class AddressMatchDialog(BaseDialog):

    def __init__(self, om_gui):
        BaseDialog.__init__(self, om_gui, remove_stretch=True)

        self.om_gui = om_gui

        title = _("Address Matches")
        self.setWindowTitle(title)

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSortingEnabled(True)

        if self.om_gui.pt.serialno == 0:
            self.address = localsettings.LAST_ADDRESS[1:]
        else:
            self.address = (self.om_gui.pt.addr1,
                            self.om_gui.pt.addr2,
                            self.om_gui.pt.addr3,
                            self.om_gui.pt.town,
                            self.om_gui.pt.county,
                            self.om_gui.pt.pcde,)

        addr = "%s, %s, %s, %s, %s, %s" % (
            self.address[0],
            self.address[1],
            self.address[2],
            self.address[3],
            self.address[4],
            self.address[5],
        )

        while re.search(", *,", addr):
            addr = re.sub(", *,", ", ", addr)

        message = "<b>%s<b><hr />%s" % (
            _("Top 12 address matches for"), addr)

        label = QtWidgets.QLabel()
        label.setText(message)

        self.insertWidget(label)
        self.insertWidget(self.table_widget)

        self.load_values()

        self.table_widget.itemSelectionChanged.connect(self.enableApply)

    def sizeHint(self):
        return QtCore.QSize(1000, 600)

    def load_values(self):
        rows = families.get_address_matches(self.address)

        self.table_widget.clear()
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(HEADERS))
        self.table_widget.setHorizontalHeaderLabels(HEADERS)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        for row, result in enumerate(rows):
            for col, field in enumerate(result):
                if field is None:
                    continue
                if col == 5:
                    item = QtWidgets.QTableWidgetItem(
                        localsettings.formatDate(field))
                elif col == 0:  # match
                    item = QtWidgets.QTableWidgetItem("%04d" % field)
                elif col == 1:  # serialno
                    item = QtWidgets.QTableWidgetItem("%d" % field)
                else:
                    item = QtWidgets.QTableWidgetItem(field)
                self.table_widget.setItem(row, col, item)

        self.table_widget.resizeColumnsToContents()
        # hide match and serialno column
        self.table_widget.setColumnWidth(0, 0)
        self.table_widget.setColumnWidth(1, 0)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.sortItems(0, QtCore.Qt.DescendingOrder)

    @property
    def selected_patients(self):
        '''
        selected patients (list of serialnos)
        '''
        patients = []
        rows = set()
        for index in self.table_widget.selectedIndexes():
            rows.add(index.row())
        for row in rows:
            patients.append(int(self.table_widget.item(row, 1).text()))
        return patients
