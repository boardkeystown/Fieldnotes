"""Run inside UBI7/Python 3.8. Preparation is online; verification is offline."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import socket
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

PROJECT = Path('/workspace')
KIT = Path('/kit')
ENV = dict(os.environ, PIP_DISABLE_PIP_VERSION_CHECK='1', PIP_NO_CACHE_DIR='1')

def run(*args, **kwargs):
    print('+ ' + ' '.join(str(a) for a in args), flush=True)
    return subprocess.run([str(a) for a in args], check=True, env=ENV, **kwargs)

def venv(folder):
    run(sys.executable, '-m', 'venv', folder)
    python = folder / 'bin/python'
    run(python, '-m', 'pip', 'install', '--no-index', '--find-links', KIT / 'bootstrap', 'pip==24.3.1')
    return python

def prepare_local():
    (KIT / 'bootstrap').mkdir(parents=True, exist_ok=True)
    (KIT / 'wheelhouse').mkdir(parents=True, exist_ok=True)
    run(sys.executable, '-m', 'pip', 'download', '--only-binary=:all:', '--dest', KIT / 'bootstrap', 'pip==24.3.1')
    with tempfile.TemporaryDirectory(prefix='fieldnotes-prepare-') as temporary:
        python = venv(Path(temporary) / 'venv')
        requirements = PROJECT / 'tests/rhel7/requirements.lock'
        if not requirements.exists():
            requirements = PROJECT / 'tests/rhel7/requirements.in'
        run(python, '-m', 'pip', 'install', '--only-binary=:all:', '-r', requirements)
        run(python, '-m', 'pip', 'check')
        result = run(python, '-m', 'pip', 'freeze', stdout=subprocess.PIPE, text=True)
        (KIT / 'requirements.lock').write_text(result.stdout, encoding='utf-8')
        run(python, '-m', 'pip', 'download', '--only-binary=:all:', '-r', KIT / 'requirements.lock', '--dest', KIT / 'wheelhouse')
    checksums = {str(p.relative_to(KIT)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted(KIT.rglob('*.whl'))}
    checksums['requirements.lock'] = hashlib.sha256((KIT / 'requirements.lock').read_bytes()).hexdigest()
    (KIT / 'checksums.json').write_text(json.dumps(checksums, indent=2), encoding='utf-8')
    print('PREPARED: Linux/Python 3.8 dependency kit', flush=True)

def export_tree(source, destination):
    # Windows bind mounts may not support chmod/copystat from container UID 1001.
    destination.mkdir(parents=True, exist_ok=True)
    for path in source.rglob('*'):
        target = destination / path.relative_to(source)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)

def prepare():
    global KIT
    destination = KIT
    try:
        with tempfile.TemporaryDirectory(prefix='fieldnotes-download-') as temporary:
            KIT = Path(temporary)
            prepare_local()
            export_tree(KIT, destination)
    finally:
        KIT = destination

def verify():
    interfaces = sorted(p.name for p in Path('/sys/class/net').iterdir())
    if interfaces != ['lo']:
        raise RuntimeError('Offline verification requires --network=none; interfaces: ' + repr(interfaces))
    with socket.socket() as connection:
        connection.settimeout(2)
        status = connection.connect_ex(('1.1.1.1', 443))
        if status == 0:
            raise RuntimeError('External networking is still available')
    print('PASS: loopback-only network; outbound connection failed ({})'.format(status), flush=True)
    for name, expected in json.loads((KIT / 'checksums.json').read_text()).items():
        if hashlib.sha256((KIT / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Dependency checksum mismatch: ' + name)
    with tempfile.TemporaryDirectory(prefix='fieldnotes-offline-') as temporary:
        work = Path(temporary)
        python = venv(work / 'venv')
        run(python, '-m', 'pip', 'install', '--no-index', '--no-cache-dir', '--find-links=/kit/wheelhouse', '-r', KIT / 'requirements.lock')
        run(python, '-m', 'pip', 'check')
        project = work / 'project'
        project.mkdir()
        for name in ('docs', 'theme', 'hooks', 'tools'):
            shutil.copytree(PROJECT / name, project / name, ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('mkdocs.yml', 'vendor-manifest.json'):
            shutil.copy2(PROJECT / name, project / name)
        run(python, '-m', 'mkdocs', 'build', '--strict', cwd=project)
        run(python, 'tools/verify_offline.py', cwd=project)
        # Exercise writing and rebuilding while still disconnected.
        index = project / 'docs/index.md'
        with index.open('a', encoding='utf-8') as output:
            output.write('\n\n## Container offline authoring check\n\nEdited and rebuilt without networking.\n')
        run(python, '-m', 'mkdocs', 'build', '--strict', cwd=project)
        run(python, 'tools/verify_offline.py', cwd=project)
        if 'Container offline authoring check' not in (project / 'site/index.html').read_text():
            raise RuntimeError('Edited documentation missing from generated HTML')
        if 'Container offline authoring check' not in (project / 'site/assets/search-index.js').read_text():
            raise RuntimeError('Edited documentation missing from search')
        version = run(python, '-m', 'mkdocs', '--version', stdout=subprocess.PIPE, text=True).stdout.strip()
        output = KIT / 'site'
        export_tree(project / 'site', output)
        report = dict(result='PASS', tested_at=datetime.now(timezone.utc).isoformat(),
                      image=os.environ.get('FIELDNOTES_IMAGE'), redhat_release=Path('/etc/redhat-release').read_text().strip(),
                      python=platform.python_version(), architecture=platform.machine(), libc=platform.libc_ver(),
                      mkdocs=version, network_interfaces=interfaces, outbound_connection_errno=status,
                      checks=['fresh isolated venv', 'offline pip bootstrap', 'offline dependency installation',
                              'pip check', 'strict build', 'local asset/link/font verification',
                              'offline Markdown edit and rebuild', 'search index updated'],
                      wheels=len(list((KIT / 'wheelhouse').glob('*.whl'))),
                      limitations='Browser rendering and the host RHEL 7 kernel are not tested by this container check.')
        (KIT / 'result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report, indent=2), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare', 'verify'])
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 8):
        raise RuntimeError('This test requires Python 3.8, got ' + sys.version)
    if 'release 7.' not in Path('/etc/redhat-release').read_text():
        raise RuntimeError('This test requires a RHEL 7 userspace')
    prepare() if args.mode == 'prepare' else verify()
