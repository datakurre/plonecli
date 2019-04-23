# -*- coding: utf-8 -*-
"""Console script for plonectl."""

from __future__ import absolute_import
from pkg_resources import WorkingSet
from plonectl.instance import main as instance_main
from plonectl.zeoserver import main as zeoserver_main
from plonectl.zeopack import main as zeopack_main

import click
import os
import sys


def echo(msg, fg='green', reverse=False):
    click.echo(click.style(msg, fg=fg, reverse=reverse))


@click.group(
    chain=True,
    context_settings={'help_option_names': ['-h', '--help']},
    invoke_without_command=True,
)
@click.option('-V', '--versions', 'versions', is_flag=True)
@click.pass_context
def cli(context, versions):
    """Plone Control (CTL)"""
    context.obj = {}
    if versions:
        ws = WorkingSet()
        plonectl_version = ws.by_key['plonectl'].version
        version_str = """Available packages:\n
        plonectl : {0}\"""".format(
            plonectl_version,
        )
        click.echo(version_str)


@cli.command('instance')
@click.argument('action', nargs=-1)
@click.option('--no-request', '-R', is_flag=True,
              help='do not set up a REQUEST.')
@click.option('--no-login', '-L', is_flag=True,
              help='do not login the system user.li')
@click.option('--object-path', '-O', metavar='<path>',
              help=('traverse to <path> from the app and make available '
                    'as `obj`.'))
@click.option('-C', metavar='<path>',
              help='path of the zope.conf for the instance.')
def instance(*args, **kwargs):
    """Serve, debug or script a Plone instance"""
    instance_main(sys.argv[2:])


@cli.command('zeoserver')
@click.option('-C', metavar='<path>',
              help='path of the zeo.conf for the server.')
def zeoserver(*args, **kwargs):
    """Serve a ZEO server in foreground"""
    os.environ['SUPERVISOR_ENABLED'] = "1"
    zeoserver_main(sys.argv[2:])


@cli.command('zeopack')
@click.option('--host', '-h', type=click.STRING, metavar='<host>',
              default="127.0.0.1",
              help=('used with the -p and -S options, specifies the host '
                    'to connect to.'))
@click.option('--port', '-p', type=click.INT, metavar='<port>',
              help=('used with the -h and -S options, specifies the port '
                    'to connect to.'))
@click.option('--unix', '-U', type=click.STRING, metavar='<unix>',
              default=None,
              help=('a unix-domain-socket server to connect to, of the '
                    'form: path[:name].'))
@click.option('--days', type=click.INT, metavar='<days>', default=1,
              help='pack objects that are older than this number of days.')
@click.option('--storage', '-S', type=click.STRING, metavar='<storage>',
              default='1',
              help=('used with the -h and -p, options, or with the -U '
                    'option, specifies the storage name to use. '
                    'Defaults to 1.'))
@click.option('--blob-dir', '-B', type=click.STRING, metavar='<blob-dir>',
              help=('specifies the path to the shared blobstorage '
                    'directory'))
@click.option('--username', type=click.STRING, metavar='<username>',
              default=None,
              help='ZEO authentication username.')
@click.option('--password', type=click.STRING, metavar='<password>',
              default=None,
              help='ZEO authentication password.')
@click.option('--realm', type=click.STRING, metavar='<realm>',
              default=None,
              help='ZEO authentication realm.')
def zeopack(host, port, unix, days,
            username, password, realm, blob_dir, storage):
    """Pack ZEO server storage (blocking)"""
    if unix is None:
        host = str(host)
    else:
        host = None
        port = None
    if blob_dir is not None:
        shared_blob_dir = True
    else:
        shared_blob_dir = False
    zeopack_main(
        host,
        port,
        unix,
        str(days),
        username,
        password,
        realm,
        blob_dir,
        storage,
        shared_blob_dir
    )


if __name__ == "__main__":
    cli()
