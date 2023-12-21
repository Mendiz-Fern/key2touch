3I just wanted to have a small program that maps key presses to touchscreen directives so I can play a specific mobile game on my computer through screen mirroring. 
At the moment, it doesn't have a GUI becuase... well... it's python. I'll try to come up with a GUI at some point, since this form of doing stuff is very archaic, not gonna lie.

<h3>V0.1.0</h3>
<h4>WELCOME TO KEY2CLICK</h4>
<h5>A prototype for key2touch</h5>
Key2Click is a python program that will map key presses to mouse clicks, with its ultimate goal being to eventually map multiple simultanous key presses to touch input in a touch screen (hopefully it works with non-touchscreens as well), but for now it's one keypress for one mouse press at a time.

<h4>USAGE</h4>
To use key2touch (or key2click for now), download the zip for the repository and extract it all in the same folder, then run key2touch (remember to have python installed in your machine first).

To make a new mapping, when prompted, input 'n' and follow the terminal instructions
To use an existing mapping, input 'e' when prompted and follow the instructions

Once you're in map mode, the key2click mappings will take effect, press [esc] at any point to exit

<h4>NOTES</h4>
- you cannot map [esc] to anything, as it is the exit key
- do NOT press enter while making a new mapping at all. This will cause the mapping to crap out and the program to exit without creating your mapping
- at the moment, I still have to make an executable for this or something of the sort. I will come around to it in V1.0.0, at the moment, V0.1.0 is the first working prototype.
- Check the changelog for more details

<h3>V0.0.4</h3>
Added functionality to load an existing mapping
Added functionality to save mappings with same names
- When saving a repeat name mapping, k2t will change its name to <mapping_name>_i, where i is the number of times you've tried re-saving a mapping with that name

<h3>V0.0.3</h3>
Have a funcional mapper. this is more akin to Key-to-Click, as it doesn't emulate touch screen just yet
In order to use k2t, run the python script and follow the instructions when prompted. Some things to note though: 
- Loading profiles does not work as of V0.0.3, so every time you boot, you'll have to remake your mapping each time you open
- You cannot open any other app (at the moment) while making the mapping, but if you have it open already, you can swtich the window to it while the mapper is open

This issues will be fixed later

<h3>V0.0</h3>
Created the Python file. That's about it

