# pyluks
A utility for managing LUKS encrypted containers

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
