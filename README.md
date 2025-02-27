# Flip Radio fans developer community

This is a project developed by flipradio fans. The main function of this project is to crawl content from the website https://fearnation.club/ and generate a PDF. An additional feature is the ability to extend the crawling functionality to ghost blog websites, which, after some configuration, can also generate PDFs for offline reading and research.

I hope you will like this program.

## Quick start

This project is developed using Python, with HTML and CSS used to define the exported styles.

The project is developed using Python 3.13, although theoretically, lower versions of Python should also work.

The related dependencies are as follows:

* beautifulsoup4~=4.13.3
* requests~=2.32.3
* loguru~=0.7.3
* PyYAML~=6.0.2
* PyPDF2~=3.0.1
* reportlab~=4.3.1
* weasyprint~=64.1
* pathlib~=1.0.1
* PyMuPDF~=1.25.3

The program is divided into the following three parts: crawling the pages, cleaning and saving the page information, and converting it into a PDF file for saving. After some basic setup, each part can be used independently.

The core of the program lies in the config.yaml file under the config folder. It defines in detail the crawling paths, filter paths, style rules, saving locations, and other information.

```yaml
main:
  cache_file_path: "tmp"              # Path for temporary cache files ，
  cache_file_name: ".cache.txt"       # Name of the cache file
  resources_path: "resources"         # Path to store additional resources (e.g., images, files)
  html_path: "html"                   # Path for saving HTML content from crawled pages
  home_page_path: "home_page"         # Path for the homepage or main entry point
  out_put_path: "output"              # Path to save the final output (e.g., PDFs)
  grouping_rules: "month"             # Rule to group content (e.g., by month)
```

The cache file is designed to prevent the program from repeatedly crawling content that has already been crawled.

```yaml
spider:
  website_url: ""                      # The starting point for crawling
  base_url: ""                         # The base URL for constructing relative URLs
  crawl_deep: 1                        # The depth of crawling (1 means only the homepage)
  download_retry_number: 3             # The number of retries if the download fails
  need_filter_url:                     # URLs that need to be filtered
    - "need filter url"                # List of URLs to be filtered
```

The spider config defines the crawling rules, preventing the crawler from going beyond the target scope.

```yaml
clean:
  main_info: ""                        # The main content to be crawled from each webpage
  img_info:
    img_select:
      - "main > article > header > figure > img"  # CSS selector for the image element
    img_local_path: "images"            # Local path to store downloaded images
    clean_img_attr:
      - "srcset"                        # Attributes to remove from images
  need_filter_elements:                 # Elements to be filtered out during cleaning
    - "main > article > header > div > span.single-meta-item.single-meta-length"
    - "main > article > div:nth-child(3)"
    - "main > article > div > div.kg-card.kg-audio-card > div.kg-audio-player-container"
    - "main > article > div > figure"
    - "main > article > div.single-content.gh-content.gh-canvas > div.kg-card.kg-audio-card"
  need_filter_ids:                      # Specific IDs to be filtered
    - "透明茶室每日新闻分析节目"
    - "你希望我在透明茶室讨论什么新闻"
  need_filter_mark_info:                # Markers for content to be filtered based on text
    - p:
        - "我们在X帐号每天早上上海时间8点进行新闻分析的直播。直播录音会在世界苦茶Podcast进行播放，也会在YouTube世界苦茶帐号播放。欢迎大家参与和收听。"
        - "欢迎大家把世界苦茶推荐给你信任的朋友。"
        - "欢迎你告诉我，兴许就会成为之后「透明茶室」的话题噢。"
  need_cut_off_mark:                    # Markers to cut off content
    - "hr"                               # Horizontal rule to cut off content after
```

The clean config defines how to remove unwanted elements from a webpage. It outlines four cleaning methods:

1. Element Cleaning: Specific elements are targeted for removal using CSS selectors.
2. ID Cleaning: Certain elements with specific IDs are removed. The IDs are URL-encoded and then used to locate and remove corresponding DOM elements on the page.
3. Content Cleaning: This method cleans the content inside specific elements, such as removing specific text or tags.
4. Truncating Content: This method stops processing and truncates the content after a specific element (e.g., after a certain hr or section).

```yaml
save:
  title_target: "head > title"             # CSS selector for the target title element
  title_source: "body > main > article > header > h1"  # CSS selector for the source title element
  page_module:                             # Different page style modules
    - style_name: "dark"                   # Name of the style (dark theme)
      home_page_path: "home_page.html"     # Path for the home page HTML
      base_template_path: "base_template.html"  # Path for the base template HTML
      home_page_style_path:
        - "styles_home_page_dark.css"     # CSS for the home page dark style
      page_style_path:
        - "styles_dark.css"               # CSS for the dark theme
      number_color: "1, 1, 1"              # Color for numbers (white)
    - style_name: "light"                  # Name of the style (light theme)
      home_page_path: "home_page.html"     # Path for the home page HTML
      base_template_path: "base_template.html"  # Path for the base template HTML
      home_page_style_path:
        - "styles_home_page_light.css"    # CSS for the home page light style
      page_style_path:
        - "styles_page_light.css"         # CSS for the light theme
      number_color: "0, 0, 0"              # Color for numbers (black)
  select_module:                           # The selected style module
    - "light"                               # Light theme selected
  home_page_content_element: "time"         # Element for displaying the time on the home page
```

The save config mainly defines the page styles. Since multiple final results are exported based on the page's style configuration during the saving process, this section also includes custom information that is needed during saving. The content for each PDF's homepage section is designed and configured here.

This configuration allows for flexible and customized output depending on the selected styles and other settings for each saved PDF.

The select_module will specify the export style based on the style_name selected from the page_module.

This means that the chosen style from the page_module configuration will determine how the final output (e.g., PDF) is styled during export.

Thank you for your attention

## Feature

From easy to hard

- [ ] More page templates
- [ ] More grouping rules
- [ ] More general way to crawl data
- [ ] Translate into other languages through large language models.
- [ ] Export crawled data into a variety of customizable formats for use in other programs