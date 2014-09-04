#!/usr/bin/env python3
"""
From: https://github.com/tpopela/google_calendar_fetcher
For Python3

Gets Google Calendar's account events and prints them to stdout
"""

import getopt
from urllib.parse import urlencode
import httplib2
import datetime
from dateutil.relativedelta import *
import xml.etree.ElementTree as etree
from operator import itemgetter

__events__ = {}


def login(username, password):
    ''' Logins to Google Account '''

    values = {'accountType': 'GOOGLE',
              'Email': username,
              'Passwd': password,
              'source': 'google_calendar_fetcher',
              'service': 'cl'}

    url_login = 'https://www.google.com/accounts/ClientLogin'

    response, content = httplib2.Http().request(url_login,
        'POST',
        urlencode(values),
        headers={'Content-Type': 'application/x-www-form-urlencoded'})

    if response.status == 403:
        print('Bad username or password')

    assert response.status == 200,\
        "Can't log in (network error?)"

    reply = content.decode().split('\n')
    token = reply[2].split('=')[1]

    return token


def get_calendars(token):
    ''' Gets calendars list '''

    token_header = "GoogleLogin auth=" + str(token)
    url_calendars = 'https://www.google.com/calendar'
    url_calendars += '/feeds/default/allcalendars/full'

    response, content = httplib2.Http().request(url_calendars,
        headers={'Authorization': token_header})

    assert response.status == 200,\
        "Can't get calendars list (network error?)"

    parse_calendars(content, token_header)

    return content


def parse_calendars(xml_calendars, token_header):
    ''' Parses calendars list '''

    tree = etree.XML(xml_calendars)
    calendars = tree.findall('{http://www.w3.org/2005/Atom}entry')
    for calendar in calendars:
        calendar_content = calendar.find('{http://www.w3.org/2005/Atom}content')
        calendar_id = calendar_content.get('src')
        get_calendar_entries(calendar_id, token_header)


def get_calendar_entries(calendar_id, token_header):
    ''' Get entries (until one month) from calendar '''

    now = datetime.date.today()
    startDate = now + relativedelta(weeks=-1)
    endDate = now
    #startDate = datetime.date.today()
    #endDate = startDate + relativedelta(months=+1)
    values = {'start-min': startDate.strftime("%Y-%m-%d") + "T00:00:00",
              'start-max': endDate.strftime("%Y-%m-%d") + "T23:59:59"}

    url = "%s?%s" % (calendar_id, urlencode(values))

    response, content = httplib2.Http().request(url,
        headers={'Authorization': token_header, 'cache-control': 'no-cache'})

    assert response.status == 200,\
        "Can't get entries from calendar (network error?)"

    parse_events(content)


def parse_events(raw_xml):
    ''' Parses events '''

    tree = etree.XML(raw_xml)
    entries = tree.findall('{http://www.w3.org/2005/Atom}entry')
    for entry in entries:
        title = entry.find('{http://www.w3.org/2005/Atom}title')
        when = entry.find('{http://schemas.google.com/g/2005}when')
        try:
            startTime = when.get('startTime')
        except:
            now = datetime.date.today()
            startTime = now.strftime("%Y-%m-%d") + "T00:00:00"
        if title.text is None:
            __events__['No subject'] = startTime
        else:
            __events__[title.text] = startTime

# DaleEMoore@gMail.Com, 3 Aug 3014 6:07 AM CST, who cares?
#def get_name_day():
#    ''' Gets name day '''
#    url_name_day = 'http://svatky.adresa.info/txt'
#    response, content = httplib2.Http().request(url_name_day)
#
#    assert response.status == 200,\
#        "Can't get name day (network error?)"
#
#    if content.decode() == "":
#        return ""
#
#    temp_name_day = content.decode().split(";")
#    name_day = temp_name_day[1].split("\n")
#
#    return " - " + name_day[0]


def print_header():
    ''' Prints header to stdout '''

    now = datetime.datetime.now()
    output = ""

    output = "Today is " + now.strftime("%Y-%m-%d") + ", "
    if (int(now.strftime("%W"))) % 2 == 0:
        output += "even week"
    else:
        output += "odd week"

    # DaleEMoore@gMail.Com, 3 Aug 3014 6:07 AM CST, who cares?
    #output += get_name_day()

    print(output)


def printOut():
    ''' Prints events to stdout '''

    #print_header()

    output_line = ""

    now = datetime.datetime.now()

    events_sorted = sorted(__events__.items(), key=itemgetter(1))

#    for key, value in events_sorted:
#       print(key + " " + value)

    for key, value in events_sorted:

        if len(value) == 10:
            event_start_time = datetime.datetime.strptime(value, "%Y-%m-%d")
            time = False
        else:
            date_time = value.split('.')
            event_start_time = datetime.datetime.strptime(date_time[0],
                                                          "%Y-%m-%dT%H:%M:%S")
            time = True

        delta = event_start_time - now
        if (delta.seconds < 0):
            continue
        # TODO; match fields to old output
        # TODO; match fields to new labels
        outHead1 = '"Event", "DateTime", "DeltaSeconds", "Delta", "DeltaHours"'
        print (outHead1)
        outDetail1 = '"{}", "{}", "{}", "{}", "{}"'.format(key, value, str(delta.seconds), str(delta), str(delta.seconds // 3600))
        print (outDetail1)
        print("1:" + key + " " + value + " " + str(delta.seconds) + " " + str(delta) + "            " + str(delta.seconds // 3600))
        pass

        outWhen = ""
        if (time is True and (delta.days == 0 or delta.days == -1)):
            if (delta.days >= 0):
                diff = delta.seconds // 3600
                if (now.day == event_start_time.day):
                    if (diff == 0):
                        outWhen = "Now"
                        output_line += "Now         "
                    elif (diff == 1):
                        outWhen = "In 1 hour"
                        output_line += "In  1 hour  "
                    else:
                        if (diff < 10):
                            outWhen = "In  " + str(diff) + " hours "
                            output_line += "In  " + str(diff) + " hours "
                        else:
                            outWhen = "In " + str(diff) + " hours "
                            output_line += "In " + str(diff) + " hours "
                else:
                    outWhen = "Tomorrow"
                    output_line += "Tomorrow    "
            else:
                outWhen = ""
                continue
        else:
            if (delta.days < 0):
                outWhen = "Today"
                output_line += "Today       "
            elif (delta.days == 0):
                outWhen = "Tomorrow"
                output_line += "Tomorrow    "
            else:
                if (delta.days > 8):
                    outWhen = "In "
                    output_line += "In "
                else:
                    outWhen = "In "
                    output_line += "In  "
                outWhen += str(delta.days + 1) + " days  "
                output_line += str(delta.days + 1) + " days  "

        outStart = ""
        if (time is True):
            outStart = event_start_time.strftime("%Y-%m-%d %H:%M ")
            output_line += event_start_time.strftime("%d.%m.%Y %H:%M ")
        else:
            if (delta.days <= -1):
                outStart = now.strftime("%Y-%m-%d")
                output_line += now.strftime("%Y-%m-%d       ")
            else:
                outStart = event_start_time.strftime("%Y-%m-%d")
                output_line += event_start_time.strftime("%Y-%m-%d      ")

        output_line += key

        if (output_line != ""):
            outHead2 = '"When", "Start"'
            print (outHead2)
            outDetail2 = '"{}", "{}"'.format(outWhen, outStart)
            print (outDetail2)
            print("2:" + output_line)
            pass

        print(outHead1, outHead2)
        print(outDetail1, outDetail2)

        output_line = ""
        time = False


def print_output():
    ''' Prints events to stdout '''

    print_header()

    output_line = ""

    now = datetime.datetime.now()

    events_sorted = sorted(__events__.items(), key=itemgetter(1))

#    for key, value in events_sorted:
#       print(key + " " + value)

    for key, value in events_sorted:

        if len(value) == 10:
            event_start_time = datetime.datetime.strptime(value, "%Y-%m-%d")
            time = False
        else:
            date_time = value.split('.')
            event_start_time = datetime.datetime.strptime(date_time[0],
                                                          "%Y-%m-%dT%H:%M:%S")
            time = True

        delta = event_start_time - now
        if (delta.seconds < 0):
            continue

        print(key + " " + value + " " + str(delta.seconds) + " " + str(delta) + "            " + str(delta.seconds // 3600))

        if (time is True and (delta.days == 0 or delta.days == -1)):
            if (delta.days >= 0):
                diff = delta.seconds // 3600
                if (now.day == event_start_time.day):
                    if (diff == 0):
                        output_line += "Now         "
                    elif (diff == 1):
                        output_line += "In  1 hour  "
                    else:
                        if (diff < 10):
                            output_line += "In  " + str(diff) + " hours "
                        else:
                            output_line += "In " + str(diff) + " hours "
                else:
                    output_line += "Tomorrow    "
            else:
                continue
        else:
            if (delta.days < 0):
                output_line += "Today       "
            elif (delta.days == 0):
                output_line += "Tomorrow    "
            else:
                if (delta.days > 8):
                    output_line += "In "
                else:
                    output_line += "In  "
                output_line += str(delta.days + 1) + " days  "

        if (time is True):
            output_line += event_start_time.strftime("%d.%m.%Y %H:%M ")
        else:
            if (delta.days <= -1):
                output_line += now.strftime("%Y-%m-%d       ")
            else:
                output_line += event_start_time.strftime("%Y-%m-%d      ")

        output_line += key

        if (output_line != ""):
            print(output_line)

        output_line = ""
        time = False


def main(username, password):
    ''' Entry point '''

    token = login(username, password)
    get_calendars(token)
    print_output()

if __name__ == '__main__':
    import sys

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f", ["filename="])
    except getopt.GetoptError as err:
        print("Only argument is -f or --filename followed by name of file "
                "that contains your Google username and password "
                "on one line separated by space!")
        sys.exit(2)

    # TODO; get the username and password from somewhere secret.
    # TODO; setup MooreWorksTest, t3st.ts3t, email account?
    username = "MooreWorksService"
    password = "s3rvic3.M3"
    #username = None
    #password = None

    for option, argument in opts:
        if option in ("-f", "--filename"):
            try:
                with open(argument, mode='r', encoding='utf-8') as credentials:
                    username, password = credentials.read().split()
            except IOError:
                print("File not found!")
                sys.exit(2)

    main(username, password)

    sys.exit()
