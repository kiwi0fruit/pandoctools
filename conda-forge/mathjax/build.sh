#!/bin/bash
mkdir -p "$PREFIX/lib"
mv "MathJax-${PKG_VERSION}" "$PREFIX/lib/mathjax"
mkdir -p "$PREFIX/bin"
cp "${RECIPE_DIR}/.mathjax-post-link.sh" "$PREFIX/bin/"
