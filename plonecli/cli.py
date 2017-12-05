# -*- coding: utf-8 -*-
"""Console script for plonecli."""

from __future__ import absolute_import
from pkg_resources import WorkingSet
from plonecli.exceptions import NoSuchValue
from plonecli.exceptions import NotInPackageError
from plonecli.registry import template_registry as reg

import click
import os
import subprocess
try:
    from plonecli.instance import main as instance_main
    from plonecli.zeoserver import main as zeoserver_main
    from plonecli.zeopack import main as zeopack_main
    HAS_ZOPE_AND_ZEO = True
except ImportError:
    HAS_ZOPE_AND_ZEO = False


def echo(msg, fg='green', reverse=False):
    click.echo(click.style(msg, fg=fg, reverse=reverse))


def get_templates(ctx, args, incomplete):
    """Return a list of available mr.bob templates."""
    templates = reg.get_templates()
    return templates


@click.group(
    chain=True,
    context_settings={'help_option_names': ['-h', '--help']},
    invoke_without_command=True,
)
@click.option('-l', '--list-templates', 'list_templates', is_flag=True)
@click.option('-V', '--versions', 'versions', is_flag=True)
@click.pass_context
def cli(context, list_templates, versions):
    """Plone Command Line Interface (CLI)"""
    context.obj = {}
    context.obj['target_dir'] = reg.root_folder
    context.obj['python'] = reg.bob_config.python
    if list_templates:
        click.echo(reg.list_templates())
    if versions:
        ws = WorkingSet()
        bobtemplates_dist = ws.by_key['bobtemplates.plone']
        bobtemplates_version = bobtemplates_dist.version
        plonecli_version = ws.by_key['plonecli'].version
        version_str = """Available packages:\n
        plonecli : {0}\n
        bobtemplates.plone: {1}\n""".format(
            plonecli_version, bobtemplates_version
        )
        click.echo(version_str)


if not reg.root_folder:
    @cli.command()
    @click.argument('template', type=click.STRING, autocompletion=get_templates)
    @click.argument('name')
    @click.pass_context
    def create(context, template, name):
        """Create a new Plone package"""
        bobtemplate = reg.resolve_template_name(template)
        if bobtemplate is None:
            raise NoSuchValue(
                context.command.name, template, possibilities=reg.get_templates()
            )
        cur_dir = os.getcwd()
        context.obj['target_dir'] = '{0}/{1}'.format(cur_dir, name)
        echo(
            '\nRUN: mrbob {0} -O {1}'.format(bobtemplate, name),
            fg='green',
            reverse=True,
        )
        subprocess.call(['mrbob', bobtemplate, '-O', name])


if reg.root_folder:
    @cli.command()
    @click.argument('template', type=click.STRING, autocompletion=get_templates)
    @click.pass_context
    def add(context, template):
        """Add features to your existing Plone package"""
        if context.obj.get('target_dir', None) is None:
            raise NotInPackageError(context.command.name)
        bobtemplate = reg.resolve_template_name(template)
        if bobtemplate is None:
            raise NoSuchValue(
                context.command.name, template, possibilities=reg.get_templates()
            )
        echo('\nRUN: mrbob {0}'.format(bobtemplate), fg='green', reverse=True)
        subprocess.call(['mrbob', bobtemplate])


@cli.command('virtualenv')
@click.option('-c', '--clean', is_flag=True)
@click.option('-p', '--python', help='Python interpreter to use')
@click.pass_context
def create_virtualenv(context, clean, python):
    """Create/update the local virtual environment for the Plone package"""
    if context.obj.get('target_dir', None) is None:
        raise NotInPackageError(context.command.name)
    python = python or context.obj.get('python')
    params = ['virtualenv', '.', '-p', python]
    if clean:
        params.append('--clear')
    echo('\nRUN: {0}'.format(' '.join(params)), fg='green', reverse=True)
    subprocess.call(params, cwd=context.obj['target_dir'])


