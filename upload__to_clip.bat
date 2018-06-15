:: universal script for running similar named script in an
:: activated python environment: copies commands to the clipboard
@set this=%~0
(
echo cd /d %cd%
echo call "%this:~0,-13%.bat"
) | clip
