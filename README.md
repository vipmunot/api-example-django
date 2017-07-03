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
- Filtering Patients data to display today's birthdays using following code
```
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
```
- Displaying Upcoming  birthdays latest first
- Patients information displayed
  - Patient photo
  - Patient age
  - Patient home and cell numbers
  - Patient email address
<img   src="readme image/home.PNG">

### Wish Page
- Patient's email address, subject and birthday message is pre-filled. In case, if you want to add things you can add them!
- Birthday message is populated randomly using following code (You can add more messages)
```
@register.filter(name='sub',is_safe = True)
def sub(value):
    lst = ['I hope your special day will bring you lots of happiness, love and fun. You deserve them a lot. Enjoy!',
    'Have a wonderful birthday. I wish your every day to be filled with lots of love, laughter, happiness and the warmth of sunshine.',
    'May your coming year surprise you with the happiness of smiles, the feeling of love and so on. I hope you will find plenty of sweet memories to cherish forever. Happy birthday.'
    'On your special day, I wish you good luck. I hope this wonderful day will fill up your heart with joy and blessings. Have a fantastic birthday, celebrate the happiness on every day of your life. Happy Birthday!!']
    cite = '\nFrom,\nDoctor '
    return '\n' + random.choice(lst) + cite
```
<img   src="readme image/wish.PNG">

### Email Confirmation
- Email is recieved as following
<img   src="readme image/email.PNG">
