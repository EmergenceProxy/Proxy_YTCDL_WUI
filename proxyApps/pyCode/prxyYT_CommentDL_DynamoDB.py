# Class to interface with DynamoDB tables for the YTCDL web interface
# Run:"python prxyYT_CommentDL_DynamoDB.py "setup_files""
import boto3
import json
import sys


class DynamoDB_interface:
    # Class attribute
    species = "Canis_familiaris"

    def __init__(self, table_name="fromStore", region_name='us-east-2'):
        # Instance attributes
        self.table_name = table_name
        self.region_name = region_name
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)

    #Test methods
    def createSongTable(self):
        print("createSongTable: Start")
        #dynamodb = boto3.resource('dynamodb')
        try:
            response = self.dynamodb.create_table(
                TableName=self.table_name, #"basicSongsTable",
                AttributeDefinitions=[
                    {
                        "AttributeName": "artist",
                        "AttributeType": "S"
                    },
                    {
                        "AttributeName": "song",
                        "AttributeType": "S"
                    }
                ],
                KeySchema=[
                    {
                        "AttributeName": "artist",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "song",
                        "KeyType": "RANGE"
                    }
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1
                }
            )
        except Exception as e:
            print("createSongTable: Error deleting item:", e)
        #except botocore.errorfactory.ResourceInUseException as riue:
        #    print("createSongTable: Table exist: riue: ", riue)
        else:
            print(f"createSongTable: successful.")
            print(f"createSongTable: {response}")
        #return f"{self.name} says woof!"
    
    def upload(self):
        print("upload: Start")
        with open('song_data.json', 'r') as datafile:
            records = json.load(datafile)
        
        print(f"upload: len(records): {len(records)}")
        #records.update(userItem)
        
        count = 1
        try: 
            for song in records:
                print(f"upload: song({count}/{len(records)}): {song}")
                print(f"upload: song['artist']: {song['artist']}")
                print(f"upload: song['song']: {song['song']}")
                
                item = {
                        'artist':song['artist'],
                        'song':song['song'],
                        'id':int(song['id']),
                        'song_rating':song['song_rating'],
                        'publisher':song['publisher']
                }
                #print("upload: item", item)
                table = self.dynamodb.Table(self.table_name)
                response = table.put_item( 
                    Item=item
                )
                print(f"upload: UPLOADING ITEM")
                #print(f"upload: response: {response}")
                print(f"upload: response[HTTPStatusCode]: {response['ResponseMetadata']['HTTPStatusCode']}")
                print(f"-------------------------------------------------")
                count += 1
                if count > 30:
                    break
        except Exception as e:
            print("upload: Error with put_item:", e)
        #return self.age * 7
    
  ################################  #End Test Methods  ###################################################################
        
##########################Setup methods#############################
#setup DB tables: {video, comment, user}
    def createTable(self, pk="primaryKey", sk="sortKey", pkt="HASH", skt="RANGE"):
        print("createTable: Start")
        #dynamodb = boto3.resource('dynamodb')
        try:
            response = self.dynamodb.create_table(
                TableName=self.table_name, #"basicSongsTable",
                AttributeDefinitions=[
                    {
                        "AttributeName": pk,
                        "AttributeType": "S"
                    },
                    {
                        "AttributeName": sk,
                        "AttributeType": "S"
                    }
                ],
                KeySchema=[
                    {
                        "AttributeName": pk,
                        "KeyType": pkt
                    },
                    {
                        "AttributeName": sk,
                        "KeyType": skt
                    }
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1
                }
            )
        except Exception as e:
            print("createTable: Error:", e)
        #except botocore.errorfactory.ResourceInUseException as riue:
        #    print("createTable: Table exist: riue: ", riue)
        else:
            print(f"createTable: successful.")
            print(f"createTable: {response}")
        #return f"{self.name} says woof!"

    def add_table_elm(self, userItem):
        print(f"add_table_elm: ", userItem)
        table = self.dynamodb.Table(self.table_name)
        response = table.put_item(
            TableName=self.table_name, #'basicSongsTable', 
            Item=userItem
        )
        print(f"add_table_elm: UPLOADING ITEM")
        print(f"add_table_elm: {response}")
        #return self.age * 7
    
    def get_table_elm(self, pk, sk, pk_value, sk_value):
        # Use the DynamoDB client get item method to get a single item
        try: 
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(
                TableName=self.table_name, #TABLE_NAME,
                Key={
                    pk: pk_value,
                    sk: sk_value
                }
            )
            print(f"get_table_elm: response: {response}")
            if 'Item' in response:
                item = response['Item']
                print("get_table_elm: Retrieved item:", item)
                return item
            else:
                print("get_table_elm: Item not found.")
                return False
            print(f"get_table_elm: response['Item']: {response['Item']}")
        except Exception as e:
            print("get_table_elm: Error getting item:", e)
        # The client's response looks like this:
        # {
        #  'artist': {'S': 'Arturus Ardvarkian'},
        #  'id': {'S': 'dbea9bd8-fe1f-478a-a98a-5b46d481cf57'},
        #  'priceUsdCents': {'S': '161'},
        #  'publisher': {'S': 'MUSICMAN INC'},
        #  'song': {'S': 'Carrot Eton'}
        # }
        return response
        
    def remove_table_elm(self, del_value):
        print(f"Start remove_table_elm")
        print(f"remove_table_elm: {del_value}")
        
        #dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        table = self.dynamodb.Table(self.table_name)
        
        # Define the key of the item to delete
        key_to_delete = {
            'PK': 'form',
            'SK': f'{del_value}' # Include if your table has a sort key
        }

        try:
            response = table.delete_item(
                Key=key_to_delete
            )
            print("remove_table_elm: Item deleted successfully: ", response)
        except Exception as e:
            print("remove_table_elm: Error deleting item:", e)
        
    def get_all_table_items(self):
        """
        Retrieves all items from a DynamoDB table using the scan operation with pagination.

        Args:
            table_name (str): The name of the DynamoDB table.

        Returns:
            list: A list containing all items from the table.
        """
        #dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        table = self.dynamodb.Table(self.table_name)

        all_items = []
        response = table.scan()
        all_items.extend(response['Items'])

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            all_items.extend(response['Items'])

        return all_items

    def get_x_table_items(self, x=100):
        """
        Retrieves all items from a DynamoDB table using the scan operation with pagination.

        Args:
            table_name (str): The name of the DynamoDB table.

        Returns:
            list: A list containing all items from the table.
        """
        #dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        table = self.dynamodb.Table(self.table_name)

        all_items = []
        response = table.scan()
        all_items.extend(response['Items'])

        pageCount = 0
        respCOunt = response['Count']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])

            print(f"get_all_table_items: pageCount: {pageCount}")
            print(f"get_all_table_items: len response: {len(response['Items'])}")
            print(f"get_all_table_items: len all_items: {len(all_items)}")

            all_items.extend(response['Items'])
            if len(all_items) >= x:
                break

        return all_items
