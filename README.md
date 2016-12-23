# Scrape-Right: scraping pages of the far and fringe right  

## Requirements:  
- Python 3.3+  
- [Scrapy 1.2.2](https://doc.scrapy.org/en/1.2/index.html)

## Purpose:  
We are a sub project under wider data for [democracy](https://medium.com/data-for-democracy/origin-story-b740f14ca6ed#.ixjfjveq) umbrella. Scrape-right is a work in progressed which will be used to crawl online communities and news sources of the alt-right/fringe-right. If you have ideas for analysis you would like to do, let us know!

## Basic Structure:  
* See scrapy architecture [overview](https://doc.scrapy.org/en/1.2/topics/architecture.html)
* Each site will have a custom spider `/spiders/<sitename>_spider.py` which contains rules specific to collecting links and parsing information contained in that site.
* All spiders should return an Article [item](https://doc.scrapy.org/en/1.2/topics/items.html) (see `items.py`) which will be be validated and saved by shared logic in `pipline.py`
  * If you have additional metadata consider creating new item class and inheriting from Article as shown [here](https://doc.scrapy.org/en/1.2/topics/items.html#extending-items)

## Data Spec (Work in progress):  
`language`: language of the text
`url`: the url of an article
`authors`: the authors of a particular article  
`pub_datetime`: date and time an article was published  
`modified_datetime`: date and time article was last modified  
`title`: the headline of a page/article/news item  
`lead`: opening paragraph, initial bolded text or summary  
`text_blob`: body of article/text  
`source`: source website  
`category`: the category an article/domain falls under  

For categories, we're considering:  
- far-right (DailyStormer)  
- conspiracy website (info-wars)  

## Pipeline

### What is it?
A collection of objects containing cleaning, validation and persistence logic. Each one should be named `*Pipeline`, i.e. `CleanTextPipeline`.

### How do I create one?
  1. Create a new class with the proper naming convention in `scrape_right/scrape_right/pipelines.py`.
  2. Implement a public method named `process_item` which receives both an `item` and `spider`. If the `item` passes whatever logic is present in this method, `return item`. If not, `DropItem`, using Scrapy's custom exception. The following is an example taken from the Scrapy [documentation](https://doc.scrapy.org/topics/item-pipeline.html):
```python
from scrapy.exceptions import DropItem

class PricePipeline:

    vat_factor = 1.15

    def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)
  ```
  3. Add your pipeline object to `ITEM_PIPELINES` in `scrape_right/scrape_right/settings.py`. The key should be the relative import path to your object, i.e. `scrape_right.pipelines.CleanTextPipeline`. The value should be an integer specifying the order that the pipeline should be run. (Pipeline A and Pipeline B with values 1 and 2 respectively implies: every item will first pass through Pipeline A then Pipeline B.)

## How can you help?  
* Experience with scrapy or general ideas about direction of project? Join us in slack!
* Input or additions to our site list.
* Volunteer to build a spider - check in slack or via PR first to prevent duplicate work.
* Help design and build our pipeline
* Let us know how you'd like to use this data for your own analysis. Suggestions for new sources/metadata you'd like to see to facilitate your analysis.
* We welcome any and all input or ideas you may have.

## Sites to Scrape:  
**Be careful: some of these sites are seriously dark corners of the web. Hate groups, militia's, white nationalists, etc. Browse with care!**  

#### English  
[Breitbart](http://www.breitbart.com/) (In progress)  
[Daily Stormer](http://www.dailystormer.com/)  
[Stormfront](https://www.stormfront.org/forum/index.php/)  
/pol (4chan)  
[/r/TheDonald](https://www.reddit.com/r/thedonald/) (reddit)  
[American Renaissance](https://www.amren.com/)

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


## Getting Started:  
* Clone locally with command `https://github.com/Data4Democracy/scrape-right.git`  
* Conda package manager is easiest way to ensure all dependencies are correctly installed. If you have [anaconda](https://www.continuum.io/downloads) installed on your machine run `conda env create -f environment.yml` from the main directory. Alternatively you can install dependencies via pip (see `requirements.txt`).
* Activate your environment. Ex: `source activate scrape-right` (mac/linux) or `activate scrape-right` (windows).  
* To test everything is working, navigate down to the scrapy project directory `cd scrape_right` and run `scrapy crawl breitbart -o test.json` this will activate the breitbart spider and save the output to a json file in your active directory.  
* Questions or issues you can join the team in slack and/or ping @bstarling.  
