set -e

python cvmake.py template.yml template.tex && \
latexmk -pdf -interaction=nonstopmode -output-directory=./out cv.tex && \
mv ./out/cv.pdf . && \
rm -rf ./out