###############################################################################
# Example usage:


def setup():#my_region_name=""
    #setup DB tables: {video, comment, user}
    my_region_name = "us-east-2"
    my_video_table_interface = DynamoDB_interface("video_table", my_region_name)
    my_comment_table_interface = DynamoDB_interface("comment_table", my_region_name)
    my_user_table_interface = DynamoDB_interface("user_table", my_region_name)
    
    my_video_table_interface.createTable(pk="channel", sk="video_id", pkt="HASH", skt="RANGE")
    my_comment_table_interface.createTable(pk="video_id", sk="comment_id", pkt="HASH", skt="RANGE")
    my_user_table_interface.createTable(pk="user_id", sk="channel",  pkt="HASH", skt="RANGE")
    
def test_DB():
    #my_table_name = "fromStore"  # Replace with your DynamoDB table name
    #my_region_name = "us-east-1"  # Replace with your DynamoDB table name
    #my_DDB_interface = DynamoDB_interface(my_table_name, my_region_name)
   
    #Create tables test
    my_table_name = "basicSongsTable"  # Replace with your DynamoDB table name
    my_region_name = "us-east-2"  # Replace with your DynamoDB table name
    my_basicSongsTable_interface = DynamoDB_interface(my_table_name, my_region_name)
    my_basicSongsTable_interface.createSongTable()
    my_basicSongsTable_interface.upload()
    
    #get_all_table_items test
    song_items = my_basicSongsTable_interface.get_all_table_items()
    print(f"Main: Retrieved {len(song_items)} items from {my_basicSongsTable_interface.table_name}.")
    
    count = 0
    for item in song_items:
        #print(f"Main: item: {item}")
        #print(f"Main: item.keys: {item.keys()}")
        print(f"Main: item['artist'] {item['artist']}")
        print(f"Main: item['song'] {item['song']}")
        #print(f"Main: item['form'].keys() {item['form'].keys()}")
    
    
    
def temp_notes():
    #add_table_elm
    #get_table_elm
    #remove_table_elm
    
    #get_all_table_items test
    
    #get_all_table_items and remove invalid enttries from lambda testing
    my_DDB_interface = DynamoDB_interface()
    items = my_DDB_interface.get_all_table_items()
    print(f"Main: Retrieved {len(items)} items from {my_DDB_interface.table_name}.")
    
    count = 0
    for item in items:
        #print(f"Main: item: {item}")
        #print(f"Main: item.keys: {item.keys()}")
        #print(f"Main: item['PK'] {item['PK']}")
        print(f"Main: item['SK'] {item['SK']}")
        #print(f"Main: item['form'].keys() {item['form'].keys()}")
        
        if "name" in item['form'].keys():
            pass
        else:
            print(f"Main: remove {item['SK']}")
            my_DDB_interface.remove_table_elm(item['SK'])
            #print(f"Main: remove {item['form']}")
            #print(f"Main: remove {item['form']['headers']}")
        print("----------------------------------------------------")
        count += 1
        if count > 20:
            break
            
            
if __name__ == "__main__":
    print(f"Script name: {sys.argv[0]}")
    if len(sys.argv) > 1:
        print("Arguments:")
        runMode = sys.argv[1]
        if len(sys.argv) > 2:
            workingDir = sys.argv[2]
        #for i, arg in enumerate(sys.argv[1:]):
        #    print(f"  Argument {i+1}: {arg}")
    else:
        print("No arguments provided.")
    
    if "test_files" in runMode:
        test_DB()
    if "setup_files" in runMode:
        setup()
    pass