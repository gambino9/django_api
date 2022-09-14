### API project for a technical test

A small API project for a technical test, using Django and Django Rest Framework.   
This is my very first API and first Django project, hence maybe not the best way to implement things with Django.

### Installation

Consider using a virtual environment before cloning the repo : 
```
python -m venv .venv
source .venv/bin/activate
```

`git clone <repo_link>`

Do not forget to install the appropriate packages to run the project,
otherwise it won't work :  

`pip install -r requirements.txt`

### Usage
Go to the `manage.py` level directory and run the following command : 

`python manage.py runserver`

Go to your browser and type your request directly in the URL like this : 
`http://127.0.0.1:8000/?q=<type+your+request+here>`

#### Example : 

`http://127.0.0.1:8000/?q=96+boulevard+bessieres+paris`

The request will result in printing the network coverage of the specified location on the page : 
``` 
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "Orange": {
        "2G": false,
        "3G": true,
        "4G": false
    },
    "Bouygues": {
        "2G": true,
        "3G": true,
        "4G": true
    }
}
```

### Code explanation
The CSV file used to get the network coverage measure is located in the [resources file](resources)

The Django Rest Framework API comes into a single View class in the [apis/views.py file](apis/views.py) 

The functions used to find the nearest points in the CSV are located [here](apis/lambert.py) in the `apis/lambert.py` file.

In the `apis/urls.py` [file](apis/urls.py) I defined that an empty URL calls the View containing the API.

In the `django_project/settings.py` [file](django_project/settings.py), I added the API I created and also
Django Rest Framework as 3rd party package.

Finally, I added the path of the API urls in the `django_project/urls.py` [file](django_project/urls.py).


### Resources :
Scipy documentation for KD tree implementation :
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html

### Possible ways to improve the project :

- Load CSV only once, when the server is run
- Better error management
- A more complex API