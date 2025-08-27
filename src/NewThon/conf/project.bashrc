(return 0 2>/dev/null) || echo 'this should be sourced not executed | use:  ./.integrate OR use: source .venv/bin/activate '

function pyversion() {
   printf $("${1}" --version|tr -d [:alpha:][:blank:] 2>0)
}
function testenv(){
	local TEST_FOLDER TEST_VENV
	TEST_FOLDER=$( pwd )
	TEST_LIB="${TEST_FOLDER}/.lib"
	TEST_VENV="${TEST_FOLDER}/.venv"

	[[ -e "${TEST_VENV}" ]] && PROJECT_VENV="${TEST_VENV}"    && export PROJECT_VENV
    [[ -e "${TEST_VENV}" ]] && PROJECT_HOME="${TEST_FOLDER}"  && export PROJECT_HOME

}
testenv

_OLD_VIRTUAL_PATH="${PATH}"
_OLD_VIRTUAL_PS1="${PS1:-}"

[[ -n "${PYTHONHOME}" ]] && _OLD_VIRTUAL_PYTHONHOME="${PYTHONHOME:-}" &&  unset  PYTHONHOME
[[ -e "${PROJECT_HOME}/.bin"  ]] && PROJECT_BIN="${PROJECT_HOME}/.bin"     && export PROJECT_BIN
[[ -e "${PROJECT_VENV}/bin"   ]] && PROJECT_VENV_BIN="${PROJECT_VENV}/bin" && export PROJECT_VENV_BIN
[[ -e "${PROJECT_VENV}" ]] && PROJECT_VENV_REAL=$( readlink -f "${PROJECT_VENV}" ) && export PROJECT_VENV_REAL

[[ ":${PATH}:" != *":${PROJECT_BIN}:"*      ]]   && PATH="${PROJECT_BIN}:${PATH}"      && export PATH
[[ ":${PATH}:" != *":${PROJECT_VENV_BIN}:"* ]]   && PATH="${PROJECT_VENV_BIN}:${PATH}" && export PATH

PROJECT_NAME=$( basename "${PROJECT_HOME}" )
PROJECT_PYTHON_VERSION=$( pyversion $(which python))

PS1="\[\e[1;37m\]( \[\e[1;33m\]${PROJECT_NAME}\[\e[0;29m\] \[\e[0;35m\]py-\[\e[1;35m\]${PROJECT_PYTHON_VERSION}\[\e[1;37m\] ) ${_OLD_VIRTUAL_PS1}"
VIRTUAL_ENV_PROMPT="(${PROJECT_NAME}  py-${PROJECT_PYTHON_VERSION}) "

printf '┌─────────────────────────────────────────────────────────────────────────────┐\n'
python -c "print('│\x1b[3G\x1b[1;33mPROJECT:\x1b[15G\x1b[1;3;38;2;255;128;0m${PROJECT_NAME}\x1b[79G\x1b[m│')"
printf '├─────────────────────────────────────────────────────────────────────────────┤\n'
python -c "print('│\x1b[3G\x1b[1;29mHome   :\x1b[20G\x1b[0;3;36m','.'+'/'.join('$(realpath "${PROJECT_HOME}")'.split('/'))[-60:],'\x1b[79G\x1b[m│')"
python -c "print('│\x1b[3G\x1b[1;29mVenv   :\x1b[20G\x1b[0;3;36m','.'+'"${PROJECT_VENV}"'.split('"${PROJECT_NAME}"')[-1][-60:],'\x1b[79G\x1b[m│')"
[[ -n "${PROJECT_VENV}" ]]  && python -c "print('│\x1b[3G\x1b[1;29mReal   :\x1b[20G\x1b[0;3;36m','.'+'"${PROJECT_VENV_REAL}"'.split('"${PROJECT_NAME}"')[-1][-60:],'\x1b[79G\x1b[m│')"
python -c "print('│\x1b[3G\x1b[1;29mPython :\x1b[20G\x1b[0;3;38;2;255;128;0m','"${PROJECT_PYTHON_VERSION}"'[-60:],'\x1b[79G\x1b[m│')"
python -c "print('│\x1b[3G\x1b[1;29mPATH   :\x1b[16G\x1b[0;3;38;2;255;128;0m+   \x1b[0;3;36m','./'+'/'.join('"${PROJECT_BIN}"'.split('/')[-2:])[-60:],'\x1b[79G\x1b[m│')"
python -c "print('│\x1b[3G\x1b[1;29m\x1b[16G\x1b[0;3;38;2;255;128;0m+   \x1b[0;3;36m','./' +'/'.join('"${PROJECT_VENV_BIN}"'.split('/')[-2:])[-60:],'\x1b[79G\x1b[m│')"
printf '└─────────────────────────────────────────────────────────────────────────────┘\n'


export PROJECT_HOME
export PROJECT_NAME
export PROJECT_VENV
export PROJECT_VENV_BIN
export PROJECT_BIN
export PATH
export PS1
export VIRTUAL_ENV_PROMPT
export _OLD_VIRTUAL_PATH
export _OLD_VIRTUAL_PS1
export _OLD_VIRTUAL_PYTHONHOME


VIRTUAL_ENV="${PROJECT_HOME}/.venv"  #for compat.
export VIRTUAL_ENV
