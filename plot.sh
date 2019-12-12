#!/bin/bash
gnuplot -persist << "EOF"
    set data style linepoints
    show timestamp
    set xlabel "time (seconds)"
    set ylabel "Segments (cwnd)"
    plot "./home/cubictcpprobingB.txt" using 1:7 title "snd_cwd"
EOF

