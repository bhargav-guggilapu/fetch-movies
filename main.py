import calendar
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
import pyrebase
import os

def date_formatter(date):
    if len(date) == 3:
        return f"{date[0]}-{str(months_short.index(date[1]) + 1).zfill(2)}-{date[2]}"
    else:
        return ''
    
def movies_list(movies):
    movies_data = movies[0:]
    
    image_elements = driver.find_elements(By.CSS_SELECTOR, '.movie-img-block a img')
    release_elements = driver.find_elements(By.CSS_SELECTOR, '.Banner')
    
    for i in range(len(image_elements)):
        movies_data.append({
            'name': image_elements[i].get_attribute('title'),
            'img_url': image_elements[i].get_attribute('src'),
            'date': date_formatter(release_elements[i].text.split()[3:])
        })
        
    return movies_data

obj = {}
months = calendar.month_name[1:]
months_short = [month[0:3] for month in months]
firebaseConfig = {
    'apiKey': os.environ["API_KEY"],
    'authDomain': "movies-list-80e05.firebaseapp.com",
    'databaseURL': "https://movies-list-80e05-default-rtdb.firebaseio.com",
    'projectId': "movies-list-80e05",
    'storageBucket': "movies-list-80e05.appspot.com",
    'messagingSenderId': "303428195964",
    'appId': "1:303428195964:web:cd5177c0d3a5caab52dbf9",
    'measurementId': "G-F5PW7CEKTQ"
}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0')

driver = webdriver.Chrome(options = options)
driver.set_page_load_timeout(30)

for month in months:
    month_name = month.lower()
    released = []
    
    if month_name == months[datetime.now().month-1].lower():
        driver.get(f'https://www.filmibeat.com/telugu/movies/{month_name}-2022.html?movieFlag=released')
        released = movies_list(released)
        
    driver.get(f'https://www.filmibeat.com/telugu/movies/{month_name}-2022.html')
    
    print(month + ' ' + 'started')
    
    obj[month_name] = movies_list(released)
    
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
db.child('movies').set(obj)

driver.quit()
