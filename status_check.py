import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import URLError
import datetime

def my_function():
  #Defined Values in dictionaries to get user inputs on which environment we want to run health check
  environment = {
    1: "iVerify_Dev",
    2: "iforms_UAT",
    3: "iforms_QA",
    4: "iforms_DEV",
    5: "iConductor_DEV",
    6: "iConductor_UAT",
    7: "iConductor_QA2"}
  #Print the dictionaries for user inputs
  for key,value in environment.items():
    print(key,"==>",value)
  #Take user input into integer and pass that for pickup a file according to that
  userInput = int(input("Please Enter environment ID from below list for health check: "))
  print(environment[userInput])
  filename = environment[userInput] + ".csv"

  source_path = "C:\\Users\\bathia_s\\Desktop\\"
  source_filename = environment[userInput] + ".csv"
  dest_filename = environment[userInput] + '_' + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv'
  dest_path = "C:\\Users\\bathia_s\\Desktop\\"

  data = pd.read_csv(source_path + source_filename, encoding="ISO-8859-1")

  # Add a new column for new CSV file with "Status" to capture URL status
  Status = pd.DataFrame({'new_header': []})
  result = []

  for row in data.URL:
    req = Request(row)
    try:
      response = urlopen(req)
    except URLError as e:
      if hasattr(e, 'reason'):
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        result.append(e.reason)
      elif hasattr(e, 'code'):
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        result.append(e.code)
    else:
      print("success")
      result.append("Success")
  # Final result of URL status is added
  data['Status'] = result
  # Create a new CSV file

  data.to_csv(dest_path + dest_filename)

my_function()
