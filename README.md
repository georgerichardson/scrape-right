# Scrape-Right: scraping pages of the far and fringe right  

## Requirements:  
- Python 3.3+  
- [Scrapy 1.2.2](https://doc.scrapy.org/en/1.2/index.html)

## Purpose:
We are a sub project under wider data for [democracy] (https://medium.com/data-for-democracy/origin-story-b740f14ca6ed#.ixjfjveq
umbrella. Scrape-right is a work in progressed which will be used to crawl online communities and news sources of the alt-right/fringe-right. If you have any ideas for analysis you would like to do, let us know!

## Basic Structure:
* See scrapy architecture [overview](https://doc.scrapy.org/en/1.2/topics/architecture.html)
* Each site will have a custom spider `/spiders/<sitename>_spider.py` which contains rules specific to collecting links and parsing information contained in that site.
* All spiders should return an Article [item](https://doc.scrapy.org/en/1.2/topics/items.html) (see `items.py`) which will be be validated and saved by shared logic in `pipline.py` (Pipeline implementation TBD)
  * If you have additional metadata consider creating new item class and inheriting from Article as shown [here](https://doc.scrapy.org/en/1.2/topics/items.html#extending-items)

## Data Spec (Work in progress):  

`title`: the headline of a page/article/news item  
`authors`: the authors of a particular article  
`text`: the text of an article  
`url`: the url of an article  
`pub_datetime`: date and time an article was published
`modified_datetime`: date and time article was last modified
`language`: the language an article was written in  
`category`: the category an article/domain falls under  

For categories, we're considering:  
- far-right (DailyStormer)  
- conspiracy website (info-wars)  

## How can you help?

* Experience with scrapy or general ideas about direction of project. Join us in slack!
* Input or additions to our site [list](#Sites to Scrape)
* Volunteer to build a spider - check in slack or via PR first to prevent duplicate work.
* Help design and build our pipeline
* Let us know how you'd like to use this data for your own analysis.  Suggestions for new sources/metadata you'd like to see to facilitate your analysis.
* We welcome any and all input or ideas you may have.

## Sites to Scrape:  
**Be careful: some of these sites are seriously dark corners of the web. Hate groups, militia's, white nationalists, etc. Browse with care!**  

#### English  
[Breitbart](http://www.breitbart.com/) (In progress)
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
