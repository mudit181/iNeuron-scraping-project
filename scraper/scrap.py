import sys
sys.path.append("../")
from flask import Flask,jsonify,request,render_template
from bs4 import BeautifulSoup as bs
import requests
from flask_cors import CORS,cross_origin
from urllib.request import urlopen as uReq
import json
from logger import logging
from mongo import mymongo
import os



class scraping:
    def __init__(self):
        try:
            self.original_url="https://ineuron.ai/courses"
            self.obj1 = mymongo()
            self.new_list = []
            logging.info("scraping all the course detail")
        except Exception as e:
            logging.error("check the correct url")

    def course_scrap(self):
        try:
            self.uClient = uReq(self.original_url)
            self.page = self.uClient.read()
            self.uClient.close()


            iNeuron_html = bs(self.page, "html.parser")
            courselistbox = iNeuron_html.find_all('script', {"id": "__NEXT_DATA__"})
            # print(courselistbox[0])


            #formet data from json review
            course_dict=json.loads(str(courselistbox[0].string))
            course_list= course_dict["props"]["pageProps"]["initialState"]["init"]["courses"]
            # print(course_list.values())


            for i in course_list.keys():
                # print(i)
                course_url = self.original_url[0:-1] + "/" + "-".join(str(i).split(" "))
                course_list[i]["course_url"] = course_url
                course_list[i]["course_name"] = i
                self.new_list.append(course_list[i])
            # print(new_list)
            logging.info("all the courses detail from https://ineuron.ai are dumped in a list ")
        except Exception as e:
            logging.error(str(e))
            logging.info("there might be chances of an error in formatting data into json format")

    # def coursedetails(self):
    #     course_res = requests.get(course_url)
    #     course_soup = bs(course_res.content, "html.parser")
    #     course_json = json.loads(course_soup.find("script", src=None).text)
    #     raw_data_json = course_json["props"]["pageProps"]
    #     page_data_json = raw_data_json["data"]
    #     detailed_data_json = page_data_json["details"]
    #     meta_data_json = page_data_json["meta"]
    #     curriculum_json = meta_data_json["curriculum"]
    #     overview_json = meta_data_json["overview"]
    #     courses = course_schema(page_data_json, detailed_data_json, meta_data_json, curriculum_json, overview_json)
    #     self.new_list.append(courses)



    def insert_Courses(self, dbname , collectionname):
        """this function dumps the scrap course data  to mongodb """
        try:
            self.obj1.create_connection(dbname, collectionname)
            self. obj1.insert_data(self.new_list)
            print("courses details are successfully dumped into mongo database ")
            logging.info("all the course details dumped into mongodb")

        except Exception as e:
            logging.error(str(e))

