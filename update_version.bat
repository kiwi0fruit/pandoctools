set tagname=1.0.0
git tag -d %tagname%
git tag -d 0.4.21
git push --delete origin %tagname%
git push --delete origin 0.4.21
git tag -a %tagname%
git push --tags
pause
