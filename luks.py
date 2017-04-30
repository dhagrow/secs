#! /usr/bin/env python

"""
pyluks | a utility for managing LUKS encrypted containers

Examples:

  Create a container. The number is the size in megabytes.

    $ luks.py create work_stuff 100

  Open a container. The default moves the container to ".<container>" and mounts
  to the container path. Use "-m" to set an explicit mount path.

    $ luks.py open work_stuff

  Close a container. The default unmounts from the container path and moves the
  container back to it's original path. "-m" to set the mount path is required
  if it was used when the container was opened.

    $ luks.py close work_stuff
"""

from __future__ import print_function, unicode_literals

import os
import sys
import shlex
import argparse
import subprocess

__author__ = 'Miguel Turner'
__version__ = '0.1.0'
__license__ = 'MIT'

CMD_ALLOC = 'dd if=/dev/urandom of="{path}" bs=1M count={size}'
CMD_EXPAND = 'dd if=/dev/urandom of="{path}" bs=1M count={size} oflag=append conv=notrunc'
CMD_FORMAT = 'cryptsetup -y luksFormat "{path}"'
CMD_OPEN = 'cryptsetup luksOpen "{path}" {name}'
CMD_CLOSE = 'cryptsetup luksClose {name}'
CMD_RESIZE = 'cryptsetup resize {name}'
CMD_ISLUKS = 'cryptsetup isLuks "{path}"'
CMD_STATUS = 'cryptsetup status "{path}"'
CMD_CREATE = 'mkfs.ext4 -j /dev/mapper/{name}'
CMD_CHECKFS = 'e2fsck -f /dev/mapper/{name}'
CMD_RESIZEFS = 'resize2fs /dev/mapper/{name}'
CMD_HIDE = 'mv "{path}" "{hide}"'
CMD_SHOW = 'mv "{hide}" "{path}"'
CMD_MKDIR = 'mkdir {mount}'
CMD_RMDIR = 'rmdir {mount}'
CMD_MOUNT = 'mount /dev/mapper/{name} {mount}'
CMD_UMOUNT = 'umount {mount}'
CMD_CHOWN = 'chown {recurse}{uid}:{gid} {path}'

def main():
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[1],
        epilog='\n'.join(__doc__.splitlines()[2:]),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(title='commands')

    sub = subparsers.add_parser('create',
        help='creates a new encrypted container')
    sub.add_argument('path', help='the path to the container')
    sub.add_argument('size', type=int,
        help='the size of the container (in megabytes)')
    sub.add_argument('-n', '--name',
        help='a mapper name (defaults to path basename)')
    sub.set_defaults(func=create_container)

    sub = subparsers.add_parser('open',
        help='opens an encrypted container')
    sub.add_argument('path', help='the path to the container')
    sub.add_argument('-m', '--mount',
        help='a mount path (default hides and mounts to container path)')
    sub.add_argument('-n', '--name',
        help='a mapper name (defaults to path basename)')
    sub.set_defaults(func=open_container)

    sub = subparsers.add_parser('close',
        help='closes an encrypted container')
    sub.add_argument('path', help='the path to the container')
    sub.add_argument('-m', '--mount',
        help='a mount path (default unmounts and restores container path)')
    sub.add_argument('-n', '--name',
        help='a mapper name (defaults to path basename)')
    sub.set_defaults(func=close_container)

    sub = subparsers.add_parser('expand',
        help='expands an encrypted container')
    sub.add_argument('path', help='the path to the container')
    sub.add_argument('size', type=int,
        help='the amount to expand the container (in megabytes)')
    sub.add_argument('-n', '--name',
        help='a mapper name (defaults to path basename)')
    sub.set_defaults(func=expand_container)

    args = parser.parse_args()
    if not args.func:
        sys.exit(parser.format_usage().rstrip())

    if os.geteuid() != 0:
        sys.exit('! must be run as root')

    args.name = args.name or os.path.basename(args.path)
    args.func(vars(args))

def create_container(args):
    if args['size'] < 3:
        sys.exit('! size must be at least 3MB')
    call(CMD_ALLOC, args)
    chown(args['path'])
    call(CMD_FORMAT, args)
    call(CMD_OPEN, args)
    call(CMD_CREATE, args)
    call(CMD_CLOSE, args)

def open_container(args):
    if is_active(args):
        sys.exit('! container already open')
    if not is_luks(args):
        sys.exit('! not a luks container: {}'.format(args['path']))
    call(CMD_OPEN, args)
    if not args['mount']:
        # move ./container to ./.container and mount to ./container
        args['hide'] = os.path.join(
            os.path.dirname(args['path']), '.' + args['path'])
        call(CMD_HIDE, args)
        args['mount'] = args['path']
    call(CMD_MKDIR, args, exit_on_error=False)
    call(CMD_MOUNT, args)
    chown(args['mount'], recurse=True)

def close_container(args):
    if not is_active(args):
        sys.exit('! container is not open')
    auto_mount = not args['mount']
    if auto_mount:
        args['mount'] = args['path']
    call(CMD_UMOUNT, args, exit_on_error=False)
    call(CMD_RMDIR, args, exit_on_error=False)
    if auto_mount:
        # unmount ./container and move ./.container to ./container
        args['hide'] = os.path.join(
            os.path.dirname(args['path']), '.' + args['path'])
        call(CMD_SHOW, args)
    call(CMD_CLOSE, args)

def expand_container(args):
    if is_active(args):
        sys.exit('! container must be closed before it can be expanded')
    if not is_luks(args):
        sys.exit('! not a luks container: {}'.format(args['path']))
    call(CMD_EXPAND, args)
    call(CMD_OPEN, args)
    call(CMD_RESIZE, args)
    call(CMD_CHECKFS, args)
    call(CMD_RESIZEFS, args)
    call(CMD_CLOSE, args)

def call(template, args, exit_on_error=True):
    """Executes a command based on *template* filled in from *args*."""
    cmd = template.format(**args)
    print('>', cmd)
    try:
        subprocess.check_call(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        msg = '! command failed: {}'.format(e)
        (sys.exit if exit_on_error else print)(msg)

def is_luks(args):
    cmd = CMD_ISLUKS.format(**args)
    print('>', cmd)
    code = subprocess.call(shlex.split(cmd))
    return True if code == 0 else  False

def is_active(args):
    cmd = CMD_STATUS.format(**args)
    print('>', cmd)
    code = subprocess.call(shlex.split(cmd))
    return True if code == 0 else  False

def chown(path, recurse=False):
    """Sets the owner of *path* to the user calling sudo."""
    env = os.environ
    call(CMD_CHOWN, {
        'recurse': '-R ' if recurse else '',
        'uid': env['SUDO_UID'],
        'gid': env['SUDO_GID'],
        'path': path,
        })

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
