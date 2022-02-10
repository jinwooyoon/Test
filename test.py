#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
import logging



class Crawling():
    def init(self):
        self.start = 50
        self.url = 'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20220207&page={self.start}'
        self.Df_list = []
    
    
    def start(self):
        first_crawling()
        
        
        
    def first_crawling(self):
        
        for i in tqdm(range(1,41)):
            req = requests.get(url)
            
        if req.ok:
            html = req.text
            soup = BeautifulSoup(html,'html.parser')
            a = soup.find_all('tr')

            for i in range(57):
                if 'None' == str(a[i].find('a')):
                    pass
                else:
                    item = str(a[i].find('a')).split('"')
                    id = item[1].split('=')[1]
                    title = item[3]
                    url = 'https://movie.naver.com'+item[1]
                    self.Df_list.append([id,title,url])

        Df_movie = pd.DataFrame(self.Df_list,columns=['Id','Title','Url'])
        
        return Df_movie
    
    def second_crawling(self):
        
        
#크롤링 한 Url만 가지고 오기
        Df_url = Df_movie['Url']

        #관람객 평점

        test_list = []


        for i in tqdm(Df_url[0:50]):
            req = requests.get(i)
            
            
            if req.ok:
                html = req.text
                soup = BeautifulSoup(html,'html.parser')


            #관람객 평점
            
            spectator_grade = soup.select_one('#actualPointPersentBasic > div > span')
            spectator_grade = spectator_grade.text[-6:-1]

            if '평점' in spectator_grade:
                spectator_grade = '평점없음'
                
            else:
                spectator_grade =float(spectator_grade)
            
            
            #네티즌 평점
            
            netizen_grade = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div.score.score_left > div.star_score')
            netizen_grade = float(netizen_grade.text.replace('\n',''))

            #썸네일 사진
            images = soup.select_one('#content > div.article > div.mv_info_area > div.poster > a')
                            
            images=str(images).split('src=')[2].split('"')[1]
            
            # 기자 평점
            reporter_grade = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(2) > div > a > div')

            if reporter_grade is None:
                reporter_grade = '평점없음'
            
            else:
                reporter_grade =float(reporter_grade.text.replace('\n',''))
            

            # 장르
            
            genre = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a').text

            #국가
            country = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(2) > a').text
            
            #런타임
            runtime = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)').text.replace(' ','')
            #개봉일

            release = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4)')
            if release is None:
                release = '개봉일 없음'
            else:
                release = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4)').text[1:13].replace('\n','')
            #감독
            director = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a').text
            #배우
            
            actor = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p').text
            if '\t' in actor:
                actor = '결측값'
            
            # 연령제한
            age = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a:nth-child(1)')
            if age is None:
                age = '전체관람가'
            
            # 줄거리
            summary = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')
            summary = summary.text.replace('\r','').replace('\xa0','').replace('\xa1','')


            # #연령대별 관람추이    

            try:            
                age_search = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.viewing_graph > div > div.bar_graph').text
                age_list = age_search.replace('\n','').split('대')[:5]
                age_10 = age_list[0][:-2]
                age_20 = age_list[1][:-2]
                age_30 = age_list[2][:-2]
                age_40 = age_list[3][:-2]
                age_50 = age_list[4][:-2]
                
            except:
                age_10 = '데이터 없음'
                age_20 = '데이터 없음'
                age_30 = '데이터 없음'
                age_40 = '데이터 없음'
                age_50 = '데이터 없음'

            test_list.append([spectator_grade,netizen_grade,images,reporter_grade,genre,country,runtime,release,director,actor,age,summary,age_10,age_20,age_30,age_40,age_50])

        test_list_df = pd.DataFrame(test_list,columns=['spectator','netizen','thumbnail','reporter','genre','country','rumtime','release','director','actor','age','summary','age_10','age20','age30','age40','age50'])
        
        return test_list_df  
    
    
        
                
    
    
    

#%%
Df_list = []


for i in tqdm(range(1,41)):
    url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20220207&page={i}'
    req = requests.get(url)
    
    if req.ok:
        html = req.text
        soup = BeautifulSoup(html,'html.parser')


    a = soup.find_all('tr')



    for i in range(57):
        if 'None' == str(a[i].find('a')):
            pass
        
        else:
            item = str(a[i].find('a')).split('"')
            id = item[1].split('=')[1]
            title = item[3]
            url = 'https://movie.naver.com'+item[1]
            
            Df_list.append([id,title,url])

    Df_movie = pd.DataFrame(Df_list,columns=['Id','Title','Url'])
    
    
#%%

#크롤링 한 Url만 가지고 오기
Df_url = Df_movie['Url']

#관람객 평점

test_list = []


for i in tqdm(Df_url[0:50]):
    req = requests.get(i)
    
    
    if req.ok:
        html = req.text
        soup = BeautifulSoup(html,'html.parser')


    #관람객 평점
    
    spectator_grade = soup.select_one('#actualPointPersentBasic > div > span')
    spectator_grade = spectator_grade.text[-6:-1]

    if '평점' in spectator_grade:
        spectator_grade = '평점없음'
        
    else:
        spectator_grade =float(spectator_grade)
    
    
    #네티즌 평점
    
    netizen_grade = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div.score.score_left > div.star_score')
    netizen_grade = float(netizen_grade.text.replace('\n',''))

    #썸네일 사진
    images = soup.select_one('#content > div.article > div.mv_info_area > div.poster > a')
                       
    images=str(images).split('src=')[2].split('"')[1]
    
    # 기자 평점
    reporter_grade = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(2) > div > a > div')

    if reporter_grade is None:
        reporter_grade = '평점없음'
    
    else:
        reporter_grade =float(reporter_grade.text.replace('\n',''))
    

    # 장르
    
    genre = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a').text

    #국가
    country = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(2) > a').text
    
    #런타임
    runtime = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)').text.replace(' ','')
    #개봉일

    release = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4)')
    if release is None:
        release = '개봉일 없음'
    else:
        release = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4)').text[1:13].replace('\n','')
    #감독
    director = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a').text
    #배우
    
    actor = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p').text
    if '\t' in actor:
        actor = '결측값'
    
    # 연령제한
    age = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a:nth-child(1)')
    if age is None:
        age = '전체관람가'
    
    # 줄거리
    summary = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')
    summary = summary.text.replace('\r','').replace('\xa0','').replace('\xa1','')


    # #연령대별 관람추이    

    try:            
        age_search = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.viewing_graph > div > div.bar_graph').text
        age_list = age_search.replace('\n','').split('대')[:5]
        age_10 = age_list[0][:-2]
        age_20 = age_list[1][:-2]
        age_30 = age_list[2][:-2]
        age_40 = age_list[3][:-2]
        age_50 = age_list[4][:-2]
        
    except:
        age_10 = '데이터 없음'
        age_20 = '데이터 없음'
        age_30 = '데이터 없음'
        age_40 = '데이터 없음'
        age_50 = '데이터 없음'

    test_list.append([spectator_grade,netizen_grade,images,reporter_grade,genre,country,runtime,release,director,actor,age,summary,age_10,age_20,age_30,age_40,age_50])

test_list_df = pd.DataFrame(test_list,columns=['spectator','netizen','thumbnail','reporter','genre','country','rumtime','release','director','actor','age','summary','age_10','age20','age30','age40','age50'])


#%%
test_list_df['Id'] = Df_movie['Id']


result = pd.merge(Df_movie,test_list_df,on='Id')



result.to_csv('./result.csv',encoding='utf-8',index=False)
