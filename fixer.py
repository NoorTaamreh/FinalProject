import json
import pandas as pd

def prepareData(path, flag):
    with open(path, 'r') as file:
        content = file.read() # read the file
        content = content.replace("{\"title\":", "\n{\"title\":") # add a new line before each title
        
        json_object = json.loads(content) # load the json object
        for index, row in enumerate(json_object['articles']): # iterate over the articles
            row['Flag'] = flag # add the flag to the row
            records.append(row) # append the row to the records list
            if index+1 == 2000: # stop after 2000 articles
                break

if __name__=="__main__":
    records = list() #list of dictionaries
    
    feed_list = [["G:\\Other computers\\My Laptop\\NoorTaamreh\\HTU\\DataScience\\FinalProject\AFND\\Dataset\\source_1\\scraped_articles.json", "credible"], 
                 ["G:\\Other computers\\My Laptop\\NoorTaamreh\\HTU\\DataScience\\FinalProject\AFND\\Dataset\\source_7\\scraped_articles.json", "uncredible"]
                 ] #list of lists
    
    for element in feed_list:
        prepareData(element[0], element[1]) #element[0] = path, element[1] = flag

    df = pd.DataFrame.from_records(records) #convert list of dictionaries to dataframe
    
    # df.to_csv('data.csv', index=False) 
    #commented out after saving it for the first time to avoid overwriting the file