@cli.command('requirements')
@click.pass_context
def install_requirements(context):
    """Install the local package requirements"""

    if context.obj.get('target_dir', None) is None:
        raise NotInPackageError(context.command.name)
    params = ['./bin/pip', 'install', '-r', 'requirements.txt', '--upgrade']
    echo('\nRUN: {0}'.format(' '.join(params)), fg='green', reverse=True)
    subprocess.call(params, cwd=context.obj['target_dir'])


@cli.command('buildout')
@click.option('-c', '--clean', count=True)
@click.pass_context
def run_buildout(context, clean):
    """Run the package buildout"""
    if context.obj.get('target_dir', None) is None:
        raise NotInPackageError(context.command.name)
    params = ['./bin/buildout']
    if clean:
        params.append('-n')
    echo('\nRUN: {0}'.format(' '.join(params)), fg='green', reverse=True)
    subprocess.call(params, cwd=context.obj['target_dir'])


@cli.command('serve')
@click.pass_context
def run_serve(context):
    """Run the Plone client in foreground mode"""
    if context.obj.get('target_dir', None) is None:
        raise NotInPackageError(context.command.name)
    params = ['./bin/instance', 'fg']
    echo('\nRUN: {0}'.format(' '.join(params)), fg='green', reverse=True)
    echo('\nINFO: Open this in a Web Browser: http://localhost:8080')
    echo('INFO: You can stop it by pressing CTRL + c\n')
    subprocess.call(params, cwd=context.obj['target_dir'])


@cli.command('test')
@click.option('-a', '--all', 'all', is_flag=True)
@click.option('-t', '--test', 'test')
@click.option('-s', '--package', 'package')
@click.pass_context
def run_test(context, all, test, package):
    """Run the tests in your package"""
    if context.obj.get('target_dir', None) is None:
        raise NotInPackageError(context.command.name)
    params = ['./bin/test']
    if test:
        params.append('--test')
        params.append(test)
    if package:
        params.append('--package')
        params.append(package)
    if all:
        params.append('--all')

    echo('\nRUN: {0}'.format(' '.join(params)), fg='green', reverse=True)
    subprocess.call(params, cwd=context.obj['target_dir'])


@cli.command('debug')
@click.pass_context
def run_debug(context):
    """Run the Plone client in debug mode"""
    if context.obj.get('target_dir', None) is None:
        raise NotInPackageError(context.command.name)
    params = ['./bin/instance', 'debug']
    echo('\nRUN: {0}'.format(' '.join(params)), fg='green', reverse=True)
    echo('INFO: You can stop it by pressing CTRL + c\n')
    subprocess.call(params, cwd=context.obj['target_dir'])


@cli.command()
@click.option('-c', '--clean', count=True)
@click.option('-p', '--python', help='Python interpreter to use')
@click.pass_context
def build(context, clean, python=None):
    """Bootstrap and build the package"""
    target_dir = context.obj.get('target_dir', None)
    python = python or context.obj.get('python')
    if target_dir is None:
        raise NotInPackageError(context.command.name)
    if clean:
        context.invoke(create_virtualenv, clean=True, python=python)
    else:
        context.invoke(create_virtualenv, python=python)
    context.invoke(install_requirements)
    context.invoke(run_buildout, clean=clean)
    # context.forward(run_buildout)


@cli.command()
def config():
    """Configure mr.bob global settings"""
    params = ['mrbob', 'plonecli:configure_mrbob']
    echo('\nRUN: {0}'.format(' '.join(params)), fg='green', reverse=True)
    subprocess.call(params)


if HAS_ZOPE_AND_ZEO:
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


if HAS_ZOPE_AND_ZEO:
    @cli.command('zeoserver')
    @click.option('-C', metavar='<path>',
                  help='path of the zeo.conf for the server.')
    def zeoserver(*args, **kwargs):
        """Serve a ZEO server in foreground"""
        os.environ['SUPERVISOR_ENABLED'] = "1"
        zeoserver_main(sys.argv[2:])


if HAS_ZOPE_AND_ZEO:
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
