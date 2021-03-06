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

from collections import namedtuple
from functools import partial

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from openmolar.settings import localsettings
from openmolar.qt4gui.dialogs.base_dialogs import ExtendableDialog


STATIC_LIST = []
for shortcut, description in (("CR,PJ", _("Porcelain Jacket")),
                              ("CR,GO", _("Gold")),
                              ("CR,V1", _("Porcelain/Metal")),
                              ("CR,LAVA", _("Lava")),
                              ("CR,OPAL", _("Opalite")),
                              ("CR,EMAX", _("Emax")),
                              ("CR,EVER", _("Everest")),
                              ("CR,SS", _("Stainless")),
                              ("CR,SR", _("Resin")),
                              ("CR,OT", _("Other")),):
    crown_chart_button = namedtuple('CrownType',
                                    ("shortcut", "description", "tooltip"))
    crown_chart_button.description = description
    crown_chart_button.tooltip = ""
    crown_chart_button.shortcut = shortcut
    STATIC_LIST.append(crown_chart_button)


class CrownChoiceDialog(ExtendableDialog):

    def __init__(self, static, parent=None):
        ExtendableDialog.__init__(self, parent, remove_stretch=True)
        self.setWindowTitle(_("Crown Choice Dialog"))
        self.om_gui = parent
        self.chosen_shortcut = None

        scroll_area = QtWidgets.QScrollArea()
        frame = QtWidgets.QFrame()
        scroll_area.setWidget(frame)
        scroll_area.setWidgetResizable(True)
        self.but_layout = QtWidgets.QGridLayout(frame)
        self.insertWidget(scroll_area)

        self.apply_but.hide()

        if static:
            self.more_but.hide()
            self.add_buttons(STATIC_LIST)
        else:
            all_crowns_but = QtWidgets.QPushButton(
                _("Show Crowns types from all feescales"))
            all_crowns_but.clicked.connect(self._show_all_crowns)
            self.add_advanced_widget(all_crowns_but)

            self.add_buttons(
                self.om_gui.pt.fee_table.ui_lists["crown_buttons"])

    def sizeHint(self):
        return QtCore.QSize(400, 500)

    def add_buttons(self, crown_chart_buttons):
        while self.but_layout.count():
            widget_item = self.but_layout.takeAt(0)
            widget_item.widget().setParent(None)
        row = 0
        for row, crown_button in enumerate(crown_chart_buttons):
            but = QtWidgets.QPushButton(crown_button.description)
            but.setToolTip(crown_button.tooltip)
            but.clicked.connect(
                partial(self.but_clicked, crown_button.shortcut))
            self.but_layout.addWidget(but, row // 2, row % 2)
        self.but_layout.setRowStretch((row + 2) // 2, 100)

    def _show_all_crowns(self):
        self.add_buttons(localsettings.FEETABLES.ui_crown_chart_buttons)
        self.show_extension(False)

    def but_clicked(self, shortcut):
        self.chosen_shortcut = shortcut
        self.accept()
