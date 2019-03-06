The various python scripts contained here are meant to provide users easy to reference methods to use for anything.
The main purpose for creating these modules is to plot event generator data (CEM, GSM, and LAQGSM) against experimental data.

>The general python modules that can be multi-purpose include the following:

*The printClass object is used to simply control printing of various messages as they are encountered. All message printing should be filtered through this function for consistency.
*The fileModule.py file contains various methods dealing with verifying the existence of files, the length of files, deleting/creating files, etc.
*The plotClass.py file contains various classes that simply interface the matplotlib utilities and add protection against user error. Multiple inheritence is used in the plot class, where users/clients only need to access the PlotClass object for most plotting needs.
*The testingModule.py is simply used to test new features that the developer intends to test, such as inheritance in the code, python's version of "public/protected/private", etc.

>Event generator specific modules include the following:
*The outputClass.py is used to read GSM/CEM/LAQGSM event generator output files and parse the various data found. This object is intended to provide clients/users with easy access to the simulated results from the event generator.
*The gsmPlotClass.py module reads an input file and, based on the specifications in the input file, creates plots by querying the simulated and experimental data loaded based on the input specifications.

These utilities were developed by Chase Juneau, a not-so-great programmer who tries his best.
>For questions, comments, suggestions, bugs, etc., contact Chase Juneau (chasem.juneau@gmail.com, [junechas@isu.edu], [chasemjun@lanl.gov])