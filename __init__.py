from .main import parse
from .form import AnkimdDialog

from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    mw.ankimd_dialog = AnkimdDialog()
    if mw.ankimd_dialog.exec():
        output_filepath = parse(path=mw.ankimd_dialog.filepath[0],
                                delimiter_front=mw.ankimd_dialog.delimiter_front_box.text(),
                                delimiter_back=mw.ankimd_dialog.delimiter_back_box.text())
        mw.handleImport(path=output_filepath)


# create a new menu item, "test"
action = QAction("Import Markdown", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

