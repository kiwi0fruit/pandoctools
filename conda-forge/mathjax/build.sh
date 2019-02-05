#!/bin/bash
cp "${SRC_DIR}/MathJax-${PKG_VERSION}/LICENSE" "${SRC_DIR}/" 
mkdir -p "$PREFIX/lib"
mv "${SRC_DIR}/MathJax-${PKG_VERSION}" "$PREFIX/lib/mathjax"
mkdir -p "$PREFIX/bin"
cp "${RECIPE_DIR}/mathjax-conda" "$PREFIX/bin/"
