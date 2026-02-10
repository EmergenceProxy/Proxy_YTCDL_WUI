#Hold all the classes that draw different pages with dominate module
import os
from dominate.tags import *
from dominate import document
from dominate.util import text

import sys

# adding Folder_2 to the system path
sys.path.insert(0, '/home/proxyApps/pyCode')
print(f"-----------------os path: {os.getcwd()}")
from prxyYT_CommentDL_Web import DownloadSession
from prxyYT_CommentDL_DynamoDB import DynamoDB_interface

class drawHTML:
##############################-Class Objects-##########################################
    myDownloadSession = DownloadSession()
    videoData = {}
    homeIpAddress = "http://13.58.4.21"
    sentiment_result={}
##############################-Helper Functions-##########################################
    # @staticmethod
    def remove_surrogates(self, mytext):
        encoded_bytes = mytext.encode('utf-16', errors='replace')
                             # text.encode('utf-16', 'surrogateescape', errors='replace')
        # print(f"remove_surrogates: {encoded_bytes}\n")
        encoded_bytes = encoded_bytes.decode('utf-8', 'replace')
        # print(f"remove_surrogates: {encoded_bytes}\n")
        return encoded_bytes

##############################-HTML pages to draw-##########################################
    def getStyle(self):
        return """
                * {
                  box-sizing: border-box;
                }
                body {
                  //background-color: #8f9492;
                  background-color: #679436;
                  background-color:#ccc;
                  font-family: sans-serif;
                  font-size: 24px;
                }
                input {
                    font-size: 20px;
                }
                table, th, td {
                  border: 1px solid black;
                }
                .text_input{
                    width: 50%;
                }
                .text_input_url{
                    width: 75%;
                }
                /* Create three unequal columns that floats next to each other */
                .column {
                  float: left;
                  padding: 10px;
                  //height: 100%;
                  //height: 550px;/* Should be removed. Only for demonstration */
                }

                .left, .right {
                  width: 25%;
                }

                .left{
                    //height: 100%;
                }
                .middle {
                    width: 50%;
                    //height: 100%;
                }

                /* Clear floats after the columns */
                .row:after {
                  content: "";
                  display: table;
                  clear: both;
                }

                /* Responsive layout - makes the three columns stack on top of each other instead of next to each other */
                /*
                @media screen and (max-width: 800px) {
                  .column {
                    width: 100%;
                  }
                }
                */
            """
        pass

    def drawTopNavBar(self, homeIpAddress="http://13.58.4.21", page="main"):

        topNavBarDivStyle = """ 
        background-color:#2A4747; 
        position: absolute;
        height: 88px;
        width: 100%;
        padding: 10;
        border-radius: 4px;
        """
        topNavBarStyle="""
        height: 75px;
        width: 90%;
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: flex-end;
        """

        extratoppings = """
        top: 0;
        left: 0;
        right: 0;
        max-width: 1750px;
        margin-left: auto;
        margin-right: auto; 
        z-index: 4;
        font-size: 16px;
        """

        topNavBarItemStyle = """
        float: left;
        #width: 300px;
        border: 5px green;
        border-style: outset;
        border-width: 10px;
        background-color:#61D095;
        margin: auto;
        flex-grow:1;
        """
        # homeIpAddress = "http://13.58.4.21"

        with div(id="topNavBarDiv", style=topNavBarDivStyle) as TopNavBarDiv:  #style=
            with nav(id="topNavBar", style=topNavBarStyle):
                with a('Home', href=homeIpAddress, style=topNavBarItemStyle):
                    pass
                with a('Reset YT Comment Download', href=f"{homeIpAddress}:5000/proxy/youtube", style=topNavBarItemStyle):
                    pass
                if page == "main":
                    with a('YT Comment Tables', href=f"{homeIpAddress}:5000/proxy/youtube/tables", style=topNavBarItemStyle):
                        pass
                with a('Goto PageTop', href='#page-TOP', style=topNavBarItemStyle, id="page-TOP"):
                    pass
                with a('Goto Page Bottom', href='#page-BOT', style=topNavBarItemStyle):
                    pass

            pass

        return TopNavBarDiv

    def drawFooter(self, homeIpAddress="http://13.58.4.21"):
        with div(id='footerDiv', style="background-color:#E0BAD7;", align="center") as FooterBarDiv:
            # p('-----------------------------I am a footer')
            h1('Hello from Dominate!')
            p(text('This is a page generated using the Dominate library by Kino. '),
              a('>Kino Link<', href='https://github.com/Knio/dominate'))
            p('This page is created to interface as the YoutubeCommentDownloader web GUI.')
            # with p(id="page-BOT"):
            #     a('Goto Page Top', href='#page-TOP')
            # with p():
            #     a('Goto Page Bottom', href='#page-BOT')
            pass
        return FooterBarDiv

    def drawDataEntryColumn(self, username, formDict=None, homeIpAddress="http://13.58.4.21"):
        url_input_value = ""
        # homeIpAddress = "http://13.58.4.21"
        if formDict is not None:
            print("drawDataEntryColumn: pull form values") #Add user input data to page b4 transmit
            url_input_value = formDict["url_input"]
            commentCount_range_value = formDict["commentCount_range"]
            commentCount_input_value = formDict["commentCount_input"]
            un_search_value = formDict["un_search_input"]
            comment_search_value = formDict["comment_search_input"]
            cid_search_value = formDict["cid_search_input"]
            set_displayAll_button_visible = True
            print(f"drawDataEntryColumn: url_input_value: {url_input_value}")
        else:
            print("drawDataEntryColumn: print basic form")
            print(f"drawDataEntryColumn: username: {username}")
            url_input_value = ""
            commentCount_range_value = 100
            commentCount_input_value = 100
            un_search_value = ""
            comment_search_value = ""
            cid_search_value = ""
            set_displayAll_button_visible = False

        with div(id="dataEntryColumn", style="background-color:#C0D6DF;") as dataEntryDiv:#cls="column",
            # Link entry fields
            with form(action=f"{homeIpAddress}:5000/{username}/youtube/view_comments", method="get",
                      name="url_input_form"):
                p('Enter a YouTube link in the box to download comments:')
                input_(type='text', name='url_input', cls="text_input_url", value=url_input_value, required=True)
                p('Number of comments to download:')
                input_(type='range', name='commentCount_range', min="100",max="5000", value=commentCount_range_value, step="100",
                       oninput="this.form.commentCount_input.value=this.value")
                input_(type='number', name='commentCount_input', min="100", max="5000", value=commentCount_input_value,
                       oninput="this.form.commentCount_range.value=this.value")
                input_(type='submit', value="Download", name="url_input_form", title="Click to download comments.")
                input_(type='submit', value="Display All",
                       formaction=f"{homeIpAddress}:5000/{username}/youtube/search_comments_author", method="get",
                       name="display_all_form", title="Click to re-display downloaded comments.", visible=set_displayAll_button_visible)
                hr()
            # Search author field
            # with form(action=f"{homeIpAddress}:5000/{username}/youtube/search_comments_author", method="get",name="search_author_form"):
                p('Search YouTube comment author:')
                input_(type='text', name='un_search_input', value=un_search_value, cls="text_input")
                input_(type='submit', value="Search", formaction=f"{homeIpAddress}:5000/{username}/youtube/search_comments_author", method="get", name="search_author_form")
                hr()
            # Search comment field
            # with form(action=f"{homeIpAddress}:5000/{username}/youtube/search_comments_text", method="get", name="search_comment_form"):
                p('Search YouTube comment text:')
                input_(type='text', name='comment_search_input', value=comment_search_value, cls="text_input")
                input_(type='submit', value="Search", formaction=f"{homeIpAddress}:5000/{username}/youtube/search_comments_text", method="get", name="search_comment_form")
                hr()
            # Search cid field
            # with form(action=f"{homeIpAddress}:5000/{username}/youtube/search_comments_cid", method="get",name="search_cid_form"):
                p('Search base CID for threads:')
                input_(type='text', name='cid_search_input', value=cid_search_value, cls="text_input")
                input_(type='submit', value="Search", formaction=f"{homeIpAddress}:5000/{username}/youtube/search_comments_cid", method="get",name="search_cid_form")
                hr()
            # Data Analysis buttons
            # with form(action=f"{homeIpAddress}:5000/{username}/youtube/sort_comments", method="get", name="count_analysis_form"):
                p('Data Analysis buttons:')
                # button('Count and sort by # of comments', type="submit", onclick="alert(document.getElementById('unEntry').value)")
                input_(type="submit", value='Sentiment Analysis',
                       formaction=f"{homeIpAddress}:5000/{username}/youtube/sentiment_analysis_input", method="get",
                       name='sentiment_analysis_input', title="click to get a sentiment analysis on the comments returned by the tool.")
                input_(type="submit", value='Count and sort by # of comments',
                       formaction=f"{homeIpAddress}:5000/{username}/youtube/sort_most_comments", method="get",
                       name='comment_count_input', title="Click to count comments for each author, and sort by # of comments.")
                input_(type="submit", value='Count # of author comments',
                       formaction=f"{homeIpAddress}:5000/{username}/youtube/sort_author_alpha", method="get",
                       name='author_count_input', title="Click to count comments for each author, and sort Author Alphabetically.")
                input_(type="submit", value='Count # of word occurrences',
                       formaction=f"{homeIpAddress}:5000/{username}/youtube/sort_most_common_words", method="get",
                       name='word_count_input', title="Click to count the occurences of each word, and sort by #.")
                hr()

                # Data Analysis buttons V2: queue implementation
                # with form(action=f"{homeIpAddress}:5000/{username}/youtube/sort_comments", method="get", name="count_analysis_form"):
                # p('Data Analysis buttons(SQS):', title="This set of buttons utilizes the AWS SQS.")
                # # button('Count and sort by # of comments', type="submit", onclick="alert(document.getElementById('unEntry').value)")
                # input_(type="submit", value='Count and sort by # of comments',
                #        formaction=f"https://sqs.us-east-2.amazonaws.com/669773239329/MyYTCDL_Queue", method="post",
                #        name='comment_count_input',
                #        title="Click to count comments for each author, and sort by # of comments.")
                # input_(type="submit", value='Count # of author comments',
                #        formaction=f"https://sqs.us-east-2.amazonaws.com/669773239329/MyYTCDL_Queue", method="post",
                #        name='author_count_input',
                #        title="Click to count comments for each author, and sort Author Alphabetically.")
                # input_(type="submit", value='Count # of word occurrences',
                #        formaction=f"https://sqs.us-east-2.amazonaws.com/669773239329/MyYTCDL_Queue", method="post",
                #        name='word_count_input', title="Click to count the occurences of each word, and sort by #.")

            if formDict is None:
                with p(id="page-BOT"):
                    a('Goto Page Top', href='#page-TOP')
                with p():
                    a('Goto Page Bottom', href='#page-BOT')
        return dataEntryDiv

    def drawDataSentimentColumn(self, isSemantic=False):
        break_long_words_style_ana = f"overflow-wrap: break-word;  word-wrap: break-word;  word-break: break-all;  word-break: break-word;  hyphens: auto;"
        dataDisplayEntryColumnStyle_ana = f"width:8%;"  # overflow-x:auto;"
        print(f"drawDataSentimentColumn: isSemantic: {isSemantic}")
        if (isSemantic):
            with div(id="SentimentAnalysisColumn", style="background-color:#C0D6DF;") as SentimentAnalysisDiv:  # cls="column",
                p('Sentiment Analysis Result:')               
                overall_sentiment = self.sentiment_result["overall_sentiment"]
                summary = self.sentiment_result["summary"]
                with table(style="width: 80%; table-layout: fixed;"):  # style="width: 50%;"
                    with thead():
                        tableHeaderRow = tr()
                        tableHeaderRow.add(td("Overall Sentiment", style=dataDisplayEntryColumnStyle_ana+break_long_words_style_ana))
                        tableHeaderRow.add(td("Summary", style=break_long_words_style_ana))
                    with tbody():
                        tableDataRow = tr()
                        tableDataRow.add(td(overall_sentiment, style=dataDisplayEntryColumnStyle_ana+break_long_words_style_ana))
                        tableDataRow.add(td(summary,style=dataDisplayEntryColumnStyle_ana+break_long_words_style_ana))
            return SentimentAnalysisDiv
    def drawDataDisplayColumn(self, showAllFields = False):
        # showAllFields = False
        setDivWidth = "width: 100%;"

        if showAllFields:
            setDivWidth = "width: 50%;"
        # dataDisplayColumnStyle = f"background-color:#DBE9EE; height: 100%; {setDivWidth}; overflow-x:auto;"
        break_long_words_style = f"overflow-wrap: break-word;  word-wrap: break-word;  word-break: break-all;  word-break: break-word;  hyphens: auto;"
        dataDisplayColumnStyle = f"background-color:#AAFFEE; height: 100%; width: 100%;"# overflow-x:auto;"
        dataDisplayEntryColumnStyle = f"width:8%;"  # overflow-x:auto;"
        dataDisplayCommentColumnStyle = f"width:50%;"  # overflow-x:auto;"
        dataDisplayCidColumnStyle = f"width:20%;"  # word-wrap: break-all;overflow-x:auto;"

        with div(cls="column", id="dataDisplayColumn", style=dataDisplayColumnStyle):  # cls="column middle"
            #
            p('Data Display:')
            with table(style="width: 80%; table-layout: fixed;"):  # style="width: 50%;"
                with thead():
                    tableHeaderRow = tr()
                    print(f"drawDataDisplayColumn: showAllFields: {showAllFields}")
                    if showAllFields:
                        # print(f"-----drawDataDisplayColumn: self.videoData {self.videoData}.")
                        # print(f"-----drawDataDisplayColumn: self.videoData[\"1\"] {self.videoData['1']}.")
                        for headerValue in self.videoData['1'].keys():  # add all fields
                            tableHeaderRow.add(td(headerValue))
                    else:
                        tableHeaderRow.add(td("Entry #", style=dataDisplayEntryColumnStyle+break_long_words_style))
                        tableHeaderRow.add(td("Authors", style=break_long_words_style))
                        tableHeaderRow.add(td("Entry Time", style=break_long_words_style))
                        tableHeaderRow.add(td("Comment", style=dataDisplayCommentColumnStyle))#dataDisplayCommentColumnStyle
                        tableHeaderRow.add(td("Comment ID", style=dataDisplayCidColumnStyle+break_long_words_style))#dataDisplayCidColumnStyle
                    pass
                with tbody():
                    for entry in self.videoData:
                        tableDataRow = tr()
                        comment = self.videoData[entry]
                        # print(f"drawYoutubeDownloader_CommentData: entry: {entry}\n")
                        if showAllFields:
                            for headerValue in comment.keys():
                                # self.videoData["1"]
                                tempData = comment[headerValue]
                                if "text" in headerValue:
                                    tempData = comment[headerValue]
                                    # print("drawYoutubeDownloader_CommentData: text surrogate removal, pre: ",tempData)
                                    tempData = self.remove_surrogates(tempData)
                                    # print(f"drawYoutubeDownloader_CommentData: text surrogate removal, post: {tempData}\n")
                                tableDataRow.add(td(str(tempData)))
                        else:
                            tableDataRow.add(td(entry))
                            tableDataRow.add(td(comment["author"], style=break_long_words_style))
                            tableDataRow.add(td(comment["time"]))

                            tempData = comment["text"]
                            # print("drawYoutubeDownloader_CommentData: text surrogate removal, pre: ",tempData)
                            tempData = self.remove_surrogates(tempData)
                            # print(f"drawYoutubeDownloader_CommentData: text surrogate removal, post: {tempData}\n")
                            tableDataRow.add(td(tempData, style=dataDisplayCommentColumnStyle))#dataDisplayCommentColumnStyle
                            tableDataRow.add(td(comment["cid"], style=dataDisplayCidColumnStyle+break_long_words_style))#dataDisplayCidColumnStyle
                    pass
                with tfoot():
                    tableFooterRow = tr()
                    if showAllFields:
                        for headerValue in self.videoData["1"].keys():  # add all fields
                            tableFooterRow.add(td(headerValue))
                    else:
                        tableFooterRow.add(td("Entry #"))
                        tableFooterRow.add(td("Authors"))
                        tableFooterRow.add(td("Entry Time"))
                        tableFooterRow.add(td("Comment"))
                        tableFooterRow.add(td("Comment ID"))
                    pass

            with p(id="page-BOT"):
                a('Goto Page Top', href='#page-TOP')
            with p():
                a('Goto Page Bottom', href='#page-BOT')
        pass


    # @staticmethod
    def drawYoutubeDownloader(self, name):
        print("Start: drawYoutubeDownloader")
        doc = document(title='YT Comment DownLoader')
        # false = "False"

        with doc.head:
            link(rel='stylesheet', href='login2_style.css')
            script(type='text/javascript', src='script.js')
            style(self.getStyle())

        with doc.body:
            with div(id='header', align="center", style="background-color:#439775;"):
                #p('-----------------------------I am a header')
                self.drawTopNavBar(page="ytcdl")

            with div(id="mainPageDiv", cls="content", align="center",style="background-color:#48BF84;"):#margin-top: 90px;
                p(".")
                p(".")
                # p(" ")

                # data entry Column
                # dataentryDiv +=
                self.drawDataEntryColumn(username=name)

                # data display Column
                showAllFields = False
                setDivWidth = "width: 100%;"

                if showAllFields:
                    setDivWidth = "width: 50%;"
                # dataDisplayColumnStyle = f"background-color:#DBE9EE; height: 100%; {setDivWidth}; overflow-x:auto;"
                # dataDisplayColumnStyle = f"background-color:#DBE9EE; height: 100%; width: 50%; overflow-x:auto;"

            with div(id='footer', style="background-color:#E0BAD7;"):
                self.drawFooter()
                pass


        # print(doc)
        # print(doc.render(pretty=True))
        return doc.render(pretty=True)

    # @staticmethod
    def drawYoutubeDownloader_CommentData(self, username, formDict, showAllFields = False,isSemantic=False):
        print("Start: drawYoutubeDownloader_CommentData")
        doc = document(title='YT Comment DownLoader')

        with doc.head:
            link(rel='stylesheet', href='login2_style.css')
            script(type='text/javascript', src='script.js')
            style(self.getStyle())

        with doc.body:  #731
            with div(id='header', align="center", style="background-color:#439775;"):
                #p('-----------------------------I am a header')
                self.drawTopNavBar()

            with div(id="mainPageDiv", cls="content", align="center",style="background-color:#48BF84;"):#margin-top: 90px;
                p(".")
                p(".")
                p(" ")

                with div(cls="row", style="background-color:#61D095;"):
                    #data entry Column
                    self.drawDataEntryColumn(username, formDict)
                    print(f"drawYoutubeDownloader_CommentData: isSemantic: {isSemantic}")
                    self.drawDataSentimentColumn(isSemantic)
                    #data display Column
                    print(f"drawYoutubeDownloader_CommentData: showAllFields: {showAllFields}")
                    self.drawDataDisplayColumn(showAllFields)

            with div(id='footer', style="background-color:#E0BAD7;"):
                #p('-----------------------------I am a footer')
                h1('Hello from Dominate!')
                p(text('This is a page generated using the Dominate library by Kino. '),
                    a('>Kino Link<', href='https://github.com/Knio/dominate'))
                p('This page is created to interface as the YoutubeCommentDownloader web GUI.')
                # with p(id="page-BOT"):
                #     a('Goto Page Top', href='#page-TOP')
                # with p():
                #     a('Goto Page Bottom', href='#page-BOT')
                pass

        # print(doc)
        # print(doc.render(pretty=True))
        return doc.render(pretty=True)

    def drawTableSelectColumn(self, username):
        # global homeIpAddress
        commentCount_range_value = 100
        commentCount_input_value = 100
        set_displayAll_button_visible = True

        url_input_value = ""
        with div(id="tableSelectColumn", style="background-color:#C0D6DF;") as dataEntryDiv:  # cls="column",
            # Link entry fields
            with form(action=f"{self.homeIpAddress}:5000/{username}/youtube/tables", method="get",
                      name="url_input_form"):
                p('Select a table to view:')
                with select(id='table-select-dropdown', name='table_select_input'):
                    # Add option tags
                    option('User Table', value='user_table', selected='selected') # Pre-selected
                    option('Comment Table', value='comment_table')
                    option('Video Table', value='video_table')
                    option('User Table 2', value='userX_table')
                p('Search for a table:')
                input_(type='text', name='table_search_input', cls="text_input_url", value=url_input_value)  #, required=True
                p('Number of entries to load:')
                input_(type='range', name='commentCount_range', min="100", max="5000", value=commentCount_range_value,
                       step="100",
                       oninput="this.form.commentCount_input.value=this.value")
                input_(type='number', name='commentCount_input', min="100", max="5000", value=commentCount_input_value,
                       oninput="this.form.commentCount_range.value=this.value")
                input_(type='submit', value="Download", name="url_input_form", title="Click to download entries.")
                input_(type='submit', value="Display All",
                       formaction=f"{self.homeIpAddress}:5000/{username}/youtube/tables", method="get",
                       name="display_all_form", title="Click to re-display downloaded comments.",
                       visible=set_displayAll_button_visible)

                # p('Data Analysis buttons:')
                # # button('Count and sort by # of comments', type="submit", onclick="alert(document.getElementById('unEntry').value)")
                # input_(type="submit", value='Count and sort by # of comments',
                #        formaction=f"{homeIpAddress}:5000/{username}/youtube/tables", method="get",
                #        name='comment_count_input',
                #        title="Click to count comments for each author, and sort by # of comments.")
                # input_(type="submit", value='Count # of author comments',
                #        formaction=f"{homeIpAddress}:5000/{username}/youtube/tables", method="get",
                #        name='author_count_input',
                #        title="Click to count comments for each author, and sort Author Alphabetically.")
                # input_(type="submit", value='Count # of word occurrences',
                #        formaction=f"{homeIpAddress}:5000/{username}/youtube/tables", method="get",
                #        name='word_count_input', title="Click to count the occurences of each word, and sort by #.")
        pass

    def drawDynamoTableColumn(self, formDict):
        print("Start: drawDynamoTableColumn")
        if formDict is not None:
            print("drawDynamoTableColumn: pull form values")  # Add user input data to page b4 transmit
            table_select_input_value = formDict["table_select_input"]
            table_search_input_value = formDict["table_search_input"]
            commentCount_range_value = formDict["commentCount_range"]
            commentCount_input_value = formDict["commentCount_input"]
            set_displayAll_button_visible = True
            print(f"drawDynamoTableColumn: url_input_value: {table_select_input_value}")
            print(f"drawDynamoTableColumn: table_search_input_value: {table_search_input_value}")
            print(f"drawDynamoTableColumn: commentCount_range_value: {commentCount_range_value}")
            print(f"drawDynamoTableColumn: commentCount_input_value: {commentCount_input_value}")
        else:
            print("drawDynamoTableColumn: print basic form")
            table_select_input_value = "user_table"
            table_search_input_value = "user_table"
            commentCount_range_value = 100
            commentCount_input_value = 100
            set_displayAll_button_visible = False


        my_table_name = "video_table"  # Replace with your DynamoDB table name
        my_table_name = "comment_table"  # Replace with your DynamoDB table name
        my_table_name = table_select_input_value
        my_table_name = "user_table"  # Replace with your DynamoDB table name
        my_region_name = "us-east-2"  # Replace with your DynamoDB table name
        myDynamoDB_interface = DynamoDB_interface(my_table_name, my_region_name)
        showAllFields = False

        break_long_words_style = f"overflow-wrap: break-word;  word-wrap: break-word;  word-break: break-all;  word-break: break-word;  hyphens: auto;"
        dataDisplayColumnStyle = f"background-color:#AAFFEE; height: 100%; width: 100%;"  # overflow-x:auto;"
        dataDisplayEntryColumnStyle = f"width:8%;"  # overflow-x:auto;"
        dataDisplayCommentColumnStyle = f"width:50%;"  # overflow-x:auto;"
        dataDisplayCidColumnStyle = f"width:20%;"  # word-wrap: break-all;overflow-x:auto;"

        #get_all_table_items test
        #table_items = myDynamoDB_interface.get_all_table_items()
        table_items = myDynamoDB_interface.get_x_table_items(commentCount_range_value)
        print(f"drawDynamoTableColumn: Retrieved {len(table_items)} items from {myDynamoDB_interface.table_name}.")

        count = 0
        # for item in table_items:
        #     #print(f"Main: item: {item}")
        #     #print(f"Main: item.keys: {item.keys()}")
        #     print(f"Main: item['artist'] {item['artist']}")
        #     print(f"Main: item['song'] {item['song']}")
        #     #print(f"Main: item['form'].keys() {item['form'].keys()}")
        #     pass

        with div(cls="column", id="dataDisplayColumn", style=dataDisplayColumnStyle):  # cls="column middle"
            #
            p('Data Display:')
            with table(style="width: 80%; table-layout: fixed;"):  # style="width: 50%;"
                with thead():
                    tableHeaderRow = tr()
                    if showAllFields:
                        # print(f"-----drawDynamoTableColumn: table_items {table_items}.")
                        # print(f"-----drawDynamoTableColumn: table_items[\"1\"] {table_items[1]}.")
                        tableHeaderRow.add(td("Entry #", style=dataDisplayEntryColumnStyle + break_long_words_style))
                        for headerValue in table_items[0].keys():  # add all fields
                            tableHeaderRow.add(td(headerValue))
                    else:
                        if "comment_table" in my_table_name:
                            tableHeaderRow.add(td("Entry #", style=dataDisplayEntryColumnStyle + break_long_words_style))
                            tableHeaderRow.add(td("Authors", style=break_long_words_style))
                            tableHeaderRow.add(td("Entry Time", style=break_long_words_style))
                            tableHeaderRow.add(td("Comment", style=dataDisplayCommentColumnStyle))  # dataDisplayCommentColumnStyle
                            tableHeaderRow.add(td("Comment ID", style=dataDisplayCidColumnStyle + break_long_words_style))  # dataDisplayCidColumnStyle
                        else: #default to #"user_table" in my_table_name:
                            tableHeaderRow.add(td("Entry #", style=dataDisplayEntryColumnStyle + break_long_words_style))
                            tableHeaderRow.add(td("user_id", style=dataDisplayEntryColumnStyle))
                            tableHeaderRow.add(
                                td("comment_count", style=dataDisplayEntryColumnStyle))
                            tableHeaderRow.add(td("video_id_list", style=break_long_words_style))
                            tableHeaderRow.add(td("channel", style=break_long_words_style))
                    pass
                with tbody():
                    entryCount = 1
                    for entry in table_items:
                        tableDataRow = tr()
                        comment = entry #table_items[entry]
                        #print(f"drawDynamoTableColumn: entry: {entry}\n")
                        if showAllFields:
                            for headerValue in comment.keys():
                                # table_items[1]
                                tempData = comment[headerValue]
                                if "text" in headerValue:
                                    tempData = comment[headerValue]
                                    # print("drawYoutubeDownloader_CommentData: text surrogate removal, pre: ",tempData)
                                    tempData = self.remove_surrogates(tempData)
                                    # print(f"drawYoutubeDownloader_CommentData: text surrogate removal, post: {tempData}\n")
                                tableDataRow.add(td(str(tempData)))
                        else:
                            if "comment_table" in my_table_name:
                                tableDataRow.add(td(entryCount))
                                tableDataRow.add(td(comment["author"], style=break_long_words_style))
                                tableDataRow.add(td(comment["time"]))

                                tempData = comment["text"]
                                # print("drawYoutubeDownloader_CommentData: text surrogate removal, pre: ",tempData)
                                tempData = self.remove_surrogates(tempData)
                                # print(f"drawYoutubeDownloader_CommentData: text surrogate removal, post: {tempData}\n")
                                tableDataRow.add(
                                    td(tempData, style=dataDisplayCommentColumnStyle))  # dataDisplayCommentColumnStyle
                                tableDataRow.add(td(comment["cid"],
                                                    style=dataDisplayCidColumnStyle + break_long_words_style))  # dataDisplayCidColumnStyle
                            else: #default to user_table
                                tableDataRow.add(td(entryCount))
                                tableDataRow.add(td(comment["user_id"], style=dataDisplayCidColumnStyle))
                                tableDataRow.add(td(comment["comment_count"]))
                                tableDataRow.add(td(comment["video_id_list"]))
                                tableDataRow.add(td(comment["channel"], style=dataDisplayCidColumnStyle))
                            entryCount += 1
                    pass
                with tfoot():
                    tableFooterRow = tr()
                    if showAllFields:
                        for headerValue in table_items[0]:  # add all fields
                            tableFooterRow.add(td(headerValue))
                    else:
                        if "comment_table" in my_table_name:
                            tableFooterRow.add(td("Entry #", style=dataDisplayEntryColumnStyle + break_long_words_style))
                            tableFooterRow.add(td("Authors", style=break_long_words_style))
                            tableFooterRow.add(td("Entry Time", style=break_long_words_style))
                            tableFooterRow.add(td("Comment", style=dataDisplayCommentColumnStyle))  # dataDisplayCommentColumnStyle
                            tableFooterRow.add(td("Comment ID", style=dataDisplayCidColumnStyle + break_long_words_style))  # dataDisplayCidColumnStyle
                        else: #default to user_table
                            tableFooterRow.add(td("Entry #", style=dataDisplayEntryColumnStyle + break_long_words_style))
                            tableFooterRow.add(td("user_id", style=dataDisplayEntryColumnStyle))
                            tableFooterRow.add(
                                td("comment_count", style=dataDisplayEntryColumnStyle))
                            tableFooterRow.add(td("video_id_list", style=break_long_words_style))
                            tableFooterRow.add(td("channel", style=break_long_words_style))
                    pass

            with p(id="page-BOT"):
                a('Goto Page Top', href='#page-TOP')
            with p():
                a('Goto Page Bottom', href='#page-BOT')

    def drawYoutubeTables(self, name, formDict=None):
        print("Start: drawYoutubeTables")
        doc = document(title='YT Comment DownLoader')
        # false = "False"

        with doc.head:
            link(rel='stylesheet', href='login2_style.css')
            script(type='text/javascript', src='script.js')
            style(self.getStyle())

        with doc.body:
            with div(id='header', align="center", style="background-color:#439775;"):
                # p('-----------------------------I am a header')
                self.drawTopNavBar()

            with div(id="mainPageDiv", cls="content", align="center",
                     style="background-color:#48BF84;"):  # margin-top: 90px;
                p(".")
                p(".")
                # p(" ")

                # data entry Column
                # dataentryDiv +=
                self.drawTableSelectColumn(username=name)
                self.drawDynamoTableColumn(formDict)

                # data display Column
                showAllFields = False
                setDivWidth = "width: 100%;"

                if showAllFields:
                    setDivWidth = "width: 50%;"
                # dataDisplayColumnStyle = f"background-color:#DBE9EE; height: 100%; {setDivWidth}; overflow-x:auto;"
                # dataDisplayColumnStyle = f"background-color:#DBE9EE; height: 100%; width: 50%; overflow-x:auto;"

            with div(id='footer', style="background-color:#E0BAD7;"):
                self.drawFooter()
                pass

        # print(doc)
        # print(doc.render(pretty=True))
        return doc.render(pretty=True)

    # @staticmethod
    def drawPWTool(self):
        doc = document(title='My Dominate Example')

        with doc.head:
            link(rel='stylesheet', href='login2_style.css')
            script(type='text/javascript', src='script.js')
            style("""
                body {
                  background-color: #f0f0f0;
                  font-family: sans-serif;
                }
                """)

        with doc:
            h1('Hello from Dominate!')
            p(text('This is a page generated using the Dominate library by Kino. '), a('>Kino Link<', href='https://github.com/Knio/dominate'))
            ul(li('Item 1'), li('Item 2'), li('Item 3'))

        print(doc.render(pretty=True))
        return doc.render(pretty=True)#Hold all the classes that draw different pages with dominate module

##############################-HTML Selector-#####################################
    def draw_url_input_form(self, name, formDict):
        print("Start: draw_url_input_form")
        print(f"selectPainting: form: {formDict}")
        return self.drawYoutubeDownloader_CommentData(name, formDict)
        pass

    # def draw_search_author_form(self,  name, formDict):
    #     print("Start: draw_search_author_form")
    #     print(f"selectPainting: form: {form}")
    #     pass
    #
    # def draw_search_comment_form(self,  name, formDict):
    #     print("Start: draw_search_comment_form")
    #     print(f"selectPainting: form: {formDict}")
    #     pass
    #
    # def draw_search_cid_form(self,  name, formDict):
    #     print("Start: draw_search_cid_form")
    #     print(f"selectPainting: form: {formDict}")
    #     pass

    def draw_search_form(self,  name, formDict):
        print("Start: draw_search_form")
        print(f"selectPainting: form: {formDict}")
        return self.drawYoutubeDownloader_CommentData(name, formDict, showAllFields=False)
        pass
    def draw_sentament_analysis_data(self, name, formDict):
        print("Start: sentiment_analysis_input")
        print(f"selectPainting: form: {formDict}")
        return self.drawYoutubeDownloader_CommentData(name, formDict, showAllFields = False,isSemantic=True)
       
    def draw_count_analysis_form(self, name, formDict):
        print("Start: draw_count_analysis_form")
        print(f"selectPainting: form: {formDict}")
        return self.drawYoutubeDownloader_CommentData(name, formDict, showAllFields = True)
        pass

    def selectPainting(self, name, request):
        print(f"selectPainting: Start")
        # print(f"selectPainting: request.name: {request.name}")
        print(f"selectPainting: request.args: {request.args}")
        # request.args.get('operator')
        # print(f"selectPainting: request.form: {request.form}")
        print(f"selectPainting: request.args.get('url_input'): {request.args.get('url_input')}")
        formDict = {}

        # for headerValue in request.keys():#add all fields
        # tableHeaderRow.add(td(headerValue))
        for key, value in request.args.items():
            # params.append(f'{key}: {value}')
            print(f"selectPainting: {key}: {value}")
            formDict[key] = value

        global myDownloadSession
        myDownloadSession = DownloadSession(formDict)
        print(f"selectPainting: myDownloadSession: after")
        print(f"selectPainting: myDownloadSession: {myDownloadSession.loadNumComments}")       
        if 'url_input_form' in request.args:
            print(f"selectPainting: found url_input_form:")
            self.videoData = myDownloadSession.getYTComments()
            # self.videoData = myDownloadSession.loadVideoComments(name) #Implement comment loading logic
            return self.draw_url_input_form(name, formDict)
        elif "search_author_form" in request.args:
            print(f"selectPainting: found search_author_form:")
            # self.videoData = myDownloadSession.getYTComments()
            self.videoData = myDownloadSession.loadVideoComments(name)  # Implement comment loading logic
            self.videoData = myDownloadSession.searchYTComments("author")
            # self.videoData = myDownloadSession.loadVideoComments() #Implement comment loading logic
            return self.draw_search_form(name, formDict)
            # return self.draw_search_author_form(formDict)
        elif "display_all_form" in request.args:
            print(f"selectPainting: found display_all_form:")
            # self.videoData = myDownloadSession.getYTComments()
            self.videoData = myDownloadSession.loadVideoComments(name)  # Implement comment loading logic
            self.videoData = myDownloadSession.searchYTComments("author")
            # self.videoData = myDownloadSession.loadVideoComments() #Implement comment loading logic
            un_search_value = formDict["un_search_input"]
            print(f"selectPainting: display_all_form: will delete un_search_value {un_search_value}")
            formDict["un_search_input"] = ""
            return self.draw_search_form(name, formDict)
            # return self.draw_search_author_form(formDict)
        elif "search_comment_form" in request.args:
            print(f"selectPainting: found search_comment_form:")
            # self.videoData = myDownloadSession.getYTComments()
            self.videoData = myDownloadSession.loadVideoComments(name)
            self.videoData = myDownloadSession.searchYTComments("text")
            # self.videoData = myDownloadSession.loadVideoComments() #Implement comment loading logic
            return self.draw_search_form(name, formDict)
            # return self.draw_search_comment_form(formDict)
        elif "search_cid_form" in request.args:
            print(f"selectPainting: found search_cid_form:")
            # self.videoData = myDownloadSession.getYTComments()
            self.videoData = myDownloadSession.loadVideoComments(name)
            self.videoData = myDownloadSession.searchYTComments("cid")
            # self.videoData = myDownloadSession.loadVideoComments() #Implement comment loading logic
            return self.draw_search_form(name, formDict)
            # return self.draw_search_cid_form(formDict)
        elif "comment_count_input" in request.args:
            print(f"selectPainting: found comment_count_input:")
            # self.videoData = myDownloadSession.getYTComments()
            self.videoData = myDownloadSession.loadVideoComments(name)
            self.videoData = myDownloadSession.countAuthors("count")
            # self.videoData = myDownloadSession.loadVideoComments() #Implement comment loading logic
            # return self.draw_url_input_form(name, formDict)
            return self.draw_count_analysis_form(name, formDict)
        elif "author_count_input" in request.args:
            print(f"selectPainting: found author_count_input:")
            # self.videoData = myDownloadSession.getYTComments()
            self.videoData = myDownloadSession.loadVideoComments(name)
            self.videoData = myDownloadSession.countAuthors("author")
            # self.videoData = myDownloadSession.loadVideoComments() #Implement comment loading logic
            # return self.draw_url_input_form(name, formDict)
            return self.draw_count_analysis_form(name, formDict)
        elif "word_count_input" in request.args:
            print(f"selectPainting: found author_count_input:")
            # self.videoData = myDownloadSession.getYTComments()
            self.videoData = myDownloadSession.loadVideoComments(name)
            self.videoData = myDownloadSession.countWords("count")
            return self.draw_count_analysis_form(name, formDict)
        elif "sentiment_analysis_input" in request.args:
            print(f"selectPainting: found sentiment_analysis_input:")
            # self.videoData = myDownloadSession.getYTComments()
            self.videoData = myDownloadSession.loadVideoComments(name)
            self.sentiment_result = myDownloadSession.getSentiment(name)
            return self.draw_sentament_analysis_data(name, formDict)
        #TODO add input from button to go to generate sentiment analysis
        else:
            return self.drawYoutubeDownloader(name)


        # drawYoutubeDownloader(self, name)

        doc = h1("404")
        return doc
        pass

