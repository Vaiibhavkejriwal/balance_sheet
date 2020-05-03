Preassumption:
---------------------------------------------------------------
- I have used print statement that can be replaced with logging to handle failure
- UI is just for demonstration pusrpose and even css is not writeen for better look feel
- Assume file can be uploaded to bucket like s3 and url can be stored in the database
- Here local file is used for uploading 


Pre-Requirement
---------------------------------------------------------------
- Python3
- Django 2.2
- MySQL database
- git
- virtualenv
- pip

Project Setup
-----------------------------------------------------------------
- Clone the project from github using: git clone repo_url
- Create the virtual env using: virtualenv -p python3 env
- Install the package requirement using: pip install -r requirement.txt
- Create database and update the database configuration in the settings.py
- Migrate the changes into database using python manage.py migrate
- Run the loca server using python manage.py runserver
- Go to url http://127.0.0.1:8000/file/balsheet


