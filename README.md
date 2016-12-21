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

## Sites to Scrape:
**Be careful: some of these sites are seriously dark corners of the web. Hate groups, militia's, white nationalists, etc. Browse with care!**  

#### English
[Breitbart](http://www.breitbart.com/)
[Daily Stormer](http://www.dailystormer.com/)
[Stormfront](https://www.stormfront.org/forum/index.php/)
/pol (4chan)
[/r/TheDonald](https://www.reddit.com/r/thedonald/) (reddit)

#### German 
http://www.blauenarzisse.de
http://info-direkt.eu
https://www.contra-magazin.com
http://www.denken-macht-frei.info
https://derhonigmannsagt.wordpress.com
http://www.gegenargument.at
http://www.freiewelt.net
https://jungefreiheit.de
http://www.metropolico.org
http://www.pi-news.net