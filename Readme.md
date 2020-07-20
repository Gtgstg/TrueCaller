#TRUECALLER

Instructions for running the code
## Install dependencies
```
pip install requirements.txt
```

## Runserver
```
python manage.py runserver
```
## Test the API

###Signup
```
Route: http://localhost:8000/signup/
Type: POST
Data: 

    {
        "username":"Abhijeet",
        "email":"kingofjeet@gmail.com",
        "password":"Iwilldoit",
        "phone":"7011282532"
    }
```
###Login
```
Route: http://localhost:8000/login/
Type: POST
Data: 

    {
        "username":"Abhijeet",
        "password":"Iwilldoit"
    }
```
### AUTHANTICATION
A AUTHTOKEN is provided after signup and login.
```
Route: http://localhost:8000/admin/
signIn using admin credentials.
Go to Token and copy the genrated token
Then in Request Header put
key: Authentication
value: Token (Token string) without bracket
```

### To mark a contact as SPAM
```
Route: http://localhost:8000/spam/
Type: POST
Random Data:
    {
        "phone": "1234567890"
    }
Registed Data:{
        "phone":"7011282532"
    }
```

### To view all the contacts
```
Public Route: http://localhost:8000/contact/
Type: GET
```

### To search by name
```
Route: http://localhost:8000/searchbyname
Type: GET
Full Data:{
    "name":"Abhijeet"
    }
Random Data:{
    "name":"Abhi"
    }
```

### To search by phone
```
Route: http://localhost:8000/searchbyphone/
Type: GET
Data:{
    "phone":"7011282532"
    }
```
