set tagname=0.4.5
git tag -d %tagname%
git push --delete origin %tagname%
git tag -a %tagname%
git push --tags
pause
