#!/usr/bin/env python3
"""
Fichier de test
"""

import random
import sqlite3
import urllib.request

from bs4 import BeautifulSoup

import sportsbetting as sb
from sportsbetting.database_functions import is_id_consistent
from sportsbetting.user_functions import parse_competitions


def test_parsing():
    """
    :return:Test simple
    """
    sb.TEST = True
    url = "http://www.comparateur-de-cotes.fr/comparateur/football"
    soup = BeautifulSoup(urllib.request.urlopen(url), features="lxml")
    sb.ODDS = {}
    names = []
    for line in soup.find_all(attrs={"class": "subhead"}):
        if "Principaux championnats" in str(line):
            for link in line.findParent().find_all(["a"]):
                names.append(link.text.strip())
            break
    name_competition = random.choice(names)
    parse_competitions([name_competition], "football", "pmu", "winamax")
    assert len(sb.ODDS) > 0
    sb.TEST = False


def test_parsing_chromedriver():
    """
    :return:Test simple
    """
    sb.TEST = True
    sb.selenium_init.start_drivers()
    url = "http://www.comparateur-de-cotes.fr/comparateur/football"
    soup = BeautifulSoup(urllib.request.urlopen(url), features="lxml")
    sb.ODDS = {}
    names = []
    for line in soup.find_all(attrs={"class": "subhead"}):
        if "Principaux championnats" in str(line):
            for link in line.findParent().find_all(["a"]):
                names.append(link.text.strip())
            break
    name_competition = random.choice(names)
    print(name_competition)
    parse_competitions([name_competition], "football", "betclic", "unibet")
    for site in sb.SELENIUM_SITES:
        sb.selenium_init.DRIVER[site].quit()
    sb.TEST = False
    assert len(sb.ODDS) > 0


def test_consistency():
    sb.TEST = True
    conn = sqlite3.connect(sb.PATH_DB)
    c = conn.cursor()
    c.execute("""
    select id, count(*) as c from names group by names.id having c>1
    """)
    results = c.fetchall()
    for result in results:
        assert is_id_consistent(result[0])
    sb.TEST = False
