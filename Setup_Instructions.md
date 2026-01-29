# Qubits-Capstone-Project
1. Download the most recent version of Python here https://www.python.org/downloads/windows/ 
        - Select the 3.14.2 Windows installer 64 bit (the second option in the list)
        - After opening the installer, check "Add Python to PATH" 
2. Download the Python extension in Visual Code by clicking the 4 box icon on the left
3. Update interpreter if needed
        - - On the top menu bar click view > command pallete 
        - Search and click "Select Interpreter"
        - choose the 3.14 option
3. Verify Python updated correctly
        - Open a terminal by view > terminal
        - type the command python --version
        - If that didn't come up with 3.14, you need to fix some of you path envs on your PC. 
          Let me know (Bailey) and I can help troubleshoot.
3. Create a virtual environment:
        - On the top menu bar click view > command pallete
        - Then search and click create environment 
        - Then select the venv option and the 3.14 path
4. Install dependencies to your virtual environment
        - Open a terminal by view > terminal
        - Make sure your venv is activated. You should see (.venv)
        - Run the command "pip install -r requirements.txt"


For later: to run the django server:
        - Open a terminal by view > terminal
        - Run command "cd qubits_capstone"
        - Run "python manage.py runserver"
        - Ctrl + c will close the server when your done. Or kill the terminal :D

        
