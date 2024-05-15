import requests
from bs4 import BeautifulSoup
import mysql.connector

data = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yy112233",
    database="mal"
)
cursor = data.cursor()

# URL of the website you want to scrape


x=0
for i in range(84):
    url = f'https://myanimelist.net/topanime.php?limit={x}'
    x+=50
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with class 'ranking-list'
    ranking_list_items = soup.find_all(class_='ranking-list')

    # Iterate over each item in the ranking list
    for item in ranking_list_items:
        # Find the title with class 'title' and 'va-t' and 'word-break'
        title = item.find(class_='di-ib clearfix').text.strip()

        # Find the score with class 'score' and 'ac' and 'fs14'
        score = item.find(class_='js-top-ranking-score-col di-ib al').text.strip()
        infos = list(item.find(class_="information di-ib mt4").text.strip())
        li=[]

        if infos[0]== "T" and infos[1] == "V":
            li.append('tv')
        elif infos[0]== "O" and infos[1] == "V":
            li.append('ova')
        else :
            li.append('movie')
        typ="".join(li)
        sql = "INSERT INTO note (title, score, type) VALUES (%s, %s, %s)"
        values = (title,score,typ)
        cursor.execute(sql, values)


data.commit()
# Close the cursor and database connection
cursor.close()
data.close()