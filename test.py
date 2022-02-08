#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd


#%%


url = 'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20220207&page=1'
req = requests.get(url)
 
if req.ok:
    html = req.text
    soup = BeautifulSoup(html,'html.parser')



#%%


a = soup.find_all('tr')

# %%

item = str(a[35].find('a')).split('"')
item
# %%
url = 'https://movie.naver.com'+item[1]

# %%
title = item[3]
title
#%%
item[1].split('=')

# %%

Df_list = []


for i in range(53):
    if 'None' == str(a[i].find('a')):
        pass
    
    else:
        item = str(a[i].find('a')).split('"')
        id = item[1].split('=')[1]
        title = item[3]
        url = 'https://movie.naver.com'+item[1]
        
        Df_list.append([id,title,url])
        
        


# %%
Df_movie = pd.DataFrame(Df_list,columns=['Id','Title','Url'],index=)
# %%
Df_movie

# %%
