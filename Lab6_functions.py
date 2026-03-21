import pandas as pd

def sundowner_data_loader(url_base):
    # This formats the url headers and combines all of the data for each day in February into one dataframe
    # Can select range of years and range of days in the month
    # This function is for February, but the 
    years = []
    month = 2 # February

    for year in range(21,27):
        for day in range(1,29): # This range and the url can be changed for whatever days corresponding to a given month 
            url = f"{url_base}20{year}{month:02d}{day:02d}.txt" # Just had to look up a bunch of stuff for this, I didn't know what :02d was
            df = pd.read_fwf(url, header=[0, 1], skiprows=[2])
            date_col = [c for c in df.columns if c[1] == "Date"][0]
            time_col = [c for c in df.columns if c[1] == "Time"][0]
            t = (
                df[time_col]
                .astype(str)
                .str.strip()
                .str.replace(r"a$", "AM", regex=True)
                .str.replace(r"p$", "PM", regex=True)
            )

            dt = pd.to_datetime(
                df[date_col].astype(str).str.strip() + " " + t,
                format="%m/%d/%y %I:%M%p",
                errors="coerce",
            )

            df = df.set_index(dt).drop(columns=[date_col, time_col])
            df.index.name = "datetime"

            df.columns = [
                "_".join([str(a).strip(), str(b).strip()]).replace(" ", "_").strip("_")
                for a, b in df.columns
            ]
            if df.empty:
                pass
            else:
                years.append(df) # Source: https://www.geeksforgeeks.org/python/pandas-concat-function-in-python/

    month_df = pd.concat(years) # Source: https://www.geeksforgeeks.org/python/pandas-concat-function-in-python/
    month_df = month_df[pd.notna(month_df.index)]
    month_df = month_df.sort_index()
    month_df = month_df[~month_df.index.duplicated(keep='first')] # https://stackoverflow.com/questions/13035764/remove-pandas-rows-with-duplicate-indices
    return month_df