# pyluks

A utility for managing LUKS encrypted containers.

## Purpose

If you are unfamiliar with [LUKS](https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup)
encryption, it is most commonly used to encrypt entire disk partitions. However,
it is also capable of encrypting files that can be mounted as a loop device,
allowing you to create portable encrypted containers to keep different types of
sensitive data isolated.

This script is a simple wrapper to simplify the steps required to create and
use these containers.

## Examples

Create a container. The number is the size in megabytes.

```shell
$ luks.py create work_stuff 100
```

Open a container. The default moves the container to ".<container>" and mounts
to the container path. Use "-m" to set an explicit mount path.

```shell
$ luks.py open work_stuff
```

Close a container. The default unmounts from the container path and moves the
container back to it's original path. "-m" to set the mount path is required
if it was used when the container was opened.

```shell
$ luks.py close work_stuff
```

Expand a container. The number is the amount in megabytes to increase the size
of the container by.

```shell
$ luks.py expand work_stuff 10
```

## Implementation

`pyluks` is based on the [LUKS](https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup)
specification. Specifically, it requires that `cryptsetup` be available. It is
currently written to use `ext4` as the container filesystem. As such, this script
will likely only work on Linux systems.

There are no external Python dependencies. The script may be freely copied
anywhere, as long as Python 2 or 3 is available.

## Related

* [Tomb](https://www.dyne.org/software/tomb/)
* [LibreCrypt](https://github.com/t-d-k/LibreCrypt) - May be useful to access
  your LUKS containers from Windows.
