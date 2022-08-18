import csv
import os


import spacy
from rdflib import Graph, Literal, RDF, URIRef, BNode, Namespace
from rdflib.namespace import FOAF, RDFS
from tika import parser
from  spacy.matcher import Matcher


DB = Namespace("http://dbpedia.org/resource/")
DBP = Namespace("http://dbpedia.org/property/")
VIVO = Namespace("http://vivoweb.org/ontology/core#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
UNI = Namespace("http://uni.io/schema#")
UNID = Namespace("http://unidata.io/data#")

g = Graph()
g1 = Graph()
g.parse("RDF_Schema.ttl", format="n3")

g1.bind("foaf", FOAF)
g1.bind("rdf", RDF)
g1.bind("rdfs", RDFS)
g1.bind("vivo", VIVO)
g1.bind("uni", UNI)
g1.bind("unidata", UNID)
g1.bind("dbpedia", DB)

filename = "C://Users/formy/PycharmProjects/Assignment-Unibot/dataset/CATALOG.csv"
studentFile = "C://Users/formy/PycharmProjects/Assignment-Unibot/dataset/StudentData.csv"
root = "C://Users/formy/PycharmProjects/Assignment-Unibot/dataset/Courses"
slidepath474 = root + "/COMP474/Lecture/slides"
wspath474 = root + "/COMP474/Worksheet/worksheet"
labpath474 = root + "/COMP474/Lab/lab"
outpath474= root + "/COMP474/Outline/outline"
slidepath6721 = root +"/COMP6721/Lectures/slide"
wspath6721 = root + "/COMP6721/Worksheets/worksheet"
outpath6721= root + "/COMP6721/Outline/outline"
uniNamespace = "http://uni.io/schema#"
uniDataNamespace = "http://unidata.io/data#"


comp474List = [["",""],
               ['Introduction to Intelligent Systems','Intelligent_Systems'],
               ['Introduction to Knowledge Graphs','RDF'],
               ['Knowledge Graphs: Vocabularies & Ontologies' , 'Knowledge_Graph'],
               ['Knowledge Base Queries' ,'SPARQL'],
               ['Linked Open Data (LOD) & Applications ','Linked_data'],
               ['Personalization & Recommender Systems', 'Recommender_system'],
               ['Introduction to Machine Learning for Intelligent Systems' ,'Machine_learning']]


comp6721List = [
                ['',''],
                ['Introduction to AI: Overview & History', 'Artificial_intelligence'],
                ['State-Space Search: Uninformed & Heuristic Search ', 'State_space_search'],
                ['Adversarial Search: Mini-Max & Alpha-Beta Pruning ' ,'Alpha-beta_pruning' ],
                ['Introduction to Machine Learning (ML)' , 'Machine_learning'],
                ['ML: Decision Trees, Evaluation & Unsupervised Learning ', 'Machine_learning'],
                ['Introduction to Artificial Neural Networks', 'Artificial_neural_network'],
                ['Introduction to Deep Learning, Convolutional Neural Networks' , 'Deep_learning'],
                ['Knowledge Graphs & Intelligent Agents (I)', 'Knowledge_Graph'],
                ['Knowledge Graphs & Intelligent Agents (II)', 'Knowledge_Graph'],
                ['Introduction to Natural Language Processing (NLP)', 'Natural_language_processing'],
                ['NLP: Vector Space Model, Applications', 'Vector_space_model'],
                ['Deep Learning for NLP', 'Deep_learning'],
                ['conclusions','']
                ]
def populate():
    g1.add((UNID.Concordia, RDF.type, UNI.University))
    g1.add((UNID.Concordia, FOAF.name, Literal("Concordia University")))
    g1.add((UNID.Concordia, RDFS.seeAlso, DB.Concordia_University))

    special_characters = "()"
    with open(filename,'r') as data:
        r = csv.DictReader(data)
        for row in r:
            course = URIRef(uniDataNamespace + row['Course code'] + row['Course number'])

            if(course!=" ") & (row['Course code']!=""):
                g1.add((UNID.Concordia, UNI.offers, course))
                g1.add((course, RDFS.label, Literal(row['Course code'] + row['Course number'])))
                g1.add((course, RDF.type, VIVO.Course))
                g1.add((course, UNI.courseName, Literal(row['Title'])))
                g1.add((course, UNI.courseSubject, Literal(row['Course code'])))
                g1.add((course, UNI.courseNumber, Literal(row['Course number'])))
                g1.add((course, UNI.courseDescription, Literal(row['Description'])))
                if(row['Website']!=""):
                    g1.add((course, UNI.courseLink, Literal(row['Website'])))

                if(row['Course code']=="COMP" and (row['Course number']=="474" or row['Course number']=="6721")):
                    g1.add((course, UNI.courseCredit, Literal(4)))
                    lecture = URIRef(uniDataNamespace + row['Course code'] + row['Course number'] + "Lec")
                    if(row['Course number']=="474"):
                        g1.add((course, UNI.courseOutline, URIRef(outpath474+".pdf")))
                        # txtGenerator(outpath474)
                        # result = tlink(outpath474)
                        # for r in result:
                        #     g1.add((UNID[r[0]],RDF.type,UNI.Topics))
                        #     g1.add((UNID[r[0]], RDFS.label, Literal(comp474List[i][1])))
                        #     g1.add((UNID[r[0]], UNI.covered_by, course))
                        #     g1.add((UNID[r[0]], RDFS.seeAlso, r[1]))
                        #     print(r[0] + "--->" +r[2])


                        for i in range(1,8):
                            lecture = URIRef(uniDataNamespace + row['Course code'] + row['Course number'] + "Lec" + str(i))
                            g1.add((lecture, UNI.in_a, course))
                            g1.add((lecture, RDF.type, UNI.Lecture))
                            g1.add((lecture, RDFS.label, Literal("Lec"+str(i))))
                            g1.add((lecture, UNI.lectureNumber, Literal(i)))
                            slide = URIRef(slidepath474+"0"+str(i)+".pdf")
                            worksheet = URIRef(wspath474+"0"+str(i)+".pdf")
                            lab = URIRef(labpath474+"0"+str(i)+".pdf")
                            g1.add((lab, RDF.type, UNI.Lab))
                            g1.add((lab, RDFS.label, Literal("lab" + str(i))))
                            g1.add((slide, RDF.type, UNI.Slides))
                            g1.add((slide, RDFS.label, Literal("slide" + str(i))))
                            g1.add((lecture, UNI.hasLectureContent, slide))
                            g1.add((worksheet, RDF.type, UNI.Worksheet))
                            g1.add((worksheet, RDFS.label, Literal("ws" + str(i))))
                            g1.add((lecture, UNI.hasLectureContent, worksheet))
                            g1.add((lecture, UNI.lectureName, Literal(comp474List[i][0])))
                            g1.add((lecture, RDFS.seeAlso, DB[comp474List[i][1]]))
                            g1.add((UNID[comp474List[i][1]], RDF.type, UNI.Topics))
                            g1.add((UNID[comp474List[i][1]], RDFS.label, Literal(comp474List[i][1])))
                            g1.add((UNID[comp474List[i][1]], UNI.covered_by, lecture))
                            g1.add((UNID[comp474List[i][1]], RDFS.seeAlso, DB[comp474List[i][1]]))

                            txtGenerator(slidepath474+"0"+str(i)+".pdf")
                            result = tlink(slidepath474+"0"+str(i)+".pdf.txt")
                            resultSpacy = tlinks(slidepath474 + "0" + str(i) + ".pdf.txt")
                            resultToken = tlinkt(slidepath474 + "0" + str(i) + ".pdf.txt")
                            for r in result:

                                if any(c in special_characters for c in r[2]):
                                    continue
                                else:
                                    for r2 in resultSpacy:
                                        if(r[0]==r2[0]):
                                            # print(r2[0] + " - link for -" + r[2] + " - label - "+ r2[1])
                                            g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                                # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                            g1.add((URIRef(r[2]), UNI.covered_by, slide))
                                            g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                            g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r2[1])))
                                                # g1.add((lecture, RDFS.seeAlso, URIRef(r[2])))

                                    for r1 in resultToken:
                                        if(r[0]==r1[0]):
                                            # print(r2[0] + " - link for -" + r[2] + " - label - "+ r2[1])
                                            g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                                # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                            g1.add((URIRef(r[2]), UNI.covered_by, slide))
                                            g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                            g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r1[1])))
                                                # g1.add((lecture, RDFS.seeAlso, URIRef(r[2])))

                            txtGenerator(wspath474 + "0" + str(i) + ".pdf")
                            result = tlink(wspath474 + "0" + str(i) + ".pdf.txt")
                            resultSpacy = tlinks(wspath474 + "0" + str(i) + ".pdf.txt")
                            resultToken = tlinkt(wspath474 + "0" + str(i) + ".pdf.txt")
                            for r in result:
                                if any(c in special_characters for c in r[2]):
                                    continue
                                else:
                                    for r2 in resultSpacy:
                                        if(r[0]==r2[0]):
                                            g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                            # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                            g1.add((URIRef(r[2]), UNI.covered_by, worksheet))
                                            g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                            g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r2[1])))

                                    for r1 in resultToken:
                                        if (r[0] == r1[0]):
                                            # print(r2[0] + " - link for -" + r[2] + " - label - "+ r2[1])
                                            g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                            # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                            g1.add((URIRef(r[2]), UNI.covered_by, worksheet))
                                            g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                            g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r1[1])))
                                            # g1.add((lecture, RDFS.seeAlso, URIRef(r[2])))


                            if (i != 1 and i!= 3):
                                txtGenerator(labpath474 + "0" + str(i) + ".pdf")
                                result = tlink(labpath474 + "0" + str(i) + ".pdf.txt")
                                resultSpacy = tlinks(labpath474 + "0" + str(i) + ".pdf.txt")
                                resultToken = tlinkt(labpath474 + "0" + str(i) + ".pdf.txt")
                                for r in result:
                                    if any(c in special_characters for c in r[2]):
                                        continue
                                    else:
                                        for r2 in resultSpacy:
                                            if (r[0] == r2[0]):
                                                g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                                # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.covered_by, lab))
                                                g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r2[1])))
                                        for r1 in resultToken:
                                            if (r[0] == r1[0]):
                                                # print(r2[0] + " - link for -" + r[2] + " - label - "+ r2[1])
                                                g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                                # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.covered_by, lab))
                                                g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r1[1])))
                                                # g1.add((lecture, RDFS.seeAlso, URIRef(r[2])))

                    if (row['Course number'] == "6721"):
                        g1.add((course, UNI.courseOutline, URIRef(outpath6721 + ".pdf")))

                        for i in range(1, 13):
                            lecture = URIRef(
                            uniDataNamespace + row['Course code'] + row['Course number'] + "Lec" + str(i))
                            g1.add((lecture, UNI.in_a, course))
                            g1.add((lecture, RDF.type, UNI.Lecture))
                            g1.add((lecture, RDFS.label, Literal("Lec" + str(i))))
                            g1.add((lecture, UNI.lectureNumber, Literal(i)))
                            slide = URIRef(slidepath6721 + str(i) + ".pdf")
                            worksheet = URIRef(wspath6721 + str(i) + ".pdf")
                            g1.add((slide, RDF.type, UNI.Slides))
                            g1.add((slide, RDFS.label, Literal("slide" + str(i))))
                            g1.add((lecture, UNI.hasLectureContent, slide))
                            if(i!=1 and i!=12):
                                g1.add((worksheet, RDF.type, UNI.Worksheet))
                                g1.add((worksheet, RDFS.label, Literal("ws" + str(i))))
                                g1.add((lecture, UNI.hasLectureContent, worksheet))
                            g1.add((lecture, UNI.lectureName, Literal(comp6721List[i][0])))
                            g1.add((lecture, RDFS.seeAlso, DB[comp6721List[i][1]]))
                            g1.add((UNID[comp6721List[i][1]], RDF.type ,UNI.Topics))
                            g1.add((UNID[comp6721List[i][1]], RDFS.label, Literal(comp6721List[i][1])))
                            g1.add((UNID[comp6721List[i][1]], UNI.covered_by, lecture))
                            g1.add((UNID[comp6721List[i][1]], RDFS.seeAlso, DB[comp6721List[i][1]]))

                            if(i!=3):
                                txtGenerator(slidepath6721 + str(i) + ".pdf")
                                result = tlink(slidepath6721 + str(i) + ".pdf.txt")
                                resultSpacy = tlinks(slidepath6721 + str(i) + ".pdf.txt")
                                resultToken = tlinkt(slidepath6721 + str(i) + ".pdf.txt")
                                for r in result:
                                    if any(c in special_characters for c in r[2]):
                                        continue
                                    else:
                                        for r2 in resultSpacy:
                                            if (r[0] == r2[0]):

                                                g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                              # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.covered_by, slide))
                                                g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                                # g1.add((lecture, RDFS.seeAlso, URIRef(r[2])))
                                                g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r2[1])))
                                        for r1 in resultToken:
                                            if (r[0] == r1[0]):
                                                # print(r2[0] + " - link for -" + r[2] + " - label - "+ r2[1])
                                                g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                                # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.covered_by, slide))
                                                g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r1[1])))
                                                # g1.add((lecture, RDFS.seeAlso, URIRef(r[2])))

                            if (i != 1 and i != 12):
                                txtGenerator(wspath6721 + str(i) + ".pdf")
                                result = tlink(wspath6721 + str(i) + ".pdf.txt")
                                resultSpacy = tlinks(wspath6721 + str(i) + ".pdf.txt")
                                resultToken = tlinkt(wspath6721 + str(i) + ".pdf.txt")
                                for r in result:
                                    if any(c in special_characters for c in r[2]):
                                        continue
                                    else:
                                        for r2 in resultSpacy:
                                            if (r[0] == r2[0]):
                                                g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                                # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.covered_by, worksheet))
                                                g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r2[1])))

                                        for r1 in resultToken:
                                            if (r[0] == r1[0]):
                                                # print(r2[0] + " - link for -" + r[2] + " - label - "+ r2[1])
                                                g1.add((URIRef(r[2]), RDF.type, UNI.Topics))
                                                # g1.add((UNID[r[0]], RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.covered_by, worksheet))
                                                g1.add((URIRef(r[2]), RDFS.label, Literal(r[0])))
                                                g1.add((URIRef(r[2]), UNI.topicLabel, Literal(r1[1])))
                                                # g1.add((lecture, RDFS.seeAlso, URIRef(r[2])))

    tempstu = "Deep"
    with open(studentFile,'r') as data:
        r = csv.DictReader(data)
        count=1
        for row in r:
            if(row['id']!=""):
                tempid = row['id']
                tempstu = row['First_name']
                student = URIRef(uniDataNamespace + tempid)
                g1.add((student, RDF.type, UNI.student))
                g1.add((student, FOAF.name, Literal(row['First_name'])))
                g1.add((student, FOAF.familyName, Literal(row['last_name'])))
                g1.add((student, UNI.id, Literal(row['id'])))
                g1.add((student, FOAF.mbox, Literal(row['Email'])))
            if(row['Grade'] != ''):
                # tpf = row['Pass/Fail']
                tran = URIRef(uniDataNamespace+ 'Transcript'+str(count))
                g1.add((tran, RDF.type, UNI.Transcript))
                g1.add((tran,RDFS.label, Literal( 'Transcript'+str(count))))
                g1.add((student, UNI.hasTranscript, tran))
                g1.add((tran, UNI.hasGrade, Literal(row['Grade'])))
                g1.add((tran, UNI.passsingYear, Literal(row['Term'])))
                #g1.add((student, UNI.hasTaken, UNID[row['Completed Course']]))
                g1.add((tran, UNI.forCourse, Literal(row['Completed Course'])))
                count+=1
                # if(row['Pass/Fail'] == 'Fail'):
                #     g1.add((student, UNI.willRetake, UNID[row['Completed Course']]))
                # if(row['Grade'>=2]):
                #     g1.add((student, UNI.cTopic, Literal(row['Competency Topic'])))

    print(g1.serialize(destination="KBTurtleFinalG1.ttl", format = "n3"))
    print(g1.serialize(destination="KBTripleFinalG1.rdf", format="nt"))
    #print(g.serialize())


