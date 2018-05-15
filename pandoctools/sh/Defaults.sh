# ${pdt_GUI} FALSE settings work only with CLI Pandoctools usage.
# They do not change Atom package behavior.
# Uses predefined variable:
#   ${pdt_GUI} (TRUE if in Atom package mode)
#   ${conda_env} (predefined if in Atom package mode)
#   ${env_path} (predefined if in Atom package mode)
#   ${python_path} (predefined if in Atom package mode)

if [ "${pdt_GUI}" != "TRUE" ]; then
    # Define default CLI python settings here:
    conda_env=""
    env_path=""
    python_path=""
fi

if [ "${python_path}" != "" ]; then
    PYTHONPATH="${python_path}"
    PATH="${python_path}/bin:$PATH"
fi
