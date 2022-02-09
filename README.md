# Latex Exam Builder

The Latex Exam Builder is a tool that:
- Manages multiple databases of questions written in latex with support to search by keywords or by text.
- Builds a pdf from the selected questions from one or more databases with support to question modifications on the fly.

This tool is aimed to help teachers to manage their question banks written in latex format and
to create pdfs of exams and other similar documents using those questions.

## Dependencies

Python 3.10 or above and pip must be installed, so the other dependencies (see requirements.txt) can also be installed.
Also, the pdflatex tex engine to build the pdfs and a pdf reader must be present.

This program should run just fine in Windows, Linux or macOS, although it is tested only in Windows. 

## Installing, running and configuring

Install all library dependencies by running ```$ pip install -r requirements.txt```.

Run the program by executing python with the file ```exam_builder.py``` by running ```$ python3 exam_builder.py``` or a similar command.

As soon as possible, the path to a pdf reader should be provided as well as a directory to store and scan the profiles.
Both can be setted in the settings of the program.