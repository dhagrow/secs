SECS
====

The Simple Encrypted Container Setup (SECS) is based on the Linux Unified Key
Setup (LUKS). Because good LUKS are SECSy.

Purpose
-------

If you are unfamiliar with LUKS_ encryption, it is most commonly used to encrypt
entire disk partitions on Linux. However, it is also capable of encrypting files
which can be mounted as a loop device, allowing you to create portable encrypted
containers to keep different types of sensitive data isolated.

This script is a wrapper to simplify the steps required to create and use these
containers.

Installation
------------

SECS can be installed using *pip*.

.. code-block::

    $ sudo pip install secs
    # or
    $ pip install --user secs

Either command will install a script called *secs* which provides all the
functionality.

Examples
--------

Root access (via *sudo*) is required for all commands. The script that is
installed will call *sudo* for you.

Create a container. The number is the size in megabytes.

.. code-block::

    $ secs create work_stuff 100
    ...
    $ ls -Ap
    work_stuff

Open a container. The default moves the container to `.<container>` and mounts
to the container path. Use `-m` to set an explicit mount path.

.. code-block::

    $ secs open work_stuff
    ...
    $ ls -Ap
    work_stuff/ .work_stuff

Close a container. The default unmounts from the container path and moves the
container back to it's original path. `-m` to set the mount path is required
if it was used when the container was opened.

.. code-block::

    $ secs close work_stuff
    ...
    $ ls -Ap
    work_stuff

Expand a container. The number is the amount in megabytes to increase the size
of the container by.

.. code-block::

    $ secs expand work_stuff 10

Implementation
--------------

*secs* is written in Python and is based on the LUKS_ specification. It requires
that cryptsetup_ be available. It is currently written to use *ext4* as the
container filesystem. As such, this script will likely only work on Linux
systems.

There are no external Python dependencies. The script may be freely copied
anywhere, as long as Python 2 or 3 is available.

Related
-------

* Tomb_ - A similar tool, written for zsh.
* Tomber_ and Mausoleum_ - Python wrappers for Tomb_.
* LibreCrypt_ - May be useful to access your LUKS containers from Windows.

.. _LUKS: https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup
.. _cryptsetup: https://gitlab.com/cryptsetup/cryptsetup/
.. _Tomb: https://www.dyne.org/software/tomb/
.. _Tomber: https://pypi.python.org/pypi/tomber
.. _Mausoleum: https://pypi.python.org/pypi/mausoleum
.. _LibreCrypt: https://github.com/t-d-k/LibreCrypt
