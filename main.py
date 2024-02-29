from jira import JIRA
from jira_config import JIRA_USER,JIRA_URL,JIRA_TOKEN,OpenAPI_KEY
from openai import AzureOpenAI
import os

#Connection to JIRA

jira_url =  JIRA_URL
jira_user = JIRA_USER
jira_token = JIRA_TOKEN


#Connection to ChatGPT

client = AzureOpenAI(
      azure_endpoint = "https://agileai-artisans-aillm.openai.azure.com/", 
      api_key=OpenAPI_KEY,  
      api_version="2024-02-15-preview"
    )

# Function to connect to Jira

def connect_to_jira(url, username, token):
    try:
        jira_client = JIRA(server=url, basic_auth=(username, token))
        print("Successfully connected to Jira.")

        #Read description on story       
        passmessage=jira_client.issue('HAC-1').fields.description
        
        #Passing story description to OpenAI
        message_text = [{"role":"user","content":"Generate Acceptance Criteria for :"+passmessage}]

        #OpenAI connection
        completion = client.chat.completions.create(
        model="gpt-4-turbo", # model = "deployment_name"
        messages = message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
        )
        
        #Output from OpenAI
        openai_msg= completion.choices[0].message.content
        
        #Updating Output from OpenAI to JIRA
        customfield_id='customfield_10033'
        fieldstring =jira_client.issue('HAC-1').fields.customfield_10033
        
        if fieldstring is None or len(fieldstring) == 0: 
            jira_client.issue('HAC-1').update(fields={customfield_id:openai_msg})
        else :
            jira_client.issue('HAC-1').update(fields={customfield_id:fieldstring+ ' ' + openai_msg})    
            
    
        return jira_client
    
    except Exception as e:

        print(f"Failed to connect to Jira: {e}")

    return None

 # Establish the connection
jira_connection = connect_to_jira(jira_url, jira_user, jira_token) 




