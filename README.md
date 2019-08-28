# AddonReloader

Anki addon to reload other addons. See the comments at the top of \_\_init\_\_.py for details.

Now working with v2.1.

Original AnkiWeb: AnkiWeb: https://ankiweb.net/shared/info/348783334.

## Current Issues

- Seems to require reloading addons twice for effect to take place
- Creates new listing in Anki "Tools" menu for addon on reload
  - Possible fixes: 
    - Add a before/after hook in the desired addon
    - Look for global addon menu item data we can reference without knowing anything about the addon