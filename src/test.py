import time, sys, subprocess
"""This is a testing file for the FIT5136 Applied3 Group6 repository"""

def clear_screen():
    """This function clears the terminal screen"""
    #Code from the internet. Not sure if we can use it or not.
    #Checks for host machine's OS and runs appropriate clear screen command.
    if sys.platform == 'win32':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)

def main():
    """The main function of the program"""
    print("Hello World")
    time.sleep(2)
    clear_screen()

if __name__ == '__main__':
    main()
    #srihari's comment
    #aparna's comment