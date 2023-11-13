---
subtitle: 3250.3 Intelligence artificielle I
title: Travail pratique 3 - Le Compte Est Bon
author: Nima Dekhli \& Maëlys Bühler
date: Le \today
lang: fr-CH
geometry: 
  - margin=2cm
  - includehead
  - includefoot
papersize: a4
colorlinks: true
linkcolor: blue
citecolor: MidnightBlue
urlcolor: MidnightBlue
numbersections: true
links-as-notes: true

mainfont: Latin Modern Roman
sansfont: Latin Modern Sans

documentclass: srcreport

lofTitle: Liste des figures
lolTitle: Liste des codes
listingTitle: Code
lstPrefix: 
  - code
  - codes

toc: true
toc-depth: 4
header-includes: |
    \usepackage{fancyhdr}
    \pagestyle{fancy}\usepackage{float}
    \let\origfigure=\figure
    \let\endorigfigure=\endfigure
    \renewenvironment{figure}[1][]{%
      \origfigure[H]
    }{%
      \endorigfigure
    }

---

# Introduction

## blabla

bla bla bla

# Analyse

une analyse

# Conclusion

ceci est une conclusion
