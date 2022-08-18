import requests
import json
import re
#import inflect
from rdflib import Graph, Literal, RDF, URIRef, Namespace, Dataset
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# 1.    What is course COMP6741 about?
class CourseAbout(Action):

    def name(self) -> Text:
        return "course_about"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
            PREFIX uni: <http://uni.io/schema#>
            PREFIX unidata: <http://unidata.io/data#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            SELECT ?cname ?cdescription
            WHERE{

            ?course a vivo:Course.
            ?course rdfs:label "%s".
            ?course uni:courseName ?cname.
       	    ?course uni:courseDescription ?cdescription.
            }""" % (tracker.slots['course'])
                                       }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]

        if not results or not results["bindings"]:
            dispatcher.utter_message(text="Course is not found or does not have a description.")
        else:
            courses = {}
            for result in results["bindings"]:
                courseName = result["cname"]
                courseDes = result["cdescription"]
                code = courseName["value"]
                name = courseDes["value"]

                dispatcher.utter_message(text=f"course name - {code} and corresponding course description - {name}")
        return []


# 2. Which topics John competent in?
class studentCompetentTopic(Action):

    def name(self) -> Text:
        return "student_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
            PREFIX uni: <http://uni.io/schema#>
            PREFIX unidata: <http://unidata.io/data#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>        
            
            SELECT ?topicName
            WHERE{
              ?student foaf:name "%s".
              ?student uni:hasTranscript ?t.
              ?t uni:forCourse ?course.
              ?courseId rdfs:label ?course.
              ?t uni:hasGrade ?grade.
              ?lec uni:in_a ?courseId.
              ?lec uni:hasLectureContent ?lecmat.
              ?topic uni:covered_by ?lecmat.
              ?topic rdfs:label ?topicName.
              FILTER (?grade >= "1.5")
            }""" % (tracker.slots['student'])
                                       }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]

        if not results or not results["bindings"]:
            dispatcher.utter_message(text="Student don't have competent topics, Try again for different student.")
        else:
            courses = {}
            dispatcher.utter_message(text=f"topics :- ")
            for result in results["bindings"]:
                topicName = result["topicName"]
                name = topicName["value"]
                dispatcher.utter_message(text=f"{name}")
        return []

#3. Which courses at Concordia teach Machine_learning?
class CoursesLecture(Action):
    def name(self) -> Text:
        return "action_topic_to_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                    PREFIX uni: <http://uni.io/schema#>
                    PREFIX unidata: <http://unidata.io/data#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX vivo: <http://vivoweb.org/ontology/core#>
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    SELECT ?coursename  (count (?coursename) as ?count)
                    WHERE {
                      ?topic uni:covered_by ?lcURI.
                      ?topic rdfs:label "%s".
                      ?lecId uni:hasLectureContent ?lcURI.
                      ?lecId rdfs:label ?lecture.
                      ?lcURI rdf:type ?t.
                      ?lcURI rdfs:label ?type.
                      ?lecId uni:in_a ?course.
                      ?course rdfs:label ?coursename.
                    }GROUP BY ?coursename ORDER BY DESC(?count)""" % (tracker.slots['topic'])
                                       }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]
        if not results or not results["bindings"]:
            dispatcher.utter_message(text="Topic not connected to course or not found")
        else:
            answer = "The courses :\n"
            for result in results["bindings"]:
                count = result["count"]["value"]
                name = result["coursename"]["value"]
                answer = answer + name + " teach " + tracker.slots['topic'] + " repeated " + count + " times\n"
            dispatcher.utter_message(text=f"{answer}")
        return []

#4. Which topics are covered in COMP6471?
class TopicCourse(Action):
    def name(self) -> Text:
        return "topic_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                    PREFIX uni: <http://uni.io/schema#>
                    PREFIX unidata: <http://unidata.io/data#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX vivo: <http://vivoweb.org/ontology/core#>
                    SELECT DISTINCT ?topicName
                    WHERE{
                        ?courseId rdfs:label "%s".
                        ?lec uni:in_a ?courseId.
                        ?lec uni:hasLectureContent ?lecmat.
                        ?topic uni:covered_by ?lecmat.
                        ?topic rdfs:label ?topicName.
                    }""" % (tracker.slots['course'])
                                       }
                                 )
        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]

        if not results or not results["bindings"]:
            dispatcher.utter_message(text="Topics covered by course not found or might not exist at the time.")
        else:
            answer = "This course covers following topics:\n"
            for result in results["bindings"]:
                topic = result["topicName"]["value"]
                answer = answer + "- " + topic + "\n"
                dispatcher.utter_message(text=f"{answer}")
        return []

