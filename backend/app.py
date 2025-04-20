from flask import Flask,jsonify
import logging
import base64
import requests
import re

#sets up flask application and logging 
app= Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

#GitHub API for READEME file
url="https://api.github.com/repos/SimplifyJobs/Summer2025-Internships/readme"

#Dictitionary to store each internship details
formatted_content=dict() 

#Helper function that formats the internship listing and details together 
def format_content(lst):
    #An identifer for internship listing, the key for the dictionary
    num=1
    #Internship details are stored in a list and are the value of the dictionary 
    intern_details= list()

    for index, value in enumerate(lst):
        #Identifies the ReadMe 5 categories the for loop has reached 
        mod= index % 5
        
        parantheses=re.compile(r"\( | \)")
        #if : x
            


        #A handler for a edge case where instead of the company name from the last item it uses an arrow
        if str(value).strip()=="\u21b3":
            company_name=formatted_content[f'Internship_Details_{num-1}']
            value=company_name[0]

        #Handler to format and stores Intenrship's company name 
        if mod == 0:
            pattern=re.compile(r"[\*\[\]\(\)]")
            '''if re.findall(r'\*\*\[((.*?)\]',lst[index+5])==[]:
            if re.findall(r'href="(https://[^"]+)"',lst[index+13])==[]:'''

            name_link=re.sub(pattern, '', value)
            company_name=name_link.split("https")
            intern_details.append(company_name[0])

        #Handler that stores the Internship role
        elif mod == 1:
            intern_details.append(value)

        #Handler to format and stores company location/s
        elif mod == 2:
            pattern=re.compile('<.*?>')
            value=re.sub(pattern,'',value)
            pattern2 = re.compile(r'\*\*\s*\d+\s+locations\s*\*\*')
            value=re.sub(pattern2,'',value)

            value.split()
            intern_details.append(value)
        
        #Handler that formats and stores Internship application links as a list 
        elif mod == 3:
            intern_applications=re.findall(r'href="(https://[^"]+)"', value)
            intern_details.append(intern_applications)

        #Handler that stores in the date posted and stores the intern_details list to formatted_content
        elif mod == 4:
            intern_details.append(value)
            formatted_content[f'Internship_Details_{num}']=intern_details

            #Resets the list for the next iteration and increments num for the next key in formatted_content
            intern_details= list()
            num+=1


@app.route('/')

def hello():
    response=requests.get(url)

    if response.status_code!=200:
       return jsonify({"error": "Repository or README not found"}), response.status_code

    #Readme has been decoded
    data=response.json()
    content_base64 = data["content"]
    content = base64.b64decode(content_base64).decode("utf-8")
    
    #Formats the README content where only the active internship listings are left 
    edit_content=content.split("**[",1)[1]
    edit_content=edit_content.split("\U0001F512",1)[0]
    edit_content=edit_content.split("|")
    edit_content=edit_content[:-4]
    
    #Goes through the edit_content list and formats it further where "\n" and any large entry are deleted
    fixed_content=[]
    for index, value in enumerate(edit_content):
        #The condition where a job entry can be added into the list if it follows the size requirements
        if value=="\n" and index%6==5:
           beginning_category=index-5
           ending_category=index-1
           
           #Only includes the entry details, ignoring "\n"
           while beginning_category<=ending_category:
            fixed_content.append(edit_content[beginning_category])
            beginning_category+=1
        

    #Removes any "\n" that are in the list
    #new_content = [x for x in edit_content if x.strip() not in [""]]

    format_content(fixed_content)
   
   #Prints out a list keys from formatted_content
    #app.logger.info(list(formatted_content.keys()))
    app.logger.info(fixed_content)
    
   #Returns the dictionary to home page 
    return( 
        formatted_content
    )

if __name__=='__main__':
    app.run(debug=True)
