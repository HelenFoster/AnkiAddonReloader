# -*- coding: utf-8 -*-
# Copyright (C) 2017  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Anki addon to reload other single-file addons (under certain conditions).

It can help speed up addon development, but should be used with caution,
 as unexpected results can occur.

The target addon can contain the functions:

- addon_reloader_before() - optional, run before reload like a cleanup
- addon_reloader_after() - optional, run after reload

Selecting "Reload addon..." from the "Tools" menu offers a choice of eligible
 addons. After reloading an addon from this menu, a new option appears:
 "Reload ADDON_NAME" (with Ctrl+R shortcut) which reloads the same one again.

When an addon is reloaded, any items which Anki holds references to will
 still exist from the previous version. Top-level code is executed again.
AddonReloader calls addon_reloader_before() before reloading the target - 
 design it to undo anything necessary, considering these two points.
For example, if you simply declared a new function and replaced one of Anki's
 functions with it, this does not need undoing, as it will be replaced with
 the new version after the addon is reloaded. However, if you used "wrap" or
 similar, this needs undoing, as it should not be done twice.

If present, AddonReloader calls addon_reloader_after() after reloading - 
 place anything here which should be executed only after reloading,
 and not when Anki starts. (Most addons won't need anything here.)

Some addons are unsuitable for reloading. Suitable addons may also break
 after certain changes - restart Anki if this happens.

Multi-file addons should instead implement their own reloading, with a minimal
 amount of code in the primary file (so it won't need modifying often).
See my KanjiVocab addon for an example.
"""

import types
import importlib

from aqt import mw
from aqt.qt import *


class AddonChooser(QDialog):
    def __init__(self, modules):
        super().__init__()
        self.setWindowTitle("Reload addon")
        
        self.layout = QVBoxLayout(self)
        self.choice = QComboBox()
        self.choice.addItems(modules.keys())
        self.layout.addWidget(self.choice)
        
        buttons = QDialogButtonBox()
        buttons.addButton(QDialogButtonBox.Ok)
        buttons.addButton(QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)


def choose_addon():
    global action_repeat
    modules = {}
    addon_names = mw.addonManager.allAddons()
    for addon_name in addon_names:
        module_name = addon_name.replace(".py", "")
        try:
            module = __import__(module_name)
        except:
            # Skip broken modules
            continue
        modules[module_name] = module

    chooser = AddonChooser(modules)
    response = chooser.exec_()
    choice = chooser.choice.currentText()
    if response == QDialog.Rejected:
        return
    if action_repeat is not None:
        mw.form.menuTools.removeAction(action_repeat)
        action_repeat = None
    if choice != "":
        new_action = QAction("Reload " + choice, mw)

        def reload_the_addon():
            # Call "before" if present
            try:
                before = modules[choice].addon_reloader_before
            except:
                before = lambda: None
            # Take "after" if present
            try:
                after = modules[choice].addon_reloader_after
            except:
                after = lambda: None
            # Execute the reloading
            before()
            reload_package(modules[choice])
            after()
        new_action.triggered.connect(reload_the_addon)
        mw.form.menuTools.addAction(new_action)
        action_repeat = new_action
        reload_the_addon()


def reload_package(package):
    """
    Recursively reload all package's child modules
    :param package: package imported via __import__()
    """
    assert(hasattr(package, "__package__"))
    fn = package.__file__
    fn_dir = os.path.dirname(fn) + os.sep
    module_visit = {fn}
    del fn

    def reload_recursive_ex(module):
        importlib.reload(module)

        for module_child in vars(module).values():
            if isinstance(module_child, types.ModuleType):
                fn_child = getattr(module_child, "__file__", None)
                if (fn_child is not None) and fn_child.startswith(fn_dir):
                    if fn_child not in module_visit:
                        module_visit.add(fn_child)
                        reload_recursive_ex(module_child)

    return reload_recursive_ex(package)


action_repeat = None
action_choose = QAction("Reload addon...", mw)
action_choose.triggered.connect(choose_addon)
mw.form.menuTools.addAction(action_choose)
