# django-rest-api-assignment
### FEATURES:

* User account registration
* User account activation
* User login
* User list
* User change password

### INSTALLATION

1. Setup python3, pip, and virtual environment
2. Create a virtual environment `CA-env`. On unix/linux `python -m venv `CA-env`. The name may be change but may not be ignored by git.
3. Activate virtual environment. On unix/linux `source CA-env/bin/activate`
4. Install required python libraries `pip install -r requirements.txt`
5. Define environment variables for email sending `EMAIL_HOST - smtp server` `EMAIL_HOST_USER - smtp account username/email` `EMAIL_HOST_PASSWORD - smtp account password` `EMAIL_HOST_PORT - smtp server port`
6. Perform migration of schema `python manage.py migrate`
7. Run server locally `python manage.py runserver`