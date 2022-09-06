# goCTF_GUI_1.1.0
Python libraries used: PyQt5, sys, os, glob, subprocess, decimal, matplotlib, numpy, math, re. 
These can be installed either directly through Linux (terminal in Mac): pip install “library name”.
Another convenient way is to install Anaconda, which will include all of these libraries. 

Mrc files: Original micrograph in mrc format. 

How to Start: Direct to the folder which has “goCTF_GUI_1.1.0.py”, and run “python3 goCTF_GUI_1.1.0.py”; another way is to open the “goCTF_GUI_1.1.0.py” with a code editor and run. 

The Graphic User Interface (GUI) provides three functions:

Particles Split: Split the particles star file into multiple individual star files. First, locate particles.star directory, and click “Particles Split”. After the text box displaying the result, the GUI will create a new folder “particles_split_x” (x will be a serial number), which stores the split star files. 
Run goCTF and calculate the title degree: First locate directories of split star files from previous step and mrc files. Note: star files and mrc files need to have paired file names. After that, adjust the parameters and click “Run goCTF”. After all the calculation is finished, a “Done” will be displayed in the python terminal/terminal, and a “job_x” folder will be created within the directory of split star files (particles_split_x). Within the job folder, new _goCTF.star files will be stored and there will be an “output_statistics.txt” recording all the details of the calculation. Optionally, “Plot and Calculate tilt degree” can show the goCTF results through plot and calculate the tilt degree. 
_goCTF.star files merge: After finishing calculation, you can merge all of the new generated _goCTF.star files back to one file. Using Step 3 to locate the “job_x” folder, and a “particles_goCTF.star” file will be generated. This file has the same format as the pre-split particles star file. 

These three steps can be ran separately. You can skip Step 1 and use the same “particles_split_x” folder generated before to run multiple tests and generate several “job_x” folders; you can directly use Step 3 to merge _goCTF.star files within any generated job folder.

Contact: 
Min Su: minsuemc@gmail.com
Chenlin Zhang: zchenlin@umich.edu 
