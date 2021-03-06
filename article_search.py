import datetime
from pynytimes import NYTAPI
class ArticleSearch:

    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate

    def printArticles(self, articles):
        for x in range(len(articles)):
            print("HeadLine: "+articles[x]['headline']['main']
                +", Publication Date: "+articles[x]['pub_date'][0:10]
                +", Web URL: "+articles[x]['web_url'])
            print("\n\n") 

    def search(self):
        nyt = NYTAPI("wbWOIDwmGPWGQALhXbfC3BDK3EMtFBMA")
        startDate=str(self.startDate)+" 00:00:00"
        endDate=str(self.endDate)+" 23:59:59"
        articles = nyt.article_search(
            query = "Covid",
            results = 10,
            dates = {
                #"begin": datetime.datetime(2020, 6, 24),
                #"end": datetime.datetime(2020, 6, 27)
                "begin": datetime.datetime.strptime(startDate,'%Y-%m-%d %H:%M:%S'),
                "end": datetime.datetime.strptime(endDate,'%Y-%m-%d %H:%M:%S')
            },
            options = {
                "sort": "relevance",
                "sources": [
                    "New York Times",
                    "AP",
                    "Reuters",
                    "International Herald Tribune"
                ],

                "type_of_material": [
                    "News"
                ]
            }
        )
        
        return articles
    #results= search('2020-6-25', '2020-6-26')
    #printArticles(results)
