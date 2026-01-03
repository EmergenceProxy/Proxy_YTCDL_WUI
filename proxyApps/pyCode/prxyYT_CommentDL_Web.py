#Youtube comment downloader gui
#Purpose: Accept a youtube link, download and display comments
#Usage: python prxyYT_CommentDL_gui.py

import os   #used to handle files
import json #used for data storage/handling
import operator #Used for sorts
import datetime # Used to display dates
from warnings import catch_warnings
from sentiment_analysis import analyze_overall_sentiment
import youtube_comment_downloader #used to get youtube comment data
from itertools import islice #used to extract youtube comment data


# from tkinter import *
# from tkinter.scrolledtext import ScrolledText


# def print_log(logMessage):
#     time_stamp=datetime.datetime.today()
#     print(f"{time_stamp}: {logMessage}")
#     return f"{time_stamp}: {logMessage}"


class DownloadSession:
    def __init__(self, form=None):
        
        self.entry_for_link = None
        self.loadNumComments = None
        # self.label_for_comments = None
        self.comment_dict = {}
        self.workingDir = "/home/proxyApps/appData/ytcData"
        self.customFilename = ""
        
        print(f"DownloadSession: init: len(form):{form}")
        if form:
            print("DownloadSession: init: form found")
            self.entry_for_link = form["url_input"]
            self.loadNumComments = int(form["commentCount_input"])
            self.entry_for_un_search = form["un_search_input"]
            self.entry_for_comment_search = form["comment_search_input"]
            self.entry_for_cid_search = form["cid_search_input"]
            # self.label_for_comments = None
            self.comment_dict = {}
        

##############################---------------Setup menus---------------------#############################

    
# ---------------------------- Save ------------------------------- #

    def getYoutubeVideoID(self):
        import urllib.parse as urlparse
        youtube_url = self.entry_for_link
        url_data = urlparse.urlparse(youtube_url)
        query = urlparse.parse_qs(url_data.query)
        videoID="temp"

        aKeyList = list(query.keys())
        print(f"getYoutubeVideoID: aKeyList: {aKeyList}")
        for entry in query:
            print(f"getYoutubeVideoID: Entry: {entry}")
            print(f"getYoutubeVideoID: query[entry]: {query[entry]}")

        try:
            videoID = query["v"][0]
            pass
        except Exception as err:
            print(f"getYoutubeVideoID: Error: {err}")
            videoIDhc=youtube_url[32:]
            print(f"getYoutubeVideoID: video hardcode cut: {videoIDhc}")
            return videoIDhc
            pass
        else:
            print(f"getYoutubeVideoID: {videoID}")
            return videoID
            pass


        # print(f"getYoutubeVideoID: {video}")
        return videoID

    def saveYTComment(self):
        print_log(f"saveYTComment: Start")
        files = [('All Files', '*.*'),
                 ('Python Files', '*.py'),
                 ('Text Document', '*.txt')]

        now = ""  # + dt.now()

        # defaultFilename = os.getlogin() + "_" + str(now) + "_pwManData.json"  # "<username>_"+str(now)+"_pwManData.bean"
        defaultFilename = self.getYoutubeVideoID()+"_CommentData.json"
        # myFile = self.customFilename
        myCommentFilePath = f"{self.workingDir}/{defaultFilename}"
        # myIssDataPath = myCommentFilePath#"\Users\geneb\PycharmProjects\PythonProject\.venv\data"+defaultFilename

        if not os.path.exists(myCommentFilePath):
            print(f"save: create: {myCommentFilePath}")
            with open(myCommentFilePath, 'w') as myFile:
                if myFile:
                    json.dump(self.comment_dict, myFile, indent=4, default=str)
                    return

        with open(myCommentFilePath, 'r+') as myFile:
            if myFile:
                # File was selected, you can now work with the file_path
                print(f"save: myFile: {myFile}")
                print(f"save: myFile.name: {myFile.name}")

                try:
                    fileData = json.load(myFile)
                except json.decoder.JSONDecodeError as err:
                    print(f"save: jsonDecodeError: {err}")
                    myFile.seek(0)
                    json.dump(self.comment_dict, myFile, indent=4, default=str)
                    myFile.truncate()
                    print(f"save: jsonDecodeError resolved!")
                else:
                    print(f"save: fileData loaded")
                    # print(f"save: fileData: {fileData}")
                    # fileData.update(myDownloadSession.comment_dict) #Dont want to update since my
                    # fileData = combineCommentDicts(fileData, myDownloadSession.comment_dict)
                    fileData = self.comment_dict

                    # Move the pointer to the beginning of the file to overwrite
                    myFile.seek(0)

                    # Use to create original file 2
                    # json.dump(newIssEntryList, myFile, indent=4)
                    json.dump(fileData, myFile, indent=4, default=str)
                    # remove remaining part of old data
                    myFile.truncate()

