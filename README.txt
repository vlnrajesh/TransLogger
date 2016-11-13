Source Code Repository : https://github.com/vlnrajesh/TransLogger
----------------------
branches:
---------
    master: current assignment
    translogger: Actual Logging functionality

How to Run the program
----------------------
1. Visit code directory
2. run python main.py
    Delete data/data file to have interactive disk data
    update data/data file with disk data such as A,B,C,D

Important Directories
----------------------
code  - All source code is placed under this directory
docs - Requirement gathering recods
log - Where actual logs were written
trans - This directory loads transactions in file alphabetial order

Important Files
----------------------
code/main.py - Wrapper script for reading transaction and run evaluation
code/Translogger.py - Consisits of INPUT,READ,WRITE and OUTPUT functionality include evaluate methods for TransLogger class
data/data - This file is read by READ& INPUT operations, in absence of variable it will ask user to provide values.

THINGS TO REMEMBER/Known Issues/Assumptions
------------------
1. As instructed by Ravi teja, Log files are in write mode, instead of append mode.
1.  I have commented out Lines #74 to 79 to qualify for assignment.
    Since the temprory variables are also cross transaction varaibles of MEMORY_OBJECT
    and we are running time of quantum, it will be read variables whose data written via OUTPUT
    and process the same.

    This results into potential bug as First variable will be processed even after OUTPUT.

2.  Correctness principle is applicable for ONDISK Storage not Memory storage.




