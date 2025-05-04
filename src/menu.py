import sys, subprocess

class Menu:
    def __init__(self):

        # Banner created using https://patorjk.com/software/taag/
        self.banner = r'''
=====================================================================================================================================================================
 __  __                       _     _____      _   _            _   __  __                                                   _    _____           _                 
|  \/  |                     | |   |  __ \    | | (_)          | | |  \/  |                                                 | |  / ____|         | |                
| \  / | ___  _ __   __ _ ___| |__ | |__) |_ _| |_ _  ___ _ __ | |_| \  / | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_| (___  _   _ ___| |_ ___ _ __ ___  
| |\/| |/ _ \| '_ \ / _` / __| '_ \|  ___/ _` | __| |/ _ \ '_ \| __| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|\___ \| | | / __| __/ _ \ '_ ` _ \ 
| |  | | (_) | | | | (_| \__ \ | | | |  | (_| | |_| |  __/ | | | |_| |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_ ____) | |_| \__ \ ||  __/ | | | | |
|_|  |_|\___/|_| |_|\__,_|___/_| |_|_|   \__,_|\__|_|\___|_| |_|\__|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|_____/ \__, |___/\__\___|_| |_| |_|
                                                                                              __/ |                                      __/ |                      
                                                                                             |___/                                      |___/                       
====================================================================================================================================================================='''
        self.banner2 = '''
===================================
 MONASH PATIENT MANAGEMENT SYSTEM
===================================
''' 

    def clear_screen(self):
        """This function clears the terminal screen"""
        #Checks for host machine's OS and runs appropriate clear screen command.
        if sys.platform == 'win32':
            subprocess.run('cls', shell=True)
        else:
            subprocess.run('clear', shell=True)
    
    def show_admin_home_page(self):
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     ADMIN HOME PAGE
                                                       Hi, Admin! What would you like to do today?
              ''')

    def show_login_page(self, attempt_number):
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     LOGIN PAGE
                                                       Please Enter Your Credentials To Login
              ''')
        if attempt_number > 0:
            print("\033[91m!! Invalid credentials. Please try again !!\033[0m")
        print('''Enter \033[34m"BACK"\033[0m to go to Exit Application\n''')

    def show_patient_home_page(self):
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     PATIENT HOME PAGE
                                                           Hi! What would you like to do today?
              ''')