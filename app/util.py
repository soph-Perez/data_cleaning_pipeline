import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename
import sys

# allows users to select which xlsx file to work on
def selectFile():
  file_path = askopenfilename(title="Select the Excel file: ")
  try:
    if not file_path.lower().endswith(".xlsx"):
      raise ValueError("Invalid file type. Program expects .xlsx files")
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    print(file_path)
  except ValueError as e:
    print("Error: ", e)
    sys.exit()
  return all_sheets

# allows user to select which tab on the spreadsheet to work on
def selectSheet(all_sheets):
  access_sheet = input("Enter sheet name (enter 'default' if not applicable): ").lower()
  try:
    if access_sheet == "default":
      df_raw = next(iter(all_sheets.values()))
    else:
      if access_sheet not in (name.lower() for name in all_sheets.keys()):
        raise ValueError("Invalid sheet name")
      else:
        df_raw = all_sheets[[name for name in all_sheets if name.lower() == access_sheet][0]]
  except Exception as e:
    print("Error: ", e)
    sys.exit()
  return df_raw

# finds header and makes a suggestion
def headerDetector(df_raw):
  try:
    best_score = float("-inf")
    best_row_index = None
    
    for i, row in df_raw.head(15).iterrows():
      score = 0
      row_list = list(row)
      for data in row_list:
        if pd.isna(data):
          score -= 2
        if isinstance(data, str):
          score +=2
        if isinstance(data, (int, float)):
          score -=1

      duplicate_count = len(row_list) - len(set(row_list))
      score -=2*duplicate_count

      # print(f"Row: {i}, Score: {score}")

      if score > best_score:
        best_score = score
        best_row_index = i
    return best_row_index
  except Exception as e:
    print("Error in header detection: ", e)
    return None

# confirm that the assumed header is right 
def confirmHeader(df_raw, best_row_index):
  assumed_header = df_raw.iloc[best_row_index]
  confirm_user = input(f"Does this row contain the header: \n{assumed_header.tolist()}? \n(Reply 'Y' for Yes and 'N' for No): ").lower()
  while(True):
    if confirm_user == "y":
      print(assumed_header)
      df_raw.columns = assumed_header
      return True
    elif confirm_user == "n":
      print("User rejected assumed header.")
      askUser(df_raw)
      return False
    else:
      print("Invalid input. Please enter only 'Y' or 'N'.") 

# if the assumed header is incorrect, allow the user to input the correct one
def askUser(df_raw):
  while(True):
    try:
      ask_user = int(input("Enter the row containing the header: "))
      user_header = df_raw.iloc[ask_user]

      confirm = input(f"Is this correct? {user_header.tolist()} (y/n): ").lower()
      if confirm == "y":
        df_raw.columns = user_header
        return user_header
      else:
        print("Try again.\n")
    except ValueError:
      print("Invalid input. Enter a whole number row value.")
      ask_user = input("Enter the row containing the header: ")