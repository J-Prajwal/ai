import pandas as pd
import json


# Transfer / assignment / leases
try:
    df1 = pd.read_csv("./data/transfer_accepted_for_filing.csv")
    df2 = pd.read_csv("./data/transfer_action.csv")
    transfer_accepted_for_filing = len(df1)
    ta_action_counts = [df2["action"].value_counts().to_dict()]
    total_transfer_actions_count = 0
    for i in ta_action_counts:
          key = list(i.keys())[0]
          total_transfer_actions_count += i[key]
except Exception as e:
     print(f"An error occurred in transfer: {e}")

# Market based
try:
     df3 = pd.read_csv("./data/market_accepted_for_filing.csv")
     df4 = pd.read_csv("./data/market_action.csv")
    #  df5 = pd.read_csv("./data/market_termination_pending.csv")
     markert_accepted_for_filing = len(df3)
     ma_action_counts = [df4["action"].value_counts().to_dict()]
     total_market_actions_count = 0
     for i in ma_action_counts:
          key = list(i.keys())[0]
          total_market_actions_count += i[key]
except Exception as e:
     print(f"an error occurred in market: {e}")

# Of Interest


# Site based
try:
     df5 = pd.read_csv("./data/site_accepted_for_filing.csv")
     df6 = pd.read_csv("./data/site_action.csv")
     df7 = pd.read_csv("./data/site_termination_pending.csv")
     Site_accepted_for_filing = len(df5)
     Site_pending = len(df7)
     Site_action = len(df6)
     sb_action_counts = [df6["action"].value_counts().to_dict()]
     total_site_action_counts = 0
     for i in sb_action_counts:
          key = list(i.keys())[0]
          total_site_action_counts += i[key]
except Exception as e:
     print(f"an error occurred in site: {e}")


response = {"transfer_accepted_for_filing": transfer_accepted_for_filing,
            "transfer_actions": ta_action_counts, "total_transfer_action": total_transfer_actions_count,"market_accepted_for_filing": markert_accepted_for_filing,
            "market_actions": ma_action_counts, "total_market_action": total_market_actions_count,"site_accepted_for_filing": Site_accepted_for_filing,
            "site_action": sb_action_counts, "total_Site_action": Site_action, "site_pending": Site_pending}


print(json.dumps(response))

