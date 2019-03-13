
**T**ransit and **R**adial velocity **I**nteractive **F**itting tool for **O**rbital analysis and **N**-body simulations : **The Exo-Striker** 

<p align="center">
  <img width="400" src="https://github.com/3fon3fonov/trifon/blob/master/lib/33_striker.png">
</p>
 

Very powerful and fast GUI tool for exoplanet orbital analysis. It uses a brang new RV fitting library called "RVmod", which can model the Stellar reflex motion caused by dynamically interacting planets in multi planetary systems. 

![new_es](https://user-images.githubusercontent.com/44244057/53755942-20667180-3eb8-11e9-9802-530618db7e7d.png)

**WARNING!** This tool is under active development and its functionality is enhanced on a daily basis! Therefore, although very unlikely, the version you download today may not be fully compatible with the version uploaded tomorrow! Use at your own risk!

Also, please keep in mind that this software is developed mostly for my needs and for fun. I hope, however, that you may find 
it capable to solve your scientific problems, too. For updates, follow my Twitter account https://twitter.com/3fon3fonov 

What works:

* Period search: GLS periodograms (RVs, act. data) & TLS (transit data).
* Keplerian and Dynamical RV modeling. 
* Transit modeling (so far only one dataset and not tested for 2+ transiting planets)
* GP modeling (only one GP kernel integrated so far).
* Joint RVs + GP + Transit best-fit modeling.
* Joint RVs + GP + Transit MCMC sampling.
* RV auto-fit (RV automated planet-finder algortm).
* Long-term stability check of multiplanet systems using SyMBA, MVS and MVS with an GR precession.
* Variouse of minimization methods (via SciPyOp).
* Interactive plots.
* RV vs. Activity time series correlation analysis/plots.
* Import/Export of work sessions and multi-sessions. 
* Export plots to a matplotlib window for further customization.
* Export ready to use Latex tables with best-fit parameters, errors and statistics. 
* Text editor.
* Bash-shell (linux only).
* Integrated Jupyter widget shell.
* Print the GUI screen into a .jpeg image (useful for sharing quick results, just like the image above)

What is to be implemented:

* More GP kernels.
* Nested sampling. 
* Binary/Triple star modeling mode.
* Combined modeling with Astrometry.
* A larger arsenal of N-body/dynamical simulation/analysis tools. 
* Documentation, Instructions and Video tutorials.
* For more "TBD" list see: "focus_matrix_TBFixed.doc".

If you use this tool and you find a bug or a problem, please report it!



