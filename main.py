import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename
import sys

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

def selectSheet(all_sheets):
  access_sheet = input("Enter sheet name (enter 'default' if not applicable): ").lower()
  try:
    if access_sheet == "default":
      df = all_sheets
    else:
      if access_sheet not in (name.lower() for name in all_sheets.keys()):
        raise ValueError("Invalid sheet name")
      else:
        df = all_sheets[[name for name in all_sheets if name.lower() == access_sheet][0]]
  except Exception as e:
    print("Error: ", e)
    sys.exit()

def main():
  all_sheets = selectFile()
  selectSheet(all_sheets)

if __name__ == "__main__":
  main()