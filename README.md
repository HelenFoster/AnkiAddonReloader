# AddonReloader

Anki addon to reload other addons. See the comments at the top of \_\_init\_\_.py for details.

Now working with v2.1.

Original AnkiWeb: https://ankiweb.net/shared/info/348783334.

## Notes

- If you do a git pull between reloads, need to restart anki
- The folder of the addon must not contain dashes or anything that wouldn't work in a normal import statement
  - e.g. anki_LL, not anki-LL
- Without modification, if your addon creates an action item in the Anki Tools menu, reloading it will create a duplicate item for each reload.
  - Solved with an `addon_reloader_before` method in the addon's \_\_init\_\_.py:
    - ```python
      for action in mw.form.menuTools.actions():
        if action.text() == ADDON_ACTION_NAME:
          mw.form.menuTools.removeAction(action)
      ```
