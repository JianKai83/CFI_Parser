import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

def get_content(hidden_code,real_articleUrl):
    real_headers = {'Referer': 'https://www.104.com.tw/job/' + hidden_code,
                    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
                    }
    real_resArticle = requests.get(real_articleUrl, headers=real_headers)
    all_content = json.loads(real_resArticle.text)
    Job_Content = all_content['data']['jobDetail']['jobDescription']
    Job_Content = Job_Content.replace("\n", "  ")

    return Job_Content

if __name__ == '__main__':
    print('Input the Job Opening you want:')
    job_name = input()

    print('Input total page you want:')
    total_page = int(input())

    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
    ss = requests.session()

    df = pd.DataFrame(columns=['Job_Company', 'Job_Opening', 'Job_Content'])
    df_index = 0

    for i in range(1,(total_page+1)):
        url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=' + job_name + '&page=' + str(i)
        res = ss.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        company = soup.select('div[class="b-block__left"] ul[class="b-list-inline b-clearfix"] li a')
        title = soup.select('div[class="b-block__left"] h2[class="b-tit"] a')

        for j in range(len(company)):
            tmp = []
            Job_Company = company[j].text.split('\n')[0]
            Job_Opening = title[j].text
            hidden_code = title[j]['href'].split('job/')[1].split('?')[0]
            real_articleUrl = 'https://www.104.com.tw/job/ajax/content/' + hidden_code
            Job_Content = get_content(hidden_code,real_articleUrl)

            tmp.extend([Job_Company,Job_Opening,Job_Content])
            df.loc[df_index] = tmp
            df_index += 1

    df.to_csv('./104.csv', index=False, encoding='utf-8-sig')


