import sys #imports module that can perform system functions
import subprocess #imports module that can run commands on local system

class Menu:
    """
    Menu class handles the display of user interface for the MPMS Application.

    Instance Variables:
        banner (str):   The raw string of the ASCII Art for displaying as banner on all screens of MPMS
    """

    def __init__(self):
        """
        Initialises a Menu instance with the banner.
        """
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

    def clear_screen(self):
        """
        This function clears the terminal screen.
        """
        #Checks for host machine's OS and runs appropriate clear screen command.
        if sys.platform == 'win32':
            subprocess.run('cls', shell=True)
        else:
            subprocess.run('clear', shell=True)
    
    def show_admin_home_page(self):
        """
        Displays the Admin home page on the terminal
        """
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     ADMIN HOME PAGE
                                                       Hi, Admin! What would you like to do today?
            ''')
    
    def show_back_prompt(self):
        """
        Displays the standard prompt to inform the user that they can enter "BACK" as input on this screen.
        """
        print('''Enter \033[34m"BACK"\033[0m to Exit Application\n''')

    def show_error_message(self, type):
        """
        This function displays an error message based on the type provided.

        Args:
            type (str): Type of error to be displayed.
        """
        if type == "login":
            print("\033[91m!! Invalid credentials. Please try again !!\033[0m")
        elif type == "standard":
            print("\033[91m!! Invalid input. Please try again !!\033[0m")


    def show_login_page(self, attempt_number):
        """
        Displays the Login Page and an Error message based on user attempt number.

        Args:
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     LOGIN PAGE
                                                       Please Enter Your Credentials To Login
            ''')
        # Display error message if not first attempt
        if attempt_number > 0:
            self.show_error_message("login")
        self.show_back_prompt()
    
    def show_logout_prompt(self):
        """
        Displays the standard prompt to inform the user that they can enter "LOGOUT" as input on this screen.
        """
        print('''Enter \033[34m"LOGOUT"\033[0m to go back to Login Page\n''')

    def show_patient_home_page(self, attempt_number):
        """
        Displays the  patient home page with user action menu.

        Args:
            attempt_number (int): Represents the number of times the user has failed to input valid details.
        """
        self.clear_screen()
        print(self.banner)
        print('''
                                                                     PATIENT HOME PAGE
                                                           Hi! What would you like to do today?
            ''')
        # Display error message is not first attempt
        if attempt_number > 0:
            self.show_error_message("standard")
        self.show_logout_prompt()
        print('''
1. My Profile
2. Book an Appointment
3. View Upcoming Appointments
4. Previous Appointments

Please enter the Option Number or LOGOUT
            ''')
    
    def  show_profile_page(self, user_obj, is_user_admin):
        """
        Displays the user profile page with user details.

        Args:
            is_user_admin (bool): A flag to represent the user's system role.
        """
        if is_user_admin:
            user_role = "ADMIN"
        else:
            user_role = "PATIENT"
        self.clear_screen()
        print(f'''
                                                                     {user_role} PROFILE PAGE
{user_obj}
            ''')