#############################------------------Gui Functions-------------------###############################
    def loadVideoComments(self, name): #Implement comment loading logic
        print_log(f"loadVideoComments: name: {name}")
        returnDict={}
        videoID = self.getYoutubeVideoID()+"_CommentData.json"
        myCommentFilePath = f"{self.workingDir}/{videoID}"

        if not os.path.exists(myCommentFilePath):
            print_log(f"loadVideoComments: path not found: {myCommentFilePath}")
            return returnDict

        with open(myCommentFilePath, 'r+') as myFile:
            if myFile:
                # File was selected, you can now work with the file_path
                print_log(f"loadVideoComments: myFile: {myFile}")
                print_log(f"loadVideoComments: myFile.name: {myFile.name}")

                try:
                    returnDict = json.load(myFile)
                    aKeyList = list(returnDict.keys())
                    #print(f"loadVideoComments: myFile.name.keyList: {aKeyList}")
                except json.decoder.JSONDecodeError as err:
                    print_log(f"loadVideoComments: jsonDecodeError: {err}")
                    myFile.seek(0)
                    json.dump(self.comment_dict, myFile, indent=4, default=str)
                    myFile.truncate()
                    print_log(f"loadVideoComments: jsonDecodeError resolved!")
                else:
                    print_log(f"loadVideoComments: fileData loaded")
                    # print(f"loadVideoComments: fileData: {fileData}")
                    # fileData.update(myDownloadSession.comment_dict) #Dont want to update since my
                    # fileData = combineCommentDicts(fileData, myDownloadSession.comment_dict)
                    self.comment_dict = returnDict
                    return returnDict
        return returnDict
        #3 methods to get video data
        if videoID in self.getVideoList():
            #2 Load from saved file
            return self.readYTComments(videoID)
        elif videoID in self.queryVideoList():
            #3 Load from DB? Future expanded functions? Independent user lookup? Could create tables in files.
            return self.queryYTComments()
        else:
            #1 load from ytdl mod. Takes time?
            returnDict = self.getYTComments()
            try:
                print("loadVideoComments: run saveYTComment")
                self.saveYTComment()
            except Exception as error:
                print("loadVideoComments: An exception occurred: ", error)
                traceback.print_exc()
                print()
                print()
            finally:
                return returnDict
        pass

    def getVideoList(self):
        print("Start readYTComments")
        videoList = []
        print(os.listdir())

        return videoList
    def queryVideoList(self):
        print("Start readYTComments")
        videoList = []
        return videoList

    def readYTComments(self, videoID):
        print("readYTComments: videoID: ", videoID)
        print("readYTComments: loadNumComments: ", self.loadNumComments)
        pass
    def queryYTComments(self, videoID):
        print("readYTComments: videoID: ", videoID)
        print("queryYTComments: loadNumComments: ", self.loadNumComments)
        pass

    def getYTComments(self):
        print_log("getYTComments:")
        myCommentFilePath = self.workingDir+"/tempYTComments.json"
        myCommentText = ""
        youtube_url = "https://www.youtube.com/watch?v=c52IzePdOag" #
        youtube_url = self.entry_for_link
   
        #youtube-comment-downloader --url myCommentLink --output myCommentFilePath
        myYoutubeCommentDownloader = youtube_comment_downloader.YoutubeCommentDownloader()
        SORT_BY_POPULAR = 0
        SORT_BY_RECENT = 1
        myCommentText = myYoutubeCommentDownloader.get_comments_from_url(youtube_url, sort_by=SORT_BY_RECENT, language=None, sleep=.1)
        
        # with open(myCommentFilePath, 'r') as file:
            # myCommentText = file.read()
        
        #print("getYTComments: len(myCommentText): ", len(json.dumps(myCommentText) ))
        count=1
        print("getYTComments: ", self.loadNumComments)
        for comment in islice(myCommentText, self.loadNumComments):
            #print(comment)
            #print("Entry: ", count)
            
            
            self.comment_dict.update({count:comment})
            #print("getYTComments: self.comment_dict[count]: ", self.comment_dict[count])
            # print(f"\rLoading... {count*(100/self.loadNumComments) }%", end="")
            #print("\n")
            for item in comment:
                if "time_parsed" in item:
                    #print("item: ", item)
                    #print("str(item): ", str(item))
                    #print("comment["+ item +"]: ", comment[item])
                    displayTime = comment[item]
                
                    #milliseconds = 1678886400000  # Example milliseconds value
                    seconds = int(displayTime) #/ 1000  # Convert milliseconds to seconds
                    datetime_object = datetime.datetime.fromtimestamp(seconds)

                    #print(datetime_object)
                    comment[item] = datetime_object
                
                
            #y = json.loads(comment)

            # the result is a Python dictionary:
            #print(comment["cid"])
            count += 1
        #Cleanup
        print("\n")
        #os.remove(myCommentText)
        self.saveYTComment()
        return self.comment_dict

    def searchYTComments(self, option):
        print_log("Start searchYTComments")
        print("searchYTComments: option: ", option)
        returnList = {}
        
        #print("getYTComments: len(myCommentText): ", len(json.dumps(myCommentText) ))
        print(f"getYTComments: len(myCommentText): {len(self.comment_dict)}")
        count=1
        if "author" in option:
            userSearch = self.entry_for_un_search
        elif "text" in option:
            userSearch = self.entry_for_comment_search
        elif "cid" in option:
            userSearch = self.entry_for_cid_search

        for comment in self.comment_dict:
            # print("searchYTComments: returnList Entry count: ", count)

            if userSearch in self.comment_dict[comment][option]:
                # print(f"searchYTComments: add comment #{comment} to returnList. Entry count: ", count)
                # print("searchYTComments: DownloadSession.comment_dict[comment][\"author\"]: ", self.comment_dict[comment]["author"])
                # print("searchYTComments: DownloadSession.comment_dict[comment]: ", self.comment_dict[comment])
                tempCommentData = {}
                for item in self.comment_dict[comment]:
                    tempCommentData.update({item:self.comment_dict[comment][item]})
                    # pass
                returnList.update({str(count):tempCommentData})
                count += 1
        return returnList

    def countAuthors(self, option="author"):
        print_log("Start countAuthors")
        print("countAuthors: option: ",option)
        authorList={}
        
        #print("countAuthors: len(myCommentText): ", len(json.dumps(myCommentText) ))
        count=1
        for comment in self.comment_dict:
            # print("countAuthors: Entry: "+str(count)+"\n")
            #print("countAuthors: comment: ", comment)
            #print("countAuthors: comment[\"author\"]: ", self.comment_dict[comment]["author"])
            thisAuthor = self.comment_dict[comment]["author"]
            #print("countAuthors: thisAuthor: ",thisAuthor)
            
            if thisAuthor in authorList:
                #print("countAuthors: authorList[]: ",authorList[thisAuthor])
                authorList.update({thisAuthor:authorList[thisAuthor]+1})
            else:
                authorList.update({thisAuthor:1})
                #print("countAuthors: authorList[]: ",authorList[thisAuthor])
        
        #display list
        #for author in authorList:
        #    self.label_for_comments.insert(END, str(author)+" appears: ")
        #    self.label_for_comments.insert(END, str(authorList[author])+"\n")

        #sort list then display
        #sort on value
        returnDict = {}
        countloops = 1

        if "count" in option: #Choose which field to sort on.
            sortBit = 1
            reverseBit = True
        elif "author" in option:
            sortBit = 0
            reverseBit = False
        else:
            sortBit = 1
            reverseBit = True

        #print("countAuthors: Sort list by # of author comments: ")
        #x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
        sorted_x = sorted(authorList.items(), key=operator.itemgetter(sortBit), reverse=reverseBit)

        for x in sorted_x:
            # print( x[0],":", x[1])
            tempCountDict = {"Author":x[0],"# of Comments":x[1]}
            returnDict.update({str(countloops):tempCountDict})
            countloops += 1

        return returnDict
        pass
    # wrapper for sentiment analysis logic
    def getSentiment(self,name):
        return analyze_overall_sentiment(self.entry_for_link,self.loadNumComments)
    def countWords(self, option="alpha"):
        print_log("Start coundWords")

        wordList = {}
        # ------------------myDownloadSession.label_for_comments.delete("1.0", 'end')  # "1.0", "end"

        # print("coundWords: len(myCommentText): ", len(json.dumps(myCommentText) ))
        count = 1
        for comment in self.comment_dict:
            #-------------------myDownloadSession.label_for_comments.insert(END, "Entry: "+str(count)+"\n" )
            # print("coundWords: comment: ", comment)
            # print("coundWords: comment[\"text\"]: ", myDownloadSession.comment_dict[comment]["text"])
            thisText = self.comment_dict[comment]["text"]
            # print("coundWords: thisText: ",thisText)

            thisText = thisText.replace("\n", " ")
            thisText = thisText.replace("\"", "")
            # thisText = thisText.replace("\'", "")
            thisText = thisText.replace("“", "")
            thisText = thisText.replace(".", " ")
            thisText = thisText.replace("!", " ")
            thisText = thisText.lower()
            thisText.split(" ")
            for word in thisText.split(" "):
                # print(f"Word: {word}")
                word = word.strip("\" .,(){}[]")
                # print(f"Word stripped: {word}")

                # ---------------------Check word for special exceptions------------------#
                if len(word) == 0:
                    print(f"Empty word: {word}")
                    # userinput = input("Press Enter to continue...: ")
                    continue
                if len(word) == 1:
                    if word == "&" or word == " " or word == "-" or word == "/" or word == "@":
                        continue

                if "\n" in word:
                    print("Complex entry found")
                    for word in thisText.split("\n"):
                        if word in wordList:
                            # print("coundWords: wordList[]: ",wordList[word])
                            wordList.update({word: wordList[word] + 1})
                        else:
                            wordList.update({word: 1})
                            # print("coundWords: wordList[]: ",wordList[word])
                    userinput = input("Press Enter to continue...: ")
                    continue
                else:
                    pass
                ###########################################################################
                if word in wordList:
                    # print("coundWords: wordList[]: ",wordList[word])
                    wordList.update({word: wordList[word] + 1})
                else:
                    wordList.update({word: 1})
                    # print("coundWords: wordList[]: ",wordList[word])

        # display list
        # for author in authorList:
        #    myDownloadSession.label_for_comments.insert(END, str(author)+" appears: ")
        #    myDownloadSession.label_for_comments.insert(END, str(authorList[author])+"\n")

        # sort list then display
        # sort on value
        returnDict = {}
        countloops = 1

        if "count" in option:  # Choose which field to sort on.
            sortBit = 1
            reverseBit = True
        elif "alpha" in option:
            sortBit = 0
            reverseBit = False
        else:
            sortBit = 1
            reverseBit = True

        # print("coundWords: Sort list by word appearance count: ")
        #-------------------- myDownloadSession.label_for_comments.insert(END, "Sort list by word appearance count:: \n")
        # x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
        sorted_x = sorted(wordList.items(), key=operator.itemgetter(sortBit), reverse=True)

        for x in sorted_x:
            # print( x[0], x[1])
            tempCountDict = {"Word": x[0], "Appears": x[1]}
            returnDict.update({str(countloops): tempCountDict})
            countloops += 1

        return returnDict


def print_log(logMessage):
    time_stamp=datetime.datetime.today()
    print(f"{time_stamp}: {logMessage}")
    return f"{time_stamp}: {logMessage}"