# OCN-XMLChecker
A Django webapp made to check OCN map XMLs for errors.

#DJANGO 1.8.3 IS REQUIRED TO INSTALL AND RUN THIS APP.

<h3>Step one: Installing virtualenv</h3>

This web app is made to run on a Linux /OS X operating system. If you are on Debian Linux or a Debian based system,
run `sudo apt-get install python-virtualenv`. If you are on RedHat Linux, run, `yum install python-virtualenv`.
If on OS X, run `pip install virtualenv`. 

<h3>Step two: Setting up your virtualenv</h3>

If you now that you have installed virtualenv, you have to create a virtualenv. Create it in a easy-to-access location, 
such as your Desktop. Now, run `virtualenv ~/Desktop/env` This will create a virtualenv named `env`. Congratulations,
you now have your virtualenv set up! Now lets go over how to install Django within your virtualenv.

<h3>Step three: Installing Django in your virtualenv</h3>

Now that you have your virtualenv set up, you're going to want to activate it. Run the command 
`source ~/Desktop/env/bin/activate`. You should see the words `(env)` appear before your prompt. Your virtualenv is now 
activated. We must install django in the virtualenv now. Install django by running `pip install django`. After it downloads
and unpacks, you will have django installed inside of your virtualenv.

<h3>Step four: Installing the XML-Checker</h3>

Enter the directory of your virtualenv by running the command `cd ~/Desktop/env`. Now create a folder called mysite. 
(This folder can be named anything you want, it's just a container folder for the project.) Clone this git repository
into the folder you just created by entering the directory and running 
`git clone http://github.com/TheMetaphorer/OCN-XMLChecker .` The `.` at the end of the command is important, because
when you clone the git repository, you don't want to have the project folder. After cloning the contents of this
repository, enter the directory named `mysite` and click on `settings.py`, and scroll down to the area with a dictionary
defined as `DATABASES`. For databases you can use sqlite or postgresql If you're using `sqlite`, continue reading. 
If you're using postgresql, then follow the link, which is a tutorial on how to use postgresql with django, and
scroll down to step seven.
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn

Since you are using sqlite, replace `postgresql_psycopg2` with `sqlite3`. Delete `USER`, `PASSWORD`, `HOST`, and `PORT`.
Replace set `NAME` equal to `os.path.join(BASE_DIR, 'db.sqlite3')` Now `cd` to the directory that you created the 
project in, And run the command `python manage.py createsuperuser` It'll ask you to create a name for your superuser
in the database, it'll ask for an email, a password, then a password confirmation. Now, after this, run 
`python manage.py makemigrations`. Then, after that, you'll run `python manage.py migrate`. 

<h3>Step five: Running and updating the app</h3>

Congratulations, you've finished installing it! If you want to run the server, run the command 
`python manage.py runserver`. By default, `runserver` sets the port to `localhost:8000`. You can specify this yourself.
If you want to be able to debug or catch errors, set `DEBUG` to settings.py to `True`. (It's set to this by default)
Otherwise, set it to `False`. If you need to update this, periodically return to this directory and run the command
`git pull master`, and it'll update with the latest code if I've made any pushes to the repo since you last cloned or 
pulled.

<h3>Appendix</h3>

This code is completely open-source and free to edit. If you have any suggestions to make or catch a bug, please open
an issue!


Contributors:

Dorian Dore - _Dorian_D_


