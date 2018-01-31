How to release
==============

Prepare release environment
---------------------------

Install packages.

     $ pip install wheel twine

Prepare the environment file `.pypirc` on your HOME directory.


Build release files
-------------------

Clear the former build files

    $ rm -rf quantpy.egg-info/ dist/

Build the release files

    $ python setup.py sdist
    $ python setup.py bdist_wheel


Upload to PyPI
--------------

    $ twine upload --repository pypi dist/*


Confirmation
------------

    $ pip --no-cache-dir install --upgrade quantpy