def tlink(path):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('dbpedia_spotlight', config={'dbpedia_rest_endpoint': 'http://localhost:2222/rest'})
    #pathl = path+".txt"
    # get the document
    # ----------------------------------CHANGE---------------------------------------------
    #pathl = path
    # ----------------------------------CHANGE---------------------------------------------
    with open(path, 'r', encoding="utf-8") as f:
        datac = f.read()
    doc = nlp(datac)
    # see the entities
    listl = []
    for ent in doc.ents:
        if eval(ent._.dbpedia_raw_result['@similarityScore']) >= 0.70:
            tl = [ent.text, ent.label_, ent.kb_id_]
            listl.append(tl)
            print('Entities', [(ent.text, ent.kb_id_)])
    return listl

def tlinks(path):
    nlp = spacy.load('en_core_web_sm')
    with open(path, 'r', encoding="utf-8") as f:
        datac = f.read()
    doc = nlp(datac)
    # see the entities
    listl = []
    c=0
    for ent in doc.ents:
        tl = [ent.text,ent.label_]
        listl.append(tl)
        print('Entities', [(ent.text, ent.label_)])
        c+=1
    print(c)
    return listl

def tlinkt(path):
    nlp = spacy.load('en_core_web_sm')
    with open(path, 'r', encoding="utf-8") as f:
        datac = f.read()
    doc = nlp(datac)
    # see the entities
    listl = []


    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'PROPN'}]
    matcher.add("uni_identifier", [pattern])
    matches = matcher(doc)
    t1 = []
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        t1.append(span.text)
    for token in doc:
        if (token.text in t1):
            tl = [token.text, token.pos_]
            listl.append(tl)
            print('Entities', [(token.text, token.pos_)])

    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'NOUN'}]
    matcher.add("uni_identifier", [pattern])
    matches = matcher(doc)
    t2 = []
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        t2.append(span.text)
    for token in doc:
        if (token.text in t2):
            tl = [token.text, token.pos_]
            listl.append(tl)

    print(listl)
    return listl


def txtGenerator(path):
    parsed_pdf = parser.from_file(path)
    txt_outline = path+".txt"
    data = parsed_pdf['content']
    #print(data)

    print(txt_outline)
    with open(txt_outline, 'w', encoding="utf-8") as f:
        f.write(str(data))

if __name__ == '__main__':
    populate()