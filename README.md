# Project Overview

This repository contains supporting Python code for automated inter-lamellar spacing measurements discussed in
"Microstructure transition gradients in titanium dissimilar alloy (Ti-5Al-5V-5Mo-3Cr/Ti-6Al-4V) tailored wire-arc
additively manufactured components", which can be found at DOI
[10.1016/j.matchar.2021.111577](https://doi.org/10.1016/j.matchar.2021.111577).

The two main scripts are ```batch_binarise.py``` (binarise the whole dataset) and ```ils_random_line-scans.py```
(perform random line scan measurements on the set of binary images). These call functions from our Python package,
Microstructural Fingerprinting Tools (mftools), which can be found at
<https://github.com/mikedwhite/microstructural-fingerprinting-tools>. Note that this package is still under development.
