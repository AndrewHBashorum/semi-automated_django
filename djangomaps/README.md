
# {{ project_name|title }}

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/USERNAME/semi-automated_django.git
    $ cd semi-automated_django
    
Activate the virtualenv for your project:

    $  python3 -m venv env
    $  source env/bin/activate
    
Install project dependencies:

    $ python -m pip install -r requirements.txt
    
    
Go into project directory:

    $ cd djmaps
    
   
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
