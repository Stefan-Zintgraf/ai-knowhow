This brainstorming skill shall be enhanced.

Currently, it will store new topics within the BRAINSTORMING_FOLDER folder. Alternatively, it should be possible to do the brainstorming in the current folder (for example to start brainstorming about a topic located in the current project). 
Thus, the first step of the skill shall be to ask the user what he wants to do:
a) run a new brainstorming topic inside the BRAINSTORMING_FOLDER (the skill shall show where BRAINSTORMING folder points to? 
   If the user says "yes", then the BRAINSTORMING_FOLDER  environment variable shall be created in case it does not yet exist. 
   If it does exist, the skill shall confirm to use this folder or to set the folder BRAINSTORMING_FOLDER  environment variable at a new location.
   In a first step, the bmad-method may have to be installed first in the topic folder, if it is not yet installed.
   Only this module shall then be installed: cis
b) run the brainstormin in the current folder? 
   If the user says "yes", then in a first step, the bmad-method may have to be installed first, if it is not yet installed.
   These modules shall then be installed: cis, bmm
You may have to adjust install-bmad.bat

Also, the skill shall be automatically tested using the sonnet model.
You must automatically verify, if the brainstorming skill works properly and supports the above requested features.
A log shall be made for all use cases to document the tests have been run successfully.

