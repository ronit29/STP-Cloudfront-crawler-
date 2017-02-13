import requests
from bs4 import BeautifulSoup
s = requests.Session()


# URL without http and any leading or trailing slashes
prd_url = 'www.redwingsseasontickets.com'
username = 'redwings_admin'
password = "redwingsadmin"





def login():		 
  URL = "https://" + prd_url + "/user/login"
  params = {"name": username, "pass" : password, "form_id" : "user_login"}
  head = {"Referer":URL,'Host': prd_url,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
  signin = s.post(URL, data = params, headers = head)
  print(signin.text)  

def links(menu):
  menu_url = "https://" + prd_url + menu
  sorce = s.get(menu_url)
  sorce_text = sorce.text
  soup = BeautifulSoup(sorce_text, "html.parser")
  tbody = soup.find('tbody')
  main_menu = {}
  for row in tbody.findAll("a", href = True, text = True):
    if row.text != 'edit' and row.text != 'delete' and row.text != 'Archive' and row.text != 'Bullpen' and row.text != 'Stand-Alone' and row['href'] != 'my-calendar' and row['href'] != 'calendar':
      main_menu[row.text] = prd_url + row['href']
  for name,path in main_menu.items():
    if path.find('http') == -1:
     path = "https://" + path
     visit = s.get(path)
     page_content = visit.text
     page_content = BeautifulSoup(page_content, "html.parser")
     article = page_content.findAll('article')    
     if article:  
       tab = 0 
       for tabs in article:   
         for img in tabs.findAll("img"):
           if img['src']:      
             src = img['src']
             if src.find('cloudfront') != -1:
               out = "FOUND CloudFront path in '" + name + "[" + str(tab) + "]" + "' = " + path
             else:
               out = "NO CloudFront Path in '" + name + "[" + str(tab) + "]" + "' = " + path
           else:
             out = "NO Image in '" + name + "' = " + path
           print(out)
         tab += 1    


login()

main = "/admin/structure/menu/manage/main-menu"
anonymous = "/admin/structure/menu/manage/menu-anonymous-menu"
links(main)
links(anonymous)
