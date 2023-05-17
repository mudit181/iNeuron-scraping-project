from logger import logging
import pymongo

class mymongo:
    def __init__(self):
        """this function is to connect with mongo db database."""
    try:
        client = pymongo.MongoClient("mongodb+srv://mudit:mudit@cluster0.hdheukw.mongodb.net/?retryWrites=true&w=majority")
        # print(client.test)
        logging.info("connect with mongodb")
    except Exception as e:
        print(e)
        logging.error(e)
        logging.info("try another connection")

    #
    def create_connection(self, database_name, collection_name):
        try:
            self.db= self.client[database_name]
            self.coll=self.db[collection_name]
            print(self.db)
            logging.info("new database  and collection is  created")
        except Exception as e:
            logging.info("Connection not established", e)
        else:
            logging.info("Connection  is successful")

    def insert_data(self, data):
        try:
            self.coll.insert_many(data)
            logging.info("insert all the scrap courses from iNeuron into database")
        except Exception as e:
            logging.error(e)

    def details(self):
        for i in self.coll.find():
            print(i)

