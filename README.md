# Scrape-Right: scraping pages of the far and fringe right

## Requirements:
- Python 3.3+
- Scrapy 1.2.2

## Data Spec:

`title`: the headline of a page/article/news item  
`authors`: the authors of a particular article  
`text`: the text of an article  
`url`: the url of an article  
`pub_datetime`: date and time an article was published  
`language`: the language an article was written in  
`category`: the category an article/domain falls under  

For categories, we're considering:
- far-right (DailyStormer)  
- conspiracy website (info-wars)  