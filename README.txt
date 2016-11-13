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
    main.py - main wrapper program
    TransLogger.py which performs logging operations

main.py - Wrapper script for reading transaction and run evaluation
Translogger.py - Consisits of INPUT,READ,WRITE and OUTPUT functionality include evaluate methods for TransLogger class
docs - Requirement gathering recods
log - Where actual logs were written
trans - This directory loads transactions in file alphabetial order

THINGS TO REMEMBER/Known Issues/Assumptions
------------------
I have commented out Lines #74 to 79 to qualify for assignment.
Since the temprory variables also we are keeping global MEMORY_OBJECT
and we are running time of quantum, it will be re read
variables whose data written via OUTPUT and process the same.
This results into potential bug as First variable will be processed even after OUTPUT.

Correctness principle is applicable for ONDISK Storage not Memory storage.




