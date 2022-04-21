# Gabriel Mortensen
# HTML Tester for HRS

# ~~~~~~~~~Import Libraries~~~~~~~~~~~~~~
# make, write to and delete files
import os
# Obtain the path of the working directory
from pathlib import Path
# Read all the .html files recursviley in all sub directories
import glob
# URL requests to obtain result of accessing URL
import requests
import requests as req
# Allows code to open specfied URL
import urllib.request
import urllib.request as urllib2
from urllib.request import urlopen
# Allows code to read and write from a csv
from bs4 import BeautifulSoup
import csv
from csv import writer
import pandas as pd
# Allows amount of characters to be quickly searched and counted
import re
# Allows for the comparison of similarity of files,strings, etc...
import spacy
import difflib
from difflib import SequenceMatcher
# Allows for opening of HTML files
import codecs
# ~~~~~~~~~Global Variables~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~Setup Function ~~~~~~~~~~~~~~
# Sets up the working directory and notifies user
# Sets up the csv file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def startup():
    # Get the current working directory
    current_directory = os.getcwd()
    # Notify user on the directry being worked on
    print('\n\nStarted In: ', current_directory, '\n')

    # Set up the CSV file by writing in the header
    header = ['URL', 'Already Redirecting',
              'Not Redirecting but Found on Wordpress',
              'Not Found on Wordpress', 'Cannot be Reached']
    with open('Results.csv', 'w', encoding='UTF8') as results:
        writer = csv.writer(results)
        # write the header
        writer.writerow(header)
    results.close()

    # obtain information of paragraph CSV
    # df = pd.read_csv('URL_And_Paragraphs.csv', sep=";", encoding='cp1252')
    # Get list of paragraphs
    # run only if CSV is empty
    # if(df.empty):
    #    Obtain_Web_Paragraph_List()

    return current_directory

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This main function obtains all the .html files
# then calls functions to run checks
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main():

    # call the start up function to get things started
    current_directory = startup()

    # Examine every file in directory and sub directories that have .html at the end
    file = Path(current_directory).glob('*')

    # For each html file do the following:
    for i in glob.glob(current_directory + '\\**\\*.html', recursive=True):

        # assign string to current directory path with .html file
        URL_Ending = i
        # replace the uncessary portion of the directory
        URL_Ending = URL_Ending.replace(current_directory, '')
        # turn all backslashes to foward slashes as common of URL link format
        URL_Ending = URL_Ending.replace('\\', '/')
        # If URL has space then modify URL
        URL_Ending = URL_Ending.replace(' ', '%20')

        # This variable is the url of the current .html file
        URL = "https://rabbit.org" + URL_Ending

        print('~~~~~~~~~~~~~~~~~~~')
        print('NEXT URL CHECK:')
        print(URL)
        # Obtain the status and result for particular page
        Obtain_Page_Status(URL, i)

        # print('!!!!!!!!!!!!!!!!!!!!!!!!!')

        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # # obtain information from the html file
        # f = codecs.open(i, 'r')
        # original_text = f.read()
        # f.close()
        # # use soup to find all p elements of html file in directory (not website page)
        # soup = BeautifulSoup(original_text, features="lxml")
        # # obtain a segment of the all paragraph elements from the original html file text
        # file_text = ' '
        # for tag in soup.findAll('p'):
        #     file_text = file_text + tag.getText()
        # file_text.strip()
        # file_text = " ".join(file_text.split())
        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # print('=================================')

        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # # content text
        # file = open('Page_Link_List.csv', encoding="utf8")
        # csvreader = csv.reader(file)
        # header = []
        # tuples = []
        # header = next(csvreader)

        # # Go through all the titles in the wordpress website and compare with the current header/title
        # for tuples in csvreader:
        #     soup = BeautifulSoup(tuples[2], features="lxml")
        #     content_text = ' '
        #     for tag in soup.findAll('p'):
        #         content_text = content_text + tag.getText()
        #     content_text.strip()
        #     content_text = " ".join(content_text.split())
        # print(content_text)
        # file.close()
        # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # print('!!!!!!!!!!!!!!!!!!!!!!!!!')

        # print('~~~~~~~~~~~~~~~~~~~')


"""
Obtains the paragraph elements from file
"""


def Obtain_File_Paragraph(URL, original_file):
 # obtain information from the html file
    f = codecs.open(original_file, 'r')
    original_text = f.read()
    f.close()
    # use soup to find all p elements of html file in directory (not website page)
    soup = BeautifulSoup(original_text, features="lxml")
    # obtain a segment of the all paragraph elements from the original html file text
    file_text = ' '
    for tag in soup.findAll('p'):
        file_text = file_text + tag.getText()
    file_text.strip()
    file_text = " ".join(file_text.split())
    return file_text, soup


