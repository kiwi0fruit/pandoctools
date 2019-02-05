#!/bin/bash
mathjax="$PREFIX/lib/mathjax"
mkdir -p "$mathjax"

mv config "$mathjax/"
mv docs "$mathjax/"
mv extensions "$mathjax/"
mv fonts "$mathjax/"
mv jax "$mathjax/"
mv localization "$mathjax/"
mv test "$mathjax/"
mv unpacked "$mathjax/"

rm *.md ".gitignore" ".npmignore" ".travis.yml" "bower.json" "composer.json" "latest.js" "package.json"
cwd="$(pwd)" && cp "$cwd" "$mathjax/"
cd "$mathjax" && rm *.sh LICENSE && cd "$cwd"

mkdir -p "$PREFIX/bin"
cp "${RECIPE_DIR}/.mathjax-post-link.sh" "$PREFIX/bin/"
