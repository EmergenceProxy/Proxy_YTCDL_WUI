#This class will be called every hour. it will:
#1. Search the "ytc/data" folder for files.
#   Pull the videoid from the file name.
#   Search for that videoid in the videos table.
#   If found: compare comments for video in comment table.
#   else: add video to video table. add comments to comment table.
#   Update user table.
#   Run:"python prxyYT_CommentDL_DynamoDB_Scheduler 'check_files' '' "
#2. If no new files found, pull videos from relevantChannelsList.
#N1. Search the queue?

#import boto3
import os
import sys #for file handling
import json #for file handling
import datetime #For logging
import prxyYT_CommentDL_Schema
from prxyYT_CommentDL_DynamoDB import DynamoDB_interface 


class DynamoDB_Scheduler:
    # Class attribute
    species = "Canis familiaris"

    def __init__(self, table_name="fromStore", region_name='us-east-2'):
        # Instance attributes
        self.table_name = table_name
        self.region_name = region_name
        #self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)

    #Test methods
    def getFileList(self, filePath="/home/proxyApps/appData/ytcData"):
        print_log("getFileList: Start")
        #print_log(f"loadVideoComments: myFile: {3333}")
        print_log("getFileList: filePath: "+filePath)
        #print_log(f"getFileList: filePath: {filePath}")
        
        try:
            if os.path.exists(filePath):
                contents_of_target = os.listdir(filePath)
                print_log(f"getFileList: Contents of '{filePath}': {contents_of_target}")
            else:
                print_log(f"getFileList: Directory '{filePath}' does not exist.") 
        except Exception as e:
            print_log("getFileList: Error pulling file list:", e)
        return contents_of_target    
        
    def updateRecords(self, my_file_list):
        print_log("updateRecords: Start")
        filePath="/home/proxyApps/appData/ytcData/"
        try:
            for file in my_file_list:
                returnDict = {}
                with open(filePath+file, 'r+') as myFile:
                    if myFile:
                        # File was selected, you can now work with the file_path
                        print_log(f"updateRecords: myFile: {myFile}")
                        print_log(f"updateRecords: myFile.name: {myFile.name}")

                        try:
                            returnDict = json.load(myFile)
                            aKeyList = list(returnDict.keys())
                            #print_log(f"updateRecords: myFile.name.keyList: {aKeyList}")
                            #print_log(f"updateRecords: returnDict[2]: {returnDict['2']}")
                        except json.decoder.JSONDecodeError as err:
                            print_log(f"updateRecords: jsonDecodeError: {err}")
                            myFile.seek(0)
                            json.dump(self.comment_dict, myFile, indent=4, default=str)
                            myFile.truncate()
                            print_log(f"updateRecords: jsonDecodeError resolved!")
                        else:
                            print_log(f"updateRecords: fileData loaded")
                            
                self.updateTables(myFile.name, returnDict)
        except Exception as e:
            print_log("updateRecords: Error updating item:", e)
        return returnDict  
        
    def updateTables(self, myFilename, recordsDict):
        print_log(f"updateTables: Start")
        userDict = {}
        dict_ex_entry = {
                    "author":
                        {
                            "channel":"XXXXXXXXXXXXXX",
                            "comment_count":3, 
                            "video_id_list":[1,2,3]
                        }
                    }
        
        myVideoID = myFilename[myFilename.rfind("/")+1:myFilename.rfind('_')]
        print_log(f"updateTables: myVideoID: {myVideoID}")
        #myVideo.channel = ""
        
        my_region_name = "us-east-2"
        my_comment_table_interface = DynamoDB_interface("comment_table", my_region_name)
        
        count = 1
        for recordKey in recordsDict:
            record = recordsDict[recordKey]
            print_log(f"updateTables: record ({count}/{len(recordsDict)}): {record}")
            
            print_log(f"updateTables: record['cid']: {record['cid']}")
            
            item = {
                "video_id":myVideoID,
                "comment_id":record['cid'],
                "text":record['text'],
                "time":record['time'],
                "author":record['author'],
                "channel":record['channel'],
                "votes":record['votes'],
                "replies":record['replies'],
                "photo":record['photo'],
                "heart":record['heart'],
                "reply":record['reply'],
                "time_parsed":record['time_parsed']
            }
            
            #my_comment_table_interface.add_table_elm(item) #comment out to speed up user testing 10/6
            
            if record['author'] in userDict:
                print_log(f"updateTables: userDict[record['author']]: {userDict[record['author']]}")
                if myVideoID in userDict[record['author']]["video_id_list"]:
                    pass
                else:
                    userDict[record['author']]["video_id_list"].append(myVideoID)
                    userDict[record['author']]["comment_count"] = len( userDict[record['author']]["video_id_list"] )
            else:
                tempDict = {
                    record['author']:
                        {
                            "channel":record['channel'],
                            "comment_count":1, 
                            "video_id_list":[myVideoID]
                        }
                    }
                userDict.update( tempDict)
                pass
            if count > 3:
                pass
                #break
            count += 1
            print_log("----------------------------------------------------------")
        
        my_user_table_interface = DynamoDB_interface("user_table", my_region_name)
        print_log(f"updateTables: Start user_table updates")
        
        count = 1
        for user in userDict:
            print_log(f"updateTables: user({count}/{len(userDict)}): {user}")
            if len(user) < 1:
                print_log(f"updateTables: author empty")
                user = userDict[user]['channel']
                continue
            
            pk = "user_id"
            sk = "channel"
            pk_value = user
            sk_value = userDict[user]['channel']
            userDBreturn = my_user_table_interface.get_table_elm(pk, sk, pk_value, sk_value)
            print_log(f"updateTables: userDBreturn: {userDBreturn}")
            if userDBreturn:
                print_log(f"updateTables: userDBreturn['user_id']: {userDBreturn['user_id']}")
                for entry in userDBreturn:
                    print_log(f"updateTables: entry: {entry}")
                if myVideoID in userDBreturn['video_id_list']:
                    print_log(f"updateTables: video in list")
                    print_log(f"updateTables: userDBreturn[entry]['video_id_list']: {userDBreturn['video_id_list']}")
                    pass
                else:
                    print_log(f"updateTables: video NOT in list")
                    userDBreturn['video_id_list'].append(myVideoID)
                    userDBreturn['comment_count'] = len( userDBreturn['video_id_list'] )
                    
                    item = {
                        "user_id":userDBreturn['user_id'],
                        "channel":userDBreturn['channel'],
                        "comment_count":userDBreturn['comment_count'], 
                        "video_id_list":userDBreturn['video_id_list']
                    }
                    response = my_user_table_interface.add_table_elm(item)
                pass
            else:
                #random_6_digit_number = random.randint(100000, 999999)
                #print_log(random_6_digit_number)
                item = {
                    "user_id":user,
                    "channel":userDict[user]['channel'],
                    "comment_count":userDict[user]['comment_count'], 
                    "video_id_list":userDict[user]['video_id_list']
                }
                response = my_user_table_interface.add_table_elm(item)
            if count > 3:
                pass
                #break
            count += 1
            print_log("----------------------------------------------------------")
        pass
            
            
            
###############################################################################
def print_log(logMessage):
    time_stamp=datetime.datetime.today()
    print(f"{time_stamp}: {logMessage}")
    return f"{time_stamp}: {logMessage}"

    
if __name__ == "__main__":
    print_log(f"Script name: {sys.argv[0]}")
    if len(sys.argv) > 1:
        print_log("Arguments:")
        for i, arg in enumerate(sys.argv[1:]):
            print_log(f"  Argument {i+1}: {arg}")
        runMode = sys.argv[1]
        if len(sys.argv) > 2:
            workingDir = sys.argv[2]
    else:
        print_log("No arguments provided.")
        
    if "check_files" in runMode:
        my_DDB_scheduler = DynamoDB_Scheduler()
        my_file_list = my_DDB_scheduler.getFileList()
        my_record_list = my_DDB_scheduler.updateRecords(my_file_list)
        
    