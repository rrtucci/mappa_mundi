"""

References:
https://github.com/j2kun/imsdb_download_all_scripts
https://github.com/AdeboyeML/Film_Script_Analysis
https://www.datacamp.com/tutorial/scraping-reddit-python-scrapy

In Chrome and most web browsers, pressing Ctrl+U opens the current page's
source code in a new browser tab.

3 depths, d0, d1, d2

d0_url
https://imsdb.com/all-scripts.html

d1_url (depends on movie)
https://imsdb.com/Movie%20Scripts/10%20Things%20I%20Hate%20About%20You%20Script.html

d2_url (depends on movie)
https://imsdb.com/scripts/10-Things-I-Hate-About-You.html

find_all() takes you
d0_html, d0_soup->d1_url
d1_html, d1_soup->d2_url
"""
from bs4 import BeautifulSoup
import requests
from slugify import slugify # python-slugify
from my_globals import *

def get_d1_urls_and_titles():
    d1_urls = []
    titles = []
    d0_url = BASE_URL+"/all-scripts.html"
    d0_html = requests.get(d0_url).text
    d0_soup = BeautifulSoup(d0_html, "html.parser")
    for p_tag in d0_soup.find_all('p'):
        d1_url = p_tag.a['href']
        cond1 = "/Movie Scripts/" in d1_url
        cond2 = ".html" in d1_url
        if cond1 and cond2:
            title = d1_url.replace("/Movie Scripts/", "").\
                replace(" Script.html", "").\
                replace(".html", "")
            d1_urls.append(BASE_URL + d1_url)
            titles.append(title)
    return d1_urls, titles


def clean_m_script(text):
    return

def get_one_m_script(d1_url, stub_only=False):
    missing = False
    tail = d1_url.split('/')[-1].replace(".html", "")
    if stub_only:
        m_script = "coming soon to a theater near you"
    else:
        # print("nabf", d1_url)
        d1_html = requests.get(d1_url).text
        d1_soup = BeautifulSoup(d1_html, "html.parser")
        p_tags = d1_soup.find_all('p', align="center")
        if not p_tags:
            print('**************** Missing: %s' % tail)
            missing = True
            return "coming soon to a theater near you", missing
        assert len(p_tags) == 1
        d2_url = p_tags[0].a['href']
        d2_url = BASE_URL + d2_url
        # print("nnfx", d2_url)
        d2_html = requests.get(d2_url).text
        d2_soup = BeautifulSoup(d2_html, "html.parser")
        # tried this. Doesn't always work
        # pre_tags = d2_soup.find_all('pre')
        pre_tags = d2_soup.find_all('td', {'class': "scrtext"})
        if not pre_tags:
            print('**************** Missing: %s' % tail)
            missing = True
            return "coming soon to a theater near you", missing
        m_script = pre_tags[0].get_text()
        # m_script = clean_m_script(m_script)
    return m_script, missing

def get_batch_of_m_scripts(d1_urls, titles,
        first=1, last=5000, stub_only=False):
    d1_urls, titles = get_d1_urls_and_titles()
    num_titles = len(titles)
    missing_m_scripts = []
    assert first <= last
    if last > num_titles:
        last = num_titles
    if first < 1:
        first = 1
    for i in range(first-1, last):
        d1_url = d1_urls[i]
        dashed_title = slugify(titles[i])
        print('%i. fetching %s' % (i+1, dashed_title))
        m_script, missing = get_one_m_script(d1_url, stub_only=stub_only)
        outpath = M_SCRIPTS_DIR + '/' + dashed_title + '.txt'
        if missing:
            missing_m_scripts.append(dashed_title + '.txt')
        else:
            written = False
            len_script = len(m_script)
            print("m_script num of characters=", len_script)
            if len_script > 500:
                with open(outpath, "w", newline="\n") as f:
                    f.write(m_script)
                    written = True
            if not written:
                # m-scripts with less than 500 char are just stubs
                print("------------------ Found just a stub: ", dashed_title)
                missing_m_scripts.append(dashed_title + '.txt')
    print("missing m_scripts:")
    print(missing_m_scripts)
    print("number of missing m_scripts=", len(missing_m_scripts))

if __name__ == "__main__":

    def main1():
        urls, titles = get_d1_urls_and_titles()
        print(urls)
        print(titles)
        assert len(urls)==len(titles)
        print("number of films=", len(urls)) # 1211
        # 75 missing
        # 1211-75=1136 expected 238 MB

    def main2():
        d1_urls, titles = get_d1_urls_and_titles()
        get_batch_of_m_scripts(d1_urls, titles,
            first=1, last=100, stub_only=False)
    #main1()
    main2()