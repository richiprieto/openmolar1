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

import logging
import re

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from openmolar.qt4gui.dialogs.base_dialogs import BaseDialog
from openmolar.qt4gui.dialogs.new_bridge_dialog import NewBridgeDialog

LOGGER = logging.getLogger("openmolar")


class BridgeDialog(BaseDialog):

    def __init__(self, om_gui=None):
        BaseDialog.__init__(self, om_gui)

        self.chosen_treatments = []
        self.om_gui = om_gui
        message = _("Bridge Treatment Dialog")
        self.setWindowTitle(message)
        self.header_label = QtWidgets.QLabel(message)
        self.header_label.setAlignment(QtCore.Qt.AlignCenter)

        frame = QtWidgets.QFrame()
        layout = QtWidgets.QHBoxLayout(frame)

        new_but = QtWidgets.QPushButton(_("Plan a New Bridge"))
        new_but.setMinimumSize(QtCore.QSize(150, 150))
        alt_but = QtWidgets.QPushButton(_("Recement/Repairs"))
        alt_but.setMinimumSize(QtCore.QSize(150, 150))

        layout.addWidget(new_but)
        layout.addWidget(alt_but)

        self.insertWidget(self.header_label)
        self.insertWidget(frame)

        self.apply_but.hide()

        new_but.clicked.connect(self.new_bridge)
        alt_but.clicked.connect(self.recement_bridge)

        if om_gui.ui.toothPropsWidget.is_Static:
            self.hide()
            QtCore.QTimer.singleShot(10, self.new_bridge)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def new_bridge(self):
        self.hide()
        dl = NewBridgeDialog(self)
        if dl.exec_():
            LOGGER.debug(dl.chosen_properties)
            material = dl.chosen_properties["material"]
            for key, value in dl.chosen_properties.items():
                if re.match("[ul][lr][1-8]", key) and value == "pontic":
                    self.chosen_treatments.append((key, "BR/P,%s" % material))
                elif re.match("[ul][lr][1-8]", key) and value == "retainer":
                    self.chosen_treatments.append((key, "BR/CR,%s" % material))
            self.accept()
        else:
            self.reject()

    def recement_bridge(self):
        QtWidgets.QMessageBox.information(self, "todo", "not yet implemented")
        self.reject()


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    LOGGER.setLevel(logging.DEBUG)
    dl = BridgeDialog(None)
    if dl.exec_():
        print(dl.chosen_treatments)
    else:
        print("dialog rejected")
