# Tracker application

## Requirements
 - The Beam application is installed on your system;
 - you have an active subscription, which makes you able to receive head and eye tracking data;
 - you run the calibration procedure within the Beam application at least once.

 In addition, if you want to use the Python API, you need:
 - Python 3.6;
 - NumPy;
 - adding <YOUR_BEAM_SDK_INSTALLATION_FOLDER>/API/python to your PYTHONPATH.

 ## Download python 3.6
 Please download python 3.6.8 from the following link: https://www.python.org/downloads/release/python-368/, and add to the python3.6 folder.

 ## Activate virtual environment
 Run the following command:
 ``` sh
python3.6/python.exe -m venv venv_py36
venv_py36\Scripts\activate
 ```
 With the virtual machine activated, install necessary dependencies:
 ``` sh
 pip install -r requirements.txt
 ```
 If you would like to deactive the virtual environment:
 ``` sh
 deactivate
 ```