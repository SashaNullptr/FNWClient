Main Goal of FNWCLient
================

Data analytics for my personal relationships.

Installing
==========

Depedencies
-----------

Python 3.6 is **required** on the target system.


All other dependencies will be handled by `pip` during installation.

Local Install
-------------

From the project root directory run
``python3 -m pip install --user .``


Building the docs
-----------------

In order to construct the project documentation you will need to have
`Sphinx <http://www.sphinx-doc.org/en/master/>`__ installed along with
the `Read The Docs theme
package <https://github.com/rtfd/sphinx_rtd_theme>`__. Note that the
Read The Docs theme is installed with most versions of Sphinx provided
by Linux distro package managers.

Once Sphinx is installed navigate to the ``docs`` folder under the
project root directory and run the following command
``python -m sphinx -b html ./source ./build``. Note that
``python`` is **mandatory** for the docs to build correctly. Sphinx
will run and produce HTML documentation in the ``docs/build`` directory.
The root of the HTML docs can be found at ``docs/build/index.html``.
