# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import collections
collections.Callable = collections.abc.Callable
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    #print(entries)
    for entry in entries:
        #print(entry)
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        #description = translate_html(entry.description)
        description = translate_html(entry.title_detail.value)
        '''pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")'''
        pubdate = translate_html(entry.published)
        pubdate = datetime.strptime(pubdate, "%Y-%m-%dT%H:%M:%S%z")
        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret
#-----------------------------------------------------------------------

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory:
    def __init__(self,guid,title,description,link,pubdate):
        self.guid=guid
        self.title=title
        self.description=description
        self.link=link
        self.pubdate=pubdate.replace(tzinfo=None)
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate




#======================
# Triggers
#======================
    
class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS
# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self,string):
        self.string=string
    def is_phrase_in(self,search_string):
        #getting words lists from search and original strings
        wssearch_string = search_string
        wsorig_string = self.string
        for sign in string.punctuation:
            wssearch_string = wssearch_string.replace(sign,' ')
            wsorig_string = wsorig_string.replace(sign,' ')
        search_words=wssearch_string.split()
        orig_words=wsorig_string.split()
        #getting unified format strings from search and original strings
        search_words=' '.join(search_words).lower()+' '
        orig_words=' '.join(orig_words).lower()+' '
        if(search_words in orig_words):
            return True
        else:
            return False
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    #string - phrase we are searching for
    def __init__(self,string):
        self.searchstring=string
    def evaluate(self, story):
        PhraseTrigger.__init__(self, story.get_title())
        return PhraseTrigger.is_phrase_in(self,self.searchstring)
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self,string):
        self.searchstring=string
    def evaluate(self,story):
        PhraseTrigger.__init__(self, story.get_description())
        return PhraseTrigger.is_phrase_in(self,self.searchstring)
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self,string):
        self.datentime=datetime.strptime(string,"%d %b %Y %H:%M:%S")
        self.datentime=self.datentime.replace(tzinfo=None)
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self,ctime):
        TimeTrigger.__init__(self,ctime)
    def evaluate(self,story):
        if(self.datentime>story.get_pubdate()):
            return True
        else:
            return False
class AfterTrigger(TimeTrigger):
    def __init__(self,ctime):
        TimeTrigger.__init__(self,ctime)
    def evaluate(self,story):
        if(self.datentime<story.get_pubdate()):
            return True
        else:
            return False
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger:
    def __init__(self,trigger):
        self.trigger=trigger
    def evaluate(self,story):
        return not self.trigger.evaluate(story)
# Problem 8
# TODO: AndTrigger
class AndTrigger:
    def __init__(self,trigger1,trigger2):
        self.trigger1=trigger1
        self.trigger2=trigger2
    def evaluate(self,story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
# Problem 9
# TODO: OrTrigger
class OrTrigger:
    def __init__(self,trigger1,trigger2):
        self.trigger1=trigger1
        self.trigger2=trigger2
    def evaluate(self,story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)
#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filtered_stories = []
    for i in range(len(stories)):
        for trigger in triggerlist:
            if trigger.evaluate(stories[i]):
                filtered_stories.append(stories[i])
                break
        '''for trigger in triggerlist:
            print(trigger.evaluate(stories[i]))
            if trigger.evaluate(stories[i])==False:
                del(filtered_stories[i-deletednum])
                deletednum = deletednum+1
                break
            print('------------')'''
    return filtered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    triggers = []
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    returntriggers = []
    triggersdict = {}
    for line in lines:
        if "ADD" in line:
            dataarr = line.split(',')
            #print(dataarr)
            for i in range(1,len(dataarr)):
                #print(dataarr[i])
                returntriggers.append(triggersdict[dataarr[i]])
        elif "TITLE" in line:
            dataarr = line.split(',')
            triggersdict[dataarr[0]]=TitleTrigger(dataarr[2])
            #print()
        elif "DESCRIPTION" in line:
            dataarr = line.split(',')
            triggersdict[dataarr[0]]=DescriptionTrigger(dataarr[2])
            #print()
        elif "AFTER" in line:
            dataarr = line.split(',')
            triggersdict[dataarr[0]]=AfterTrigger(dataarr[2])
            #print()
        elif "BEFORE" in line:
            dataarr = line.split(',')
            triggersdict[dataarr[0]]=BeforeTrigger(dataarr[2])
            #print()
        elif "AND" in line:
            dataarr = line.split(',')
            triggersdict[dataarr[0]]=AndTrigger(triggersdict[dataarr[2]],triggersdict[dataarr[3]])
            #print()
        elif "OR" in line:
            dataarr = line.split(',')
            triggersdict[dataarr[0]]=OrTrigger(triggersdict[dataarr[2]],triggersdict[dataarr[3]])
            #print(dataarr)
        elif "NOT" in line:
            dataarr = line.split(',')
            triggersdict[dataarr[0]]=NotTrigger(triggersdict[dataarr[2]])
            #print()
    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines,end='\n') # for now, print it so you see what it contains!
    print(returntriggers)
    return returntriggers


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        #t1 = TitleTrigger("election")
        #t2 = DescriptionTrigger("Trump")
        #t3 = DescriptionTrigger("Clinton")
        #t4 = AndTrigger(t2, t3)
        #t1 = TitleTrigger("Trump")
        #t4 = TitleTrigger("Trump")
        #triggerlist = [t1, t4]
        #triggerlist = [t1]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers1.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            #print("We are here!\n")
            stories = process("http://news.yahoo.com/rss/topstories")
            #print("We are here1!\n")
            #print(stories)
            #stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

