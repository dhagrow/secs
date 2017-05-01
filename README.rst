pyluks
======

A utility for managing LUKS encrypted containers.

Purpose
-------

If you are unfamiliar with LUKS_ encryption, it is most commonly used to encrypt
entire disk partitions on Linux. However, it is also capable of encrypting files
that can be mounted as a loop device, allowing you to create portable encrypted
containers to keep different types of sensitive data isolated.

This script is a wrapper to simplify the steps required to create and use these
containers.

Examples
--------

Root access (via sudo) is required for all commands.

Create a container. The number is the size in megabytes.

.. code-block::

    $ sudo crypt create work_stuff 100

Open a container. The default moves the container to `.<container>` and mounts
to the container path. Use `-m` to set an explicit mount path.

.. code-block::

    $ sudo crypt open work_stuff

Close a container. The default unmounts from the container path and moves the
container back to it's original path. `-m` to set the mount path is required
if it was used when the container was opened.

.. code-block::

    $ sudo crypt close work_stuff

Expand a container. The number is the amount in megabytes to increase the size
of the container by.

.. code-block::

    $ sudo crypt expand work_stuff 10

Implementation
--------------

*crypt* is based on the LUKS_ specification. Specifically, it requires that
*cryptsetup* be available. It is currently written to use *ext4* as the
container filesystem. As such, this script will likely only work on Linux
systems.

There are no external Python dependencies. The script may be freely copied
anywhere, as long as Python 2 or 3 is available.

Related
-------

* Tomb_ - A similar tool, written for zsh.
* _Tomber and _Mausoleum - Python wrappers for Tomb_.
* LibreCrypt_ - May be useful to access your LUKS containers from Windows.

.. _LUKS: https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup
.. _Tomb: https://www.dyne.org/software/tomb/
.. _Tomber: https://pypi.python.org/pypi/tomber
.. _Mausoleum: https://pypi.python.org/pypi/mausoleum
.. _LibreCrypt: https://github.com/t-d-k/LibreCrypt
