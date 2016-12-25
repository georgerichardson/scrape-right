# Scrape-Right: scraping pages of the far and fringe right  

## Requirements:  
- Python 3.3+  
- [Scrapy 1.2.2](https://doc.scrapy.org/en/1.2/index.html)

## Purpose:  
We are a sub project under wider data for [democracy](https://medium.com/data-for-democracy/origin-story-b740f14ca6ed#.ixjfjveq) umbrella. Scrape-right is a work in progress tool which will be used to crawl online communities of the alt-right/fringe-right. If you have ideas for analysis you would like to do, let us know!  

## How can you help?   
* Provide feedback on any of our open issues or open new ones.
* Browse our `help wanted` [issues](https://github.com/Data4Democracy/scrape-right/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22). See if there is anything that interests you.
* Volunteer to build a spider.
  * Do not worry if you do not have previous experience, there are lots of helpful people in our group chat. Checkout `scrape_right/spiders/example.py` to get a feel for how a basic spider works.
  * If you already know what site you'd like to work on. Open a pull request stating what you would like to work on. This is a good way solicit for feedback and prevent multiple people from working on the same thing. 
  * Ask us in our group chat or direct message any of the contributors if you would prefer to ask your questions in private.
* Experience with scrapy and willing to answer questions? Come hang out in slack  
* Help us standardize and store our data.  
* Let us know how you'd like to use this data for your own analysis. Suggestions for new sources/metadata you'd like to see to facilitate your analysis.  
* We welcome all input or ideas you may have.  

## Basic Structure:  
* See scrapy architecture [overview](https://doc.scrapy.org/en/1.2/topics/architecture.html)
* Each site will have a custom spider `/spiders/<sitename>_spider.py` which contains rules specific to collecting links and parsing information contained in that site.
* All spiders should return an Article [item](https://doc.scrapy.org/en/1.2/topics/items.html) (see `items.py`) which will be be validated and saved by shared logic in `pipline.py`  

## Data Spec (Work in progress):  

#### Required:  
`language`: language of the text  
`url`: the url of an article  
`text_blob`: body of article/text  
`source`: source website  

#### Optional/If exists:  
`authors`: the authors of a particular article  
`pub_datetime`: date and time an article was published  
`modified_datetime`: date and time article was last modified  
`title`: the headline of a page/article/news item  
`lead`: opening paragraph, initial bolded text or summary  


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

## Sites to Scrape:  
**Be careful: some of these sites are seriously dark corners of the web. Hate groups, militia's, white nationalists, etc. Browse with care!**  

### Done  
Coming soon!  

### In Progress  
[Breitbart](http://www.breitbart.com/) - @bstarling in slack  
[Compact-Online](http://www.compact-online.de) @lukas in slack  
[Daily Stormer](http://www.dailystormer.com/) @matt.kleinert in slack  
[American Renaissance](https://www.amren.com/) @alarcj in slack commit test

### Looking for help  

#### English  

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


## Getting Started:  
* Clone locally with command `https://github.com/Data4Democracy/scrape-right.git`  
* Conda package manager is easiest way to ensure all dependencies are correctly installed. If you have [anaconda](https://www.continuum.io/downloads) installed on your machine run `conda env create -f environment.yml` from the main directory. Alternatively you can install dependencies via pip (see `requirements.txt`).
* Activate your environment. Ex: `source activate scrape-right` (mac/linux) or `activate scrape-right` (windows).  
* To test everything is working, navigate down to the scrapy project directory `cd scrape_right` and run `scrapy crawl example -o test.json` this will activate the example spider and should save a json file containing ten quotes inside the `scrape_right` directory.  
* Questions or issues you can join the team in slack and/or ping @bstarling.  
