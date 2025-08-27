# This file must be used with "source bin/activate" *from bash*
#make sure its sourced not executed
#(return 0 2>/dev/null) || echo 'this should be sourced not executed | use:  ./.integrate OR use: source .venv/bin/activate '

#set -o xtrace
function activate(){

	# Call hash to forget past commands. Without forgetting
	# past commands the $PATH changes we made may not be respected
	hash -r 2> /dev/null

	exec bash --rcfile "$PWD/.local/conf/project.bashrc"
}
function deactivate () {
	# reset old environment variables
	if [ -n "${_OLD_VIRTUAL_PATH:-}" ] ; then
		PATH="${_OLD_VIRTUAL_PATH:-}"
		export PATH
		unset _OLD_VIRTUAL_PATH
	fi
	if [ -n "${_OLD_VIRTUAL_PYTHONHOME:-}" ] ; then
		PYTHONHOME="${_OLD_VIRTUAL_PYTHONHOME:-}"
		export PYTHONHOME
		unset _OLD_VIRTUAL_PYTHONHOME
	fi


	if [ -n "${_OLD_VIRTUAL_PS1:-}" ] ; then
		PS1="${_OLD_VIRTUAL_PS1:-}"
		export PS1
		unset _OLD_VIRTUAL_PS1
	fi
	#these have no prev value yeet
	unset VIRTUAL_ENV
	unset VIRTUAL_ENV_PROMPT
	unset PROJECT_HOME
	unset PROJECT_NAME
	unset PROJECT_VENV
	unset PROJECT_BIN
	unset PROJECT_VENV_BIN
# TODO: figure out what this does
	# Call hash to forget past commands. Without forgetting
	# past commands the $PATH changes we made may not be respected
	hash -r 2> /dev/null

	if [ ! "${1:-}" = "nondestructive" ] ; then

	# Self destruct!
	unset -f deactivate
	fi
}
# unset irrelevant variables
deactivate nondestructive
activate
