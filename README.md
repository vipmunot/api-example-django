# drchrono Hackathon

### Requirements
- [pip](https://pip.pypa.io/en/stable/)
- [python virtual env](https://packaging.python.org/installing/#creating-and-using-virtual-environments)
- client_id  = Please update this field with your drchrono client_id
- client_secret = Please update this field with your drchrono client_secret
- EMAIL_HOST_USER = Please update this field with your email id
- EMAIL_HOST_PASSWORD = Please update this field with your email password
### Setup
``` bash
$ git clone https://github.com/vipmunot/drchrono.git
$ cd drchrono/
$ virtualenv myenv
$ source myenv/bin/activate
$ pip install -r requirements.txt
$ sh code.sh
```

### Landing Page
<img   src="readme image/landing.PNG">

### Home Page
- Filtering Patients data using following code
'''
@register.filter(name='todaybirthay')
def today_birthday(pdata):
    plist = []
    for person in pdata:
        if person["date_of_birth"] is None:
            return False
        now = datetime.now()
        toks = person["date_of_birth"].split("-")
        if int(toks[1]) == now.month and int(toks[2]) == now.day:
            plist.append(person)
    return plist
'''    
<img   src="readme image/home.PNG">