def Obtain_Web_Paragraph_List():

    # open the CSV file to read the URLs of Wordpress pages
    file = open('WordPress_URLs.csv', encoding="utf8")
    csvreader = csv.reader(file)
    header = next(csvreader)
    paragraph_list = []

    with open('a.csv', 'w', encoding="utf-8") as results:

        # go through all the URLs
        for tuples in csvreader:
            # Obtain page content (from csv) and determine which file content is the most similar
            webUrl = urllib.request.urlopen(tuples[0])
            data = webUrl.read()
            # use soup to find all p elements of html website page
            soup_web = BeautifulSoup(data, features="lxml")
            # obtain a segment of the all paragraph elements from the original html file text
            web_text = ' '

            # only extract the paragraph elements of html document
            for tag in soup_web.findAll('p'):
                web_text = web_text + tag.getText()
            web_text.strip()
            web_text = " ".join(web_text.split())

            # obtain data along with coresponding URL
            Data_Paragraph = [tuples[0], web_text[0:125]]

            # store results in CSV
            writer_object = csv.writer(results)
            writer_object.writerow(Data_Paragraph)

            # show some snippet of pargraph to user
            print("Pargraph snippet:" + web_text[0:125])

            # add paragraph to list
            # paragraph_list.append(web_text)

    results.close()
    file.close()
    return paragraph_list


"""
Gives a report that lists the status of each URL
There are three conditions:
already redirecting to xxx,
not redirecting but found on wordpress at xxx url,
and not found on wordpress.
"""


def Obtain_Page_Status(URL, original_file):

    # obtain text of the current HTMl file (not page, just the file)
    file_text, soup = Obtain_File_Paragraph(URL, original_file)
    # obtain the response of the URL
    response = req.get(URL)

    # website page cannot be reached
    if (response.status_code == 404 or response.status_code == 401):
        data = [URL, 'False', 'False', 'False', 'True']
        with open('Results.csv', 'a') as results:
            writer_object = csv.writer(results)
            writer_object.writerow(data)
        results.close()
        print('\033[1;36;40m  Error  \033[0;37;40m')
    # website page can be reached
    else:
        # website has been redirected
        if ('<meta http-equiv="refresh" content="0;URL=' in soup):

            # obtain index of redirection statment in html file
            redirected_URL_index = html_text.find(
                '<meta http-equiv="refresh" content="0;URL')

            # add constants to obtain the Redirected URL link (index starts 43 back)
            redirected_URL_index = redirected_URL_index + 43

            # run through line until you get entire url (After content="0;URL=)
            i = 0
            while True:
                if(html_text[redirected_URL_index + i] == '"'):
                    break
                i = i + 1

            # update results CSV with redirected link
            redirected_URL = html_text[redirected_URL_index:redirected_URL_index + i]
            data = [URL, redirected_URL, 'False', 'False', 'False']
            with open('Results.csv', 'a') as results:
                writer_object = csv.writer(results)
                writer_object.writerow(data)
            results.close()
            print(
                '\033[1;35;40m Redirects to A WordPress Page \033[0;37;40m')

        # If website has not been redirected
        else:

            # Obtain the list of paragraphs for each webapge
            paragraph_list = Obtain_Web_Paragraph_List()

            # Obtain content from CSV file of all wordpress links and paragraphs
            file = open('URL_And_Paragraphs.csv', encoding="utf8")
            csvreader = csv.reader(file)

            # reset the boolean detection for the previous link
            Redirected = False
            redirect = ''

            # index
            i = 0
            # Go through all the titles in the wordpress website and compare with the current header/title
            for tuples in csvreader:

                if(file_text[0:125] == tuples[1]):
                    # url related to matchign paragraph
                    redirect = tuples[0]
                    data = [URL, 'False', redirect, 'False', 'False']
                    with open('Results.csv', 'a') as results:
                        writer_object = csv.writer(results)
                        writer_object.writerow(data)
                    results.close()
                    print(
                        '\033[1;32;40m Needs to direct to: \033[0;37;40m' + tuples[1])
                    Redirected = True
                i = i + 1
            # close the file being read from
            file.close()

            # if no website text matched then likely there is no redirect
            if(Redirected == False):
                data = [URL, 'False', 'False', 'True', 'False']
                with open('Results.csv', 'a') as results:
                    writer_object = csv.writer(results)
                    writer_object.writerow(data)
                results.close()
                print(
                    '\033[1;31;40m Does not redirect, no WordPress Page \033[0;37;40m')


# This is where the program begins
if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')

    with urllib.request.urlopen("WordPress_URLs.csv") as resp:
        df1 = pd.read_csv(resp, sep=";", encoding='cp1252')

    print(df1)

    exit()
    main()
