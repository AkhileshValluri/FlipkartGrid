from bs4 import BeautifulSoup
import requests

urls = [
    'https://www.refinery29.com/en-us/2021/06/10546896/tiktok-fashion-influencer-subculture-trend',
    'https://www.refinery29.com/en-us/2021/09/10655149/everlane-labor-day-sale',
    'https://www.refinery29.com/en-us/best-weekend-sales-editors-picks',
    'https://www.refinery29.com/en-us/aesthetic-fall-fashion-style',
    'https://www.refinery29.com/en-us/2023/08/11484391/shirt-dresses-styling-outfit-ideas',
    'https://www.refinery29.com/en-us/2023-shoe-trends',
    'https://www.refinery29.com/en-us/fall-shoe-trends-2023',
    'https://www.refinery29.com/en-us/wide-leg-jeans-women',
    'https://www.refinery29.com/en-us/summer-dresses-best-reviews',
    'https://www.refinery29.com/en-us/summer-fashion-trends-2023',
]

all_titles = [] 

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = [title.text for title in soup.find_all('article')]
    all_titles.append(titles)

with open('blog.txt', 'w') as txt_file:
    for title in all_titles:
        for final_title in title:
            temp = final_title.encode('utf-8')
            txt_file.write(str(temp))
            txt_file.write('\n')
