import os
import pickle
import time

from sqlalchemy.exc import IntegrityError

from .database import Case
from .search_year import search_year


def get_cases(year, court):
    return search_year(year, court=court)


def get_all_cases(court, filename):
    years = range(2000, 2020)
    if not os.path.isfile(filename):
        with open(filename, 'wb') as outfile:
            cases = dict()
            for year in years:
                cases[year] = get_cases(year, court)
                time.sleep(5)
            pickle.dump(cases, outfile)
    else:
        cases = pickle.load(open(filename, 'rb'))
    return cases


def make_case(court, data, dbclass=Case):
    case = dbclass()
    case.court = court
    docket_num = data['docket_num']
    if ' ' in docket_num:
        parts = [p.strip() for p in docket_num.split()]
        docket_num = ' '.join(parts)
    case.docket_num = docket_num
    for key in ['date', 'name', 'link']:
        setattr(case, key, data[key])
    case.has_brief = data['briefs']
    case.has_video = data['video']
    return case


def insert_case(session, court, data):
    case = make_case(court, data)
    session.add(case)
    session.commit()
    print("Added single", case.docket_num, case.name)


def insert_many_cases(session, court, rows):
    good_cases = list()
    for row in rows:
        case = make_case(court, row)
        session.add(case)
        good_cases.append(case)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        good_cases = list()
        for row in rows:
            insert_case(session, court, row)
    if good_cases:
        for case in good_cases:
            print("Quickly added", case.date.year, case.docket_num, case.name)
