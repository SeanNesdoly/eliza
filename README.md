# Eliza Chatbot
>Assignment 1  
>CISC 352: Artificial Intelligence  
>Sean Nesdoly  
>January 29th, 2017  

I implemented the assignment using **Python 2.7.8**.  As such, ensure that python is installed correctly and that the path to the python executable is contained within the system PATH variable.

### Running the Eliza chatbot with input from a file

The text specifying the user input to the Eliza chatbot must be contained within a file named "**human_script.txt**" in the **same directory** that the **eliza.py** file is in. Each phrase in the file must be separated by the new-line character "**\n**".

*To run the code on a unix environment with file input:*

```bash
cd ~/path/to/NesdolyAssn1/
python eliza.py
```

Eliza will read the input phrases from the **human_script.txt** file line-by-line in a sequential order. For every line, Eliza will read, process and transform the string into a response to the user that is written to the standard output stream, along with its associated human input phrase (from file).

When reading from a file, the Eliza chatbot will terminate when one of the following conditions is true:

1. the string "**quit**" is given as a line in the **human_script.txt** file, or,
2. all lines in **human_script.txt** have been parsed

---

### Running the Eliza chatbot in terminal-mode

Alternatively, the Eliza chatbot can be run in a **terminal-mode**. In this mode, user input is accepted from the standard input stream (**stdin**) instead of from a file. 

*To run the code on a unix environment in terminal-mode:*

```bash
cd ~/path/to/NesdolyAssn1/
python eliza.py --terminal
```

Eliza will proceed to greet the user on the standard output stream with, "*Hello. How are you feeling today?*". The program will prompt the user for an input string on a new line. The conversation continues completely within the terminal environment, where user input is read, processed and fed back to the user in a "chatbot-like" style. To terminate the program in **terminal-mode**, simply input the string "**quit**".
