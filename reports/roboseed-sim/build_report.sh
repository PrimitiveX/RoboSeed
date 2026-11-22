#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p _build

xelatex -interaction=nonstopmode -halt-on-error -output-directory=_build main.tex > _build/build.log 2>&1
xelatex -interaction=nonstopmode -halt-on-error -output-directory=_build main.tex >> _build/build.log 2>&1

# Dense, angled plot labels can trigger Ghostscript's page auto-rotation.
# Preserve the orientation authored by LaTeX when producing the reader PDF.
publish_dir=../../docs/report/roboseed-sim
mkdir -p "$publish_dir"
temporary_pdf="$publish_dir/RoboSeed-Sim_zh.tmp.pdf"
trap 'rm -f -- "$temporary_pdf"' EXIT
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
  -dAutoRotatePages=/None -sOutputFile="$temporary_pdf" _build/main.pdf
gs -q -dNOPAUSE -dBATCH -sDEVICE=nullpage "$temporary_pdf"
mv -- "$temporary_pdf" "$publish_dir/RoboSeed-Sim_zh.pdf"
printf 'Published reader PDF: %s/RoboSeed-Sim_zh.pdf\n' "$publish_dir"
