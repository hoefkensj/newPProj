#!/usr/bin/env python
import os
from pathlib import Path

def activate(){

	def testenv():

	
		print(f'Checking \x1b[1;34m{ROOT}\x1b[m for \x1b[1mVirtual Env\x1b[m. ...',end='')
		


	def project():
		env=os.environ
		
		ROOT=Path(os.getcwd())
		VENV=Path(ROOT,".venv"	)
		VBIN=Path(VENV,"bin"	)
		BIN=Path(ROOT,".bin"	)
		GIT=Path(ROOT,".git")
		
		if VENV.exists():
			PROJECT_NAME=ROOT.name
			PROJECT_VENV=VENV
			PROJECT_VENV_BIN=VBIN
		
		if BIN.exists():
			PROJECT_BIN=BIN
		
		_OLD_VIRTUAL_PATH=env["PATH"]
		_OLD_VIRTUAL_PS1=env["PS1"]
		
		if env.get('PYTHONHOME'):
			_OLD_VIRTUAL_PYTHONHOME=env.pop('PYTHONHOME')
			
		PATH=	env["PATH"].split(':')
		if not BIN in PATH:
			PATH=[BIN,*PATH]
		if not VBIN in PATH:
			PATH=[VBIN,*PATH]
			
			
	
		PYTHON_VERSION=$( "${PROJECT_VENV}/bin/python" --version|tr -d 'Python ' )
		PS1="\[\e[1;37m\]( \[\e[1;33m\]${PROJECT_NAME}\[\e[0;29m\]-\[\e[0;35m\]py\[\e[0;34m\]${PYTHON_VERSION}\[\e[1;37m\] ) ${PS1:-}"
		VIRTUAL_ENV_PROMPT="(${PROJECT_NAME}-py${PYTHON_VERSION}) "
		
		printf '\x1b[1;3;35mProject:\x1b[m\n'
		printf '\x1b[1mName:\x1b[m\x1b[15G\x1b[1;34m%s\x1b[m\n'   "${PROJECT_NAME}"
		printf '\x1b[1mHome:\x1b[m\x1b[15G\x1b[1;34m%s\x1b[m\n'   "${PROJECT_HOME}"
		printf '\x1b[1mVenv:\x1b[m\x1b[15G\x1b[1;34m%s\x1b[m\n'   "${PROJECT_VENV}"
		printf '\x1b[1mPATH:\x1b[m\x1b[15G\x1b[1;34m+ %s\x1b[m\n' "${PROJECT_BIN}"
		printf                   '\x1b[15G\x1b[1;34m+ %s\x1b[m\n' "${PROJECT_VENV_BIN}"
		
		export PROJECT_HOME
		export PROJECT_NAME
		export PROJECT_VENV
		export PROJECT_BIN
		export PROJECT_VENV_BIN
		export PS1
		export VIRTUAL_ENV_PROMPT
		export _OLD_VIRTUAL_PATH
		export _OLD_VIRTUAL_PS1
		export _OLD_VIRTUAL_PYTHONHOME
		
		
		VIRTUAL_ENV="${PROJECT_HOME}/.venv"  #for compat.
		export VIRTUAL_ENV

	}

	testenv
	[[ -n $PROJECT_HOME ]] && project
	# Call hash to forget past commands. Without forgetting
	# past commands the $PATH changes we made may not be respected
	hash -r 2> /dev/null
}
