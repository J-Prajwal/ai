import json
import pandas as pd
import numpy as np
import openai
from gpt import GPT
import sys
import datetime
from gpt import Example
import os
from dotenv import load_dotenv

load_dotenv()


temp_query = sys.argv
temp_query.pop(0)


query = ' '.join(temp_query)


openai.api_key = os.getenv('API_KEY')

gpt = GPT(engine="davinci",
          temperature=0,
          max_tokens=500)


df = pd.read_csv("./data/transfer_action.csv")
df2 = pd.read_csv("./data/site_accepted_for_filing.csv")

# Granted file query
gpt.add_example(Example('Show details of all granted lease applications.',
                        'response = df[df["action"] == "G"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))
gpt.add_example(Example('Give me all granted lease applications.',
                        'response = df[df["action"] == "G"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))
gpt.add_example(Example('Granted',
                        'response = df[df["action"] == "G"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))

# Pending file query
gpt.add_example(Example('Give me all pending lease applications.',
                        'response = df[df["action"] == "Q"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))
gpt.add_example(Example('Q',
                        'response = df[df["action"] == "Q"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))
gpt.add_example(Example('pending',
                        'response = df[df["action"] == "Q"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))

# 600MHz file query

gpt.add_example(Example('600MHz',
                        'response = df[df["rsc"] == "WT"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))

# De Facto Transfer Lease
gpt.add_example(Example('Show me the details of De Facto Transfer Leases',
                        'response = df[df["type"] == "De Facto Transfer Lease"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))
gpt.add_example(Example('De Facto Transfer Lease',
                        'response = df[df["type"] == "De Facto Transfer Lease"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))

# Educational
gpt.add_example(Example('Educational',
                        'response = df[df["rsc"] == "ED"][["assignee", "purpose", "type", "assignor", "transferor", "transferee", "lessee", "licensee", "sublessee", "file_number", "rsc", "call_sign", "action_date", "action"]]\nprint(json.dumps(response.to_dict(orient="records")))'))

x = gpt.get_top_reply(query)
# print(x)
splitted = x.split("output: ")
length = len(splitted)

pdCode = splitted[length-1]


def run_query(code):
    exec(code)


run_query(pdCode)
