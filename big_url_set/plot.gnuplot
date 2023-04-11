set term pdfcairo
set datafile separator ','
set xlabel "URL length"
set xrange [0:1200]
set out "cycles.pdf"
set ylabel "CPU cycles"
plot "ada_url_aggregator_rome.txt" using 1:2 ti "ada::url aggregator", "ada_url_rome.txt" using 1:2 ti "ada::url"

set out "instructions.pdf"
set ylabel "instructions"
plot "ada_url_aggregator_rome.txt" using 1:4 ti "ada::url aggregator", "ada_url_rome.txt" using 1:4  ti "ada::url"