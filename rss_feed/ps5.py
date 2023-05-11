

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import collections
collections.Callable = collections.abc.Callable

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        try:
            description = translate_html(entry.description)
        except:
            description = ''
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            # pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
            pubdate = ''

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret



class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
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


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    
    def is_phrase_in(self, text):
        for c in string.punctuation:
            text = text.replace(c,' ')
        text = ' '.join(text.split())
        text = text.lower()
        index = text.find(self.phrase)
        if index != -1 and (index + len(self.phrase) >= len(text) or text[index+len(self.phrase)] == ' '):
            return True
        return False


class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

         

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time = datetime.strptime(time,'%d %b %Y %H:%M:%S')


class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        if not story.get_pubdate().tzinfo is None:
            timetz = (self.time).replace(tzinfo=pytz.timezone("EST"))
        else:
            timetz = self.time
        return timetz > story.get_pubdate()

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
            if not story.get_pubdate().tzinfo is None:
                timetz = (self.time).replace(tzinfo=pytz.timezone("EST"))
            else:
                timetz = self.time
            return timetz < story.get_pubdate()

# COMPOSITE TRIGGERS

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
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

    story_list = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                story_list.append(story)
    return story_list



#======================
# User-Specified Triggers
#======================

def create_trigger(type, arg):
    if len(arg) == 1:
        arg = arg[0]
    if type == 'TITLE':
        return TitleTrigger(arg)
    if type == ' DESCRIPTION':
        return DescriptionTrigger(arg)
    if type == 'AFTER':
        return AfterTrigger(arg)
    if type == 'BEFORE':
        return BeforeTrigger(arg)
    if type == 'NOT':
        return NotTrigger(arg)
    if type == 'AND':
        return AndTrigger(arg[0], arg[1])
    if type == 'OR':
        return  OrTrigger(arg[0], arg[1])
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """

    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)


    triggerlist = []
    triggerdict = {}
    for line in lines:
        parameters = line.split(',')
        if parameters[0] == 'ADD':
            for i in range(1,len(parameters)):
                triggerlist.append(triggerdict[parameters[i]])
        else:
            type = parameters[1]
            args = ()
            for i in range(2,len(parameters)):
                args += (parameters[i],)
                triggerdict[parameters[0]] = create_trigger(type, args)

    return triggerlist



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')
        
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
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))
            print(stories)
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

