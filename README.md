# ipl_project

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/heeragokul/ipl_project.git
$ cd ipl_project
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3 env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:

```sh
(env)$ cd project
(env)$ python manage.py migrate
```

After migration download the data from https://drive.google.com/file/d/1ie-WwMWr-K8B9nBUE7ZYjHLbl5IFIcwU/view. 
and export the data into db tables and specify database details in settings.py file.
After that 

```sh
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.

