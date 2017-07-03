from django import template
from django.utils.safestring import mark_safe
from datetime import date, datetime
import random
register = template.Library()

@register.filter(name='age')
def calculate_age(value):
    d = map(int, value.split("-"))
    born = datetime(d[0], d[1], d[2])
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

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

@register.filter(name='not_provided')
def not_provided(value):
    if value:
        return value
    return "Not Available"

# Wouldn't actually be used, but all of the provided images 404, so this
# is just a place holder
@register.filter(name='fake_image')
def fake_image(person):
    genders = {
        "Male":   "men",
        "Female": "women",
    }
    if person["patient_photo"]:
        return person["patient_photo"]
    else:
        if not person["gender"]:
            person["gender"] = "Female"
        return "http://api.randomuser.me/portraits/med/" +\
                genders[person["gender"]] +\
                "/" + str(person["id"] % 90) + ".jpg"

@register.filter(name='phonelink', is_safe=True)
def phonelink(value):
    if not value:
        return value
    return mark_safe('<a href="tel:' + value + '">' + value + '</a>')

@register.filter(name='sub',is_safe = True)
def sub(value):
    lst = ['I hope your special day will bring you lots of happiness, love and fun. You deserve them a lot. Enjoy!',
    'Have a wonderful birthday. I wish your every day to be filled with lots of love, laughter, happiness and the warmth of sunshine.',
    'May your coming year surprise you with the happiness of smiles, the feeling of love and so on. I hope you will find plenty of sweet memories to cherish forever. Happy birthday.'
    'On your special day, I wish you good luck. I hope this wonderful day will fill up your heart with joy and blessings. Have a fantastic birthday, celebrate the happiness on every day of your life. Happy Birthday!!']
    cite = '\nFrom,\nDoctor '
    return '\n' + random.choice(lst) + cite
