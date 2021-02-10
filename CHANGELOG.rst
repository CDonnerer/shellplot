=========
Changelog
=========

Version 0.2.0
---------------
- Added object-orientated figure API, entailed major refactor of plotting code
- Examples of figure api in docs, updated api reference
- Added option to add line in plot function
- Safeguarding number of bins in hist
- Default docs now refer to stable versions
- Added config for global options, such as figsize


Version 0.1.5
-------------
- Allow to plot multiple scatters via 2d np arrays
- Added support for datetime types
- Added pandas visualisation example docs
- General support for adding legend to plot via ``label`` keyword


Version 0.1.4
-------------
- Fixed bug in x-axis drawing, spurious rounding
- Added options to modify global figure properties, e.g. xlim, figsize, etc
- Updated docs for manually curated API reference as opposed to sphinx api-doc
- Additional tests for plots along with flexibility for pandas/ numpy/ list inputs
- Additional tests for drawing module


Version 0.1.3
-------------
- Fixed bug in x-axis drawing, now tick marks are aligned with plot
- Fixed bug in axis tick values rounding
- Fixed bug in histogram x-axis not scaling correctly
- Added ``boxplot`` plotting function


Version 0.1.2
-------------
- Refactor of axis functionality into separate module, with lots of bug fixes
  and proper testing
- Added ``barh`` plotting function
- Automatic build and deploy in travis ci


Version 0.1.1
-------------
- Added basic docs
- Added color support in ``plot`` function, with legend
- Minor refactoring and bug fixing in axis and drawing


Version 0.1
-----------

- Basic functionality of shellplot released.
- Includes ``plot`` and ``hist`` functions which print to the command line.
- Includes pandas backend api for the above
