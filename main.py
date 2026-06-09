from app.util import selectFile, selectSheet, headerDetector, confirmHeader
def main():
  all_sheets = selectFile()
  df_raw = selectSheet(all_sheets)
  best_row_index = headerDetector(df_raw)
  confirmHeader(df_raw, best_row_index)
if __name__ == "__main__":
  main()