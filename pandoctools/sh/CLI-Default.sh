# These settings work only with CLI Pandoctools usage.
# They do not change Atom package behavior.
# Uses predefined variable:
#   ${GUI} (TRUE if in Atom package mode)

if [ "${GUI}" != "TRUE" ]; then
    conda_env=""
    env_path=""
    python_path=""
fi
