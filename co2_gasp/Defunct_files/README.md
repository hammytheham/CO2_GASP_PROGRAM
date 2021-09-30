# Welcome to trexplot

By Hamish Robertson & Tan Benjakul

We aim to deliver a plotting experience to Toughreactmech output files.

Features;

-> Only plots the last time step at the moment

-> 4/5 different types of plot

-> Custom x,y & z cross sections

-> PDF,PNG & 'custom-build' options

-> 'Custom plot' - ipython experience

-> Should work with any grids you have.

-> Supported .tec files are flow data, flow vector, displacement, stress strain, aqueous concentrations, gas volfrac, mineral abundances and saturation states.

-> You dont need a displacement file (see trexoptions) but the default is you have one in the directory. It is used for the corner locations.

## To install

This doesn't work well yet... Will get it working some moon in the future....Much like I need to do some maintenance and clean up of this script. 
`pip install -i https://test.pypi.org/simple/ trexplot==1`

Just `git clone` this repo for the time being

## To get stuff to work

We supply a set of example .tec files. Move the TestFiles folder somewhere else.

`cd` into the TestFiles folder.

run `ipython SOME-PATH/Trexplot/trexplot.py`

This will use the `trexoptions.py` file which controls plotting. The trex options supplied by default has only a few options turned on. You use this scipt to 'drive the bus'.

Use the trex_fig_return.py script as an example of methods to personally modify the returned graphics.

Drop a message if you want new features or have bugs. 

If you do use this code and feel inclined to acknowledge;

H. Robertson & T.Benjakul, Trexplot, (2019), GitHub repository, https://github.com/hammytheham/trexplot/


