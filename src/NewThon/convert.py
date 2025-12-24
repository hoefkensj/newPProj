# /usr/bin/env pyhthon
import click
from pathlib import Path
import sys

venvtag= lambda :'.'.join([{'x86_64':'x64'}.get(sys.implementation.__dict__['_multiarch'].split('-')[0]),sys.platform,
	  '-'.join([sys.implementation.name,'.'.join([str(i)for i in sys.version_info[:3]])])])

def teststructure(path):
	proj=path.name
	srcdir=Path(path,'src')
	localdir=Path(path,'.local')
	venvsdir=Path(localdir,'venvs')
	venvlnk=Path(path,'.venv')
	actenv=venvtag()
	if not srcdir.exists():
		srcdir.mkdir(775)
	if not localdir.exists():
		localdir.mkdir(775)
		venvsdir.mkdir(775)
	if not venvlnk.is_symlink():
		venvlnk.rename(Path(venvsdir,'original'))

def main(path):
	p=Path(path).resolve()
