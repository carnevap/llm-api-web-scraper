import openai
import os
import requests
from bs4 import BeautifulSoup
import json
import time

start_time = time.time()


#Get links:
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

link_data = []

def getLinks(tag, page):
    url = f'https://stackoverflow.com/questions/tagged/{tag}?tab=Active&page={page}&pagesize=50'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('div', {'class': 's-post-summary'})

    for item in links:
        L = {
        'link': 'https://stackoverflow.com' + item.find('a', {'class': 's-link'})['href'],
        }
        link_data.append(L)
    return

for x in range(1,3):
    getLinks('python', x)
    getLinks('c++', x)
    getLinks('java', x)

with open('links.json', 'w', encoding='utf-8') as json_file:
    json.dump(link_data, json_file, ensure_ascii=False, indent=4)

print(f"Scraped {len(link_data)} links and saved them in 'links.json'.")

with open('links.json', 'r') as file:
    data = json.load(file)


#Get Questions / Answers:
url = data[4]['link'] #Change this value to select question

response = requests.get(url)

stackoverflow = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    Q = {
        'question': soup.find('div', class_='js-post-body').text.strip(),
    }
    stackoverflow.append(Q)

    answers = soup.find_all('div', class_='answer')
    for answer in answers:
        A = {
            'answer': answer.find('div', class_='js-post-body').text.strip()
        }
        stackoverflow.append(A)
else:
    print("Failed to retrieve the page. Status code:", response.status_code)

with open('content.json', 'w', encoding='utf-8') as json_file:
    json.dump(stackoverflow, json_file, ensure_ascii=False, indent=4)

print(f"Scraped {len(Q)} question(s) and {len(stackoverflow)-1} answer(s) and saved them in 'content.json'.")


#ChatGPT API:

processed = []

with open('content.json', 'r') as file:
    data = json.load(file)

MODEL="gpt-4" #"gpt-3.5-turbo"
openai.api_key  = ('') #Insert api key here
def get_completion(prompt, model=MODEL):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.6,
    )
    return response.choices[0].message["content"]

question = data[0]["question"]

text=f"I need help with the following question:", question #Modify this to change ChatGPT prompt

prompt=f"""

    ```{text}```
    """

P = {
    'processed': get_completion(prompt),
}
processed.append(P)

with open('processed.json', 'w', encoding='utf-8') as json_file:
    json.dump(processed, json_file, ensure_ascii=False, indent=4)

print(f"Processed the question and saved the compiled answer in 'processed.json'.")

#Improved answer processing:
with open('content.json', 'r') as file_content:
    data_content = json.load(file_content)

question_content = data_content[0]["question"]
answer_content = data_content[1]["answer"]

with open('processed.json', 'r') as file_processed:
    data_processed = json.load(file_processed)

processed_data = data_processed[0]["processed"]

improved = []

text=f"Can you combine these two answers and question to create an improved answer that expands on redability: ", question_content + "\n\nanswer: \n" + answer_content + "\n\nprocessed answer: \n" + processed_data #Modify this to change ChatGPT prompt

prompt=f"""

    ```{text}```
    """

P = {
    'improved': get_completion(prompt),
}
improved.append(P)

with open('improved.json', 'w', encoding='utf-8') as json_file:
    json.dump(improved, json_file, ensure_ascii=False, indent=4)

print(f"Processed the improved answer and saved it in 'improved.json'.")


#Time calculation: Display's time it took to run through the program
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time} seconds")