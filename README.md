# AddonReloader

Anki addon to reload other addons. See the comments at the top of \_\_init\_\_.py for details.

Now working with v2.1.

Original AnkiWeb: AnkiWeb: https://ankiweb.net/shared/info/348783334.

## Notes

- If you do a git pull between reloads, need to restart anki
- The folder of the addon must not contain dashes or anything that wouldn't work in a normal import statement
  - e.g. anki_LL, not anki-LL

## Current Issues

- Creates new listing in Anki "Tools" menu for addon on reload
  - Possible fixes: 
    - Add a before/after hook in the desired addon
    - Look for global addon menu item data we can reference without knowing anything about the addon
