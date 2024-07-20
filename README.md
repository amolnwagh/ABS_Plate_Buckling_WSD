# ABS_Plate_Buckling_WSD
### Calculations for plate buckling checks according to "Requirements for Buckling and Ultimate Strength Assessment for Offshore Structures (Working Stress Method)", published by American Bureau of Shipping (ABS), July 2022 Edition

* This app calculates the buckling state limit of a stiffened plated panel. 
* Such stiffened panels are typically used in hulls of ships and floating offshore structures like jack-up rigs and semi-submersibles.
* Generally, the inputs are details regarding plate panel dimensions and material properties.
* Instead of loads, the inputs are stresses, since these buckling check calculations are used typically after extracting stresses from a detailed finite element analysis model of the mentioned structures.
* Currently, the app gives buckling state limit (UC) check if you have entered the stresses.
* Even if the stresses are not input, the critical buckling state limits are calculated.
* Additionally, interactive plotly charts are presented for the values of the critical buckling stresses and UCs (if stresses are supplied) for the defined panel and also for a range of aspect ratios of the panel, keeping all other inputs same.

Streamlit app link: https://abs-plate-buckling-amolnwagh.streamlit.app/
