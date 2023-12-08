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

df1 = pd.read_csv("./data/transfer_action.csv")
df2 = pd.read_csv("./data/transfer_accepted_for_filing.csv")

df3 = pd.read_csv("./data/market_accepted_for_filing.csv")

df5 = pd.read_csv("./data/site_accepted_for_filing.csv")
df6 = pd.read_csv("./data/site_termination_pending.csv")

df7 = pd.read_csv("./data/market_action.csv")
df8 = pd.read_csv("./data/site_action.csv")

gpt.add_example(Example('Transfers/Assignments/Spectrum Leases Accepted for Filing',
                        'print(json.dumps(df2.to_dict(orient="records")))'))
gpt.add_example(Example('Transfer Leases Accepted for Filing',
                        'print(json.dumps(df2.to_dict(orient="records")))'))
gpt.add_example(Example('Spectrum Leases Accepted for Filing',
                        'print(json.dumps(df2.to_dict(orient="records")))'))

gpt.add_example(Example('Transfers/Assignments/Spectrum Leases Action',
                        'print(json.dumps(df1.to_dict(orient="records")))'))
gpt.add_example(Example('Transfer Leases Action',
                        'print(json.dumps(df1.to_dict(orient="records")))'))
gpt.add_example(Example('Spectrum leases action',
                        'print(json.dumps(df1.to_dict(orient="records")))'))

gpt.add_example(Example('Market-based Action',
                        'print(json.dumps(df7.to_dict(orient="records")))'))
gpt.add_example(Example('Market based Action',
                        'print(json.dumps(df7.to_dict(orient="records")))'))
gpt.add_example(Example('Market action',
                        'print(json.dumps(df7.to_dict(orient="records")))'))

gpt.add_example(Example('Market-based Accepted for Filing',
                        'print(json.dumps(df3.to_dict(orient="records")))'))
gpt.add_example(Example('Market based Accepted for Filing',
                        'print(json.dumps(df3.to_dict(orient="records")))'))
gpt.add_example(Example('Market accepted for filing',
                        'print(json.dumps(df3.to_dict(orient="records")))'))

gpt.add_example(Example('Market-based License Termination Pending',
                        'print("no record found")'))
gpt.add_example(Example('Market based License Termination Pending',
                        'print("no record found")'))
gpt.add_example(Example('Market license termination pending',
                        'print("no record found")'))

gpt.add_example(Example('Site-based Action',
                        'print(json.dumps(df8.to_dict(orient="records")))'))
gpt.add_example(Example('Site based Action',
                        'print(json.dumps(df8.to_dict(orient="records")))'))
gpt.add_example(Example('Site action',
                        'print(json.dumps(df8.to_dict(orient="records")))'))

gpt.add_example(Example('Site-based Accepted for Filing',
                        'print(json.dumps(df5.to_dict(orient="records")))'))
gpt.add_example(Example('Site based Accepted for Filing',
                        'print(json.dumps(df5.to_dict(orient="records")))'))
gpt.add_example(Example('Site accepted for filing',
                        'print(json.dumps(df5.to_dict(orient="records")))'))

gpt.add_example(Example('Site-based License Termination Pending',
                        'print(json.dumps(df6.to_dict(orient="records")))'))
gpt.add_example(Example('Site based License Termination Pending',
                        'print(json.dumps(df6.to_dict(orient="records")))'))
gpt.add_example(Example('Site license termination pending',
                        'print(json.dumps(df6.to_dict(orient="records")))'))


x = gpt.get_top_reply(query)

splitted = x.split("output: ")
length = len(splitted)

pdCode = splitted[length-1]


def run_query(code):
    exec(code)


run_query(pdCode)
