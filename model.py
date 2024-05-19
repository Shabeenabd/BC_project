
# importing libraries 
import requests as re
import spacy


# initializing the return object
response=0
url='https://devapi.beyondchats.com/api/get_message_with_sources?'

# function to get response from specific pages | default=1
def get_responses(url=url,pageno=1):
    url+str(pageno)
    global response
    #response object
    response=re.get(url)

    # returning object to  carry response-source pair
    result=[]

    #importing nlp model using spacy 
    nlp = spacy.load("en_core_web_sm")

    #filtering to main data
    datas=response.json()['data']['data']

    #looping through each response
    for data in datas:

        #doc is response
        doc = nlp(data['response'])
        #tockenizing and removing stopwords from doc (response)
        nlp.vocab['yes']
        doc1=set([i.text.lower() for i in doc if not i.is_punct and not i.is_stop and i.text.lower()!='yes'])

        #citation object to carry the id and link
        result_cit=[]

        #to check the similarity between response and its source
        #so that we can make sure response came from the corresponding source
        #there by filtering unwanted sources
        score=[]
        
        #looping through each source
        for i in data['source']:
            #doc2 is context of each source
            doc2 =i['context']
            #calculating score by assessing the presence of common words in response and source
            score=[1  if word in doc2 else 0 for word in doc1]
            
            #calculating score
            try:
                #
                similarity_score=sum(score)/len(score)
            
            #if no common words
            except:
                print('no common words')
            #if similarity score is greater than 10% and it contain link
            if similarity_score>.1 and i['link']!='':

                #appending to citation object
                result_cit.append({'id':i['id'],'link':i['link']})

        #appending to the final object(response -source pair)
        result.append({'response':doc,'source' : result_cit})
        
    #returning the final result
    return result

#function to access the next page
def next_page():
    #accessing next page url from current response object property
    nxtpg=response.json()['data']['next_page_url']
    if nxtpg:
        url_new=nxtpg
        #calling the main function to get response
        return get_responses(url=url_new)
    else:
        #if there is no last page
        return None

#function for previous page 
def prev_page():
    prvpg=response.json()['data']['prev_page_url']
    if prvpg:
        url_new=prvpg
        return get_responses(url=url_new)
    else:
        return None 


#conclusion
#can get the response-source object by simply calling the get_response() function
#To view through web page , run  the flask application given:
                            # 1)app.py
                            # 2) index.html
