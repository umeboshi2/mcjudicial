import os
import datetime

from bs4 import BeautifulSoup
import requests

base_url = "http://judicial.mc.edu"
search_url = os.path.join(base_url, "researchresults.php")


def check_year(year):
    if type(year) is not int:
        msg = "Bad year type: {}=>{}".format(year, type(year))
        raise RuntimeError(msg)
    if year < 1971 or year > 2019:
        msg = "Year out of range: {}".format(year)
        raise RuntimeError(msg)
    return year


# court is either "sct", "coa", or "trial"
def year_search_data(year, court='sct'):
    year = check_year(year)
    data = dict()
    keyprefix = "date{}".format(court)
    # first date
    for part in "MD":
        key = "{}1{}".format(keyprefix, part)
        data[key] = 1
    key = "{}1Y".format(keyprefix)
    data[key] = year
    # second date
    for part in "MD":
        key = "{}2{}".format(keyprefix, part)
        data[key] = 1
    key = "{}2Y".format(keyprefix)
    data[key] = year + 1
    return data


def parse_search_summary(summary_table):
    num_results_list = summary_table.select('h2')
    if len(num_results_list) > 1:
        msg = "Parsing error {}".format(summary_table)
        raise RuntimeError(msg)
    num_results = num_results_list.pop()
    num_results = num_results.text.split()[0]
    return int(num_results)


def parse_date_cell(cell):
    text = cell.text
    fmt = "%m-%d-%Y"
    return datetime.datetime.strptime(text, fmt).date()


def parse_extra_cell(cell):
    briefs = False
    video = False
    text = cell.text
    if text:
        if 'B' in text:
            briefs = True
        if 'V' in text:
            video = True
    return briefs, video


def parse_result_row(row):
    acell, date_cell, name, extra = row.select('td')
    anchor = acell.find('a')
    href = anchor.get('href')
    if href.startswith('case.php'):
        href = os.path.join(base_url, href)
    docket_num = anchor.text
    date = parse_date_cell(date_cell)
    name = name.text
    briefs, video = parse_extra_cell(extra)
    data = dict(docket_num=docket_num, link=href, date=date,
                name=name, briefs=briefs, video=video)
    return data


def parse_search_results(results_table):
    rows = results_table.select('tr')[1:]
    cases = list()
    for row in rows:
        cases.append(parse_result_row(row))
    return cases


def search_year(year, court="sct"):
    search_url = "http://judicial.mc.edu/researchresults.php"
    table_selector = "#main-column > table"
    data = year_search_data(year, court=court)
    response = requests.post(search_url, data=data)
    soup = BeautifulSoup(response.content, 'lxml')
    tables = soup.select(table_selector)
    if len(tables) != 2:
        msg = "search returned {} tables".format(len(tables))
        raise RuntimeError(msg)
    summary, results = tables
    num_results = parse_search_summary(summary)
    print("court", court, "year", year, "num_results", num_results)
    rows = results.select('tr')
    actual_rows = rows[1:]
    if len(actual_rows) != num_results:
        raise RuntimeError("Parsing error: {}".format(data))
    return parse_search_results(results)
