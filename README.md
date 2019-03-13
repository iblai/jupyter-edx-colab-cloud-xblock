# Colab XBlock

## Overview
Provides a convenient way to launch Google Colab notebooks with within EdX.

## Installation
### XBlock
* login as the root user: `sudo -i`
* `cd /edx/app/edxapp`
* Activate the EdX virtualenv: `source venvs/edxapp/bin/activate`
* New Installation:
    * `sudo -u edxapp /edx/bin/pip.edxapp install git+https://github.com/ibleducation/jupyter-edx-colab-cloud-xblock.git`
* Upgrading:
    * `sudo -u edxapp /edx/bin/pip.edxapp install --upgrade --no-deps --force-reinstall git+https://github.com/ibleducation/jupyter-edx-colab-cloud-xblock.git`

### Edx Server Setup
In the following files:
* `/edx/app/edxapp/edx-platform/lms/envs/common.py` 

Add the following at the bottom of the `INSTALLED_APPS` section:
```python
    # Colab XBlock
    'colab_xblock',
```

Restart `edxapp` via `/edx/bin/supervisorctl restart edxapp:`

* In the studio, go to the course you would like to implement this XBlock in
* Under `Settings` at the top, select `Advanced Settings`
* in the Advanced Module List, add: `"colab_xblock"`
    * ensure there is a comma after the second to last entry, and no comma exists after the last entry
* Select Save

The Google Colab Link can now be added to a unit by selecting `Colab XBlock` from the `Advanced` component menu

## How it works
Provides a button that will open a new tab/window to the provided google colab notebook.

If the link is a github link, we reformat it to a google colab link, otherwise we leave it as is.

The user can enter optional instructions or a summary that will be displayed above the link.

