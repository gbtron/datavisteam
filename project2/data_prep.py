import pandas as pd
import ast
hometown_data = pd.read_csv("raw_data/hometowns.csv")
hometown_data.columns =  [x.replace("\ufeff","") for x in list(hometown_data.columns)]
just_for_towns_cols = ["Artist Name", "Latitude", "Longitude", "City", "Country Edited", "State Edited", "Region"]
hometown_data2 = hometown_data[just_for_towns_cols].drop_duplicates(subset=["Artist Name", "City", "Country Edited", "State Edited", "Region"])
hometown_data2.columns = ['Artist_Name', 'Latitude', 'Longitude', 'City', 'Country', 'State', "Region"]
hometown_data2 = hometown_data2[hometown_data2.Country == "United States"]
hometown_data2.to_csv("data/hometowns.csv",index=False)

hometown_data3 = hometown_data[['Song Title', 'Artist Name', 'Unique ID', 'Year', 'Peak Position', 'Genre 1']].drop_duplicates()
hometown_data3 = hometown_data3.rename(columns={"Artist Name": "Performer", "Peak Position":"Peak_Position","Song Title":"Song", 'Unique ID':'SongID'})
hometown_data3_noPeak = hometown_data3.drop("Peak_Position",axis=1).drop_duplicates()
hometown_data3_peak = hometown_data3.groupby(['Song', 'Performer', 'SongID', 'Year', 'Genre 1'],as_index=False)["Peak_Position"].min()
hometown_data3 = hometown_data3_noPeak.merge(hometown_data3_peak)

hometown_data3['genre_larger'] = hometown_data3['Genre 1'].apply(lambda x: "rap" if "rap" in x 
	else ("latin" if "latin" in x 
	else ("country" if "country" in x 
	else ("hip hop" if "hip hop" in x 
	else ("rock" if "rock" in x 
	else ("pop" if "pop" in x else x))))))

hometown_data3 = hometown_data3[((hometown_data3.Year>=2000) & (hometown_data3.Year<=2015))]
hometown_data3.to_csv("data/billboard_hits.csv",index=False)
