pandoc about.md \
    -o about.html \
    --section-divs \
    --citeproc \
    --bibliography="references.bib" \
    --csl="apa.csl" \
    --metadata link-citations=true