#5. What is the name of COMP474 lecture 2?
class LectureName(Action):
    def name(self) -> Text:
        return "find_lecture_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, any]]:
        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                            PREFIX uni: <http://uni.io/schema#>
                            PREFIX unidata: <http://unidata.io/data#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                            SELECT ?lectureIsAbout
                            WHERE{
                                ?lec a uni:Lecture .
                                ?lec uni:lectureNumber %d .
                                ?lec uni:in_a ?course .
                                ?course rdfs:label "%s".
                                ?lec uni:lectureName ?lectureIsAbout .
                            }""" % (int(float(tracker.slots['number'])), tracker.slots['course'])
                                       }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]
        if not results or not results["bindings"]:
            dispatcher.utter_message(text="Lecture is not found or name might not exist.")
        else:
            answer = "This lecture is about:\n"
            for result in results["bindings"]:
                lecture = result["lectureIsAbout"]["value"]
                answer = answer + " " + lecture + "\n"
            dispatcher.utter_message(text=f"{answer}")
        return []

# 6. How many courses does the University offer?
class NumberofCourses(Action):
    def name(self) -> Text:
        return "find_numofcourse"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #university = tracker.slots['university']
        # if "concordia" in university.lower() or "university" in university.lower():
        #     university = "Concordia_University"
        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                            PREFIX uni: <http://uni.io/schema#>
                            PREFIX unidata: <http://unidata.io/data#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                            SELECT ?uname (COUNT(?course) AS ?coursesNum)
                            WHERE{
                                ?university a uni:University.
                                ?university foaf:name ?uname.
                                ?university uni:offers ?course.
                            } GROUP BY ?university ?uname"""
                                     }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]
        if not results or not results["bindings"]:
            dispatcher.utter_message(text="There is no courses in any university.")
        else:
            for result in results["bindings"]:
                university = result["uname"]["value"]
                courses_num = result["coursesNum"]["value"]
                answer = university + " offers " + courses_num + " courses." + "\n"
            dispatcher.utter_message(text=f"{answer}")
        return []

# 7. How many topics are covered in COMP474?
class NumberofTopics(Action):
    def name(self):
        return "find_number_of_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                                        PREFIX uni:<http://uni.io/schema#>
                                        PREFIX unidata:<http://unidata.io/data#>
                                        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                                        PREFIX vivo:<http://vivoweb.org/ontology/core#>
                                        SELECT ?coursename (COUNT(?topic) AS ?topicNum)
                                        WHERE {
                                            ?course a vivo:Course.
                                            ?course rdfs:label "%s".
                                            ?course uni:courseName ?coursename.
                                            ?lec uni:in_a ?courseId.
                                            ?lec uni:hasLectureContent ?lecmat.
                                            ?topic uni:covered_by ?lecmat.
                                        }GROUP BY ?coursename""" % (tracker.slots['course'])
                                       })

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]
        if not results or not results["bindings"]:
            dispatcher.utter_message(text="This course covers no topics or does not exist.")
        else:
            for result in results["bindings"]:
                course_name = result["coursename"]["value"]
                topic_num = result["topicNum"]["value"]
                answer = course_name + " have " + topic_num + " number of topics \n"
            dispatcher.utter_message(text=f"{answer}")
        return []

# 8. Does COMP6741 have labs?
class CourseLabs(Action):
    def name(self):
        return "ask_have_courselabs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                                                    PREFIX uni: <http://uni.io/schema#>
                                                    PREFIX unidata: <http://unidata.io/data#>
                                                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                    PREFIX vivo: <http://vivoweb.org/ontology/core#>
                                                    ASK{
                                                        ?course a vivo:Course.
                                                        ?course rdfs:label "%s".
                                                        ?lab uni:in_a ?course.
                                                        } """ % (tracker.slots['course'])
                                       }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        result = y["boolean"]

        if result:
            dispatcher.utter_message(text=f"YES,this course has labs.")
        else:
            dispatcher.utter_message(text=f"NO, this course does not have labs.")

        return []

# 9. What is the course Credit of comp474?
class CourseCredit(Action):
    def name(self) -> Text:
        return "find_course_credit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                                                    PREFIX uni: <http://uni.io/schema#>
                                                    PREFIX unidata: <http://unidata.io/data#>
                                                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                    PREFIX vivo: <http://vivoweb.org/ontology/core#>
                                                    SELECT ?courseId ?cName ?credit
                                                    WHERE {
                                                        ?course a vivo:Course.
                                                        ?course uni:courseSubject "%s".
                                                        ?course uni:courseNumber "%d".
                                                        ?course rdfs:label ?courseId.
                                                        ?course uni:courseName ?cName.
                                                        ?course uni:courseCredit ?credit .
                                                    } """ % (tracker.slots['course'], int(float(tracker.slots['number'])))
                                       }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]
        if not results or not results["bindings"]:
            dispatcher.utter_message(text="Currently, Course credits for the course is not available.")
        else:
            for result in results["bindings"]:
                course_id = result["courseId"]["value"]
                course_name = result["cName"]["value"]
                credit = result["credit"]["value"]
                answer = "Course " + course_id + "-" + course_name + " have " + credit + " number of credits\n"
            dispatcher.utter_message(text=f"{answer}")
        return []

# 10. Which course Sarah will take again?
class CoursesTakeAgain(Action):
    def name(self) -> Text:
        return "find_courses_take_again"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                                                            PREFIX uni: <http://uni.io/schema#>
                                                            PREFIX unidata: <http://unidata.io/data#>
                                                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                                                            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                                                            SELECT ?course 
                                                            WHERE {
                                                                ?student foaf:name "%s".
                                                                ?student uni:hasTranscript ?t.
                                                                ?t uni:forCourse ?course.
                                                                ?t uni:hasGrade ?grade.
                                                                FILTER (?grade <= "2")
                                                            } """ % (tracker.slots['student'])
                                       }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]
        if not results or not results["bindings"]:
            dispatcher.utter_message(text="This student does not need to retake any courses or does not exist.")
        else:
            answer = f"{tracker.slots['student']} will retake \n"
            for result in results["bindings"]:
                course_id = result["course"]["value"]
                answer = answer + "- " + course_id + "\n"
            dispatcher.utter_message(text=f"{answer}")
        return []

# 11. Which topics are covered in slide2 of COMP474?
class CoursesTakeAgain(Action):
    def name(self) -> Text:
        return "find_topic_of_courseEvent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.post('http://localhost:3030/ass1/sparql',
                                 data={'query': """
                                                            PREFIX uni: <http://uni.io/schema#>
                                                            PREFIX unidata: <http://unidata.io/data#>
                                                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                                            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                                                            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                                                            SELECT ?topicName ?topic
                                                            WHERE {
                                                              ?lecid uni:in_a ?course.
                                                              ?course rdfs:label "%s".
                                                              ?lecid uni:hasLectureContent ?lc.
                                                              ?lc rdfs:label "%s".
                                                              ?topic uni:covered_by ?lc.
                                                              ?topic rdfs:label ?topicName.
                                                            }""" % (tracker.slots['course'], tracker.slots['courseEvent'])
                                       }
                                 )

        # dispatcher.utter_message(text=f" {response.status_code}")
        # dispatcher.utter_message(text=f" {response.raise_for_status()}")
        y = json.loads(response.text)
        results = y["results"]
        if not results or not results["bindings"]:
            dispatcher.utter_message(text="Material do not have topics available for the given course.")
        else:
            for result in results["bindings"]:
                tName = result["topicName"]["value"]
                tLink = result["topic"]["value"]
                answer = "Topic - " + tName + " have link -" + tLink + "\n"
                dispatcher.utter_message(text=f"{answer}")
        return []