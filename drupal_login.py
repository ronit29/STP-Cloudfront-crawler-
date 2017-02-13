import requests
from bs4 import BeautifulSoup
s = requests.Session()


Uname = 'stp_admin'
password = 'stpadmin'
# URL without http and any leading or trailing slashes
prd_url = 'grizzlies-prd.io-media.com'


main = "/admin/structure/menu/manage/main-menu"
anonymous = "/admin/structure/menu/manage/menu-anonymous-menu"

def login():		 
  URL = "https://" + prd_url + "/user/login"
  params = {"name": Uname, "pass" : password, "form_id" : "user_login"}
  head = {"Referer":URL,'Host': prd_url,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
  signin = s.post(URL, data = params, headers = head)
  print(signin)

def links(menu):
  menu_url = "https://" + prd_url + menu
  sorce = s.get(menu_url)
  sorce_text = sorce.text
  soup = BeautifulSoup(sorce_text, "html.parser")
  tbody = soup.find('tbody')
  main_menu = {}
  for row in tbody.findAll("a", href = True, text = True):
    if row.text != 'edit' and row.text != 'delete' and row['href'] != 'my-calendar' and row['href'] != 'calendar':
      # page_link = row.text + ' = ' + row['href']
      main_menu[row.text] = prd_url + row['href']
  for name,path in main_menu.items():
    if path.find('http') == -1:
     path = "https://" + path
     visit = s.get(path)
     page_content = visit.text
     page_content = BeautifulSoup(page_content, "html.parser")
     article = page_content.find('article')    
     if article:      
       for img in article.findAll("img"):
         if img['src']:      
           src = img['src']
           if src.find('cloudfront') != -1:
             out = "CloudFront path Found in '" + name + "' = " + path
           else:
             out = "No cloudfront path in '" + name + "' = " + path
         else:
           out = "NO image in '" + name + "' = " + path
         print(out)   

login()
links(main)
links(anonymous)
