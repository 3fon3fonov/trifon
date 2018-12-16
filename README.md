
**T**ransit and **R**adial velocity **I**nteractive **F**itting tool for **O**rbital analysis and **N**-body simulations

(Because of a lack of better name and for fun)

Very powerfull and fast GUI tool for exoplanet orbital analysis. It uses a brang new RV fitting library called "RVmod", which can model the Stellar reflex motion caused by dynamicaly interacting planets in multi planetary systems.

![trifon_rvmod](https://user-images.githubusercontent.com/44244057/47589870-ccc4a400-d96a-11e8-8de0-3ea3ceed1a37.jpg)

**WARNING!** This tool is under active development and its functionality is enhanced on a daily basis! Therefore, although very unlikely, the version you download today may not be fully compatible with the version uploaded tomorrow! Use at your own risk!

What works:

* Periodograms.
* RVs Keplerian and Dynamical modeling + GP (only one GP kernel integrated so far).
* RVs MCMC sampling/modeling.
* RV auto-fit (automated planet-finder algortm).
* Long-term stability check of multiplanet systems using SyMBA, MVS, MVS with GR precession term
* Interactive plots.
* Import/Export of work sessions and multi-sessions. 
* Text editor/Calculator/Bash-shell widgets.
* Integrated Jupyter widget shell.

What is to be implemented:

* Transit modeling (soon to be included)
* Combined modeling of data (Transit + RV + Astrometry +  GP/Moving avarage modeling, at once). 
* Variouse of minimization/sampling methods.
* Some more GUI plots and plot functionality.
* GUI accsess to parameter limits and priors (there, but not connected with RVmod, yet)
* Many minor glitches and bugs to be fixed.
* For more detailed TBD list see: "focus_matrix_TBFixed.doc".

If you use this tool and you find a bug or a problem, please report it!
