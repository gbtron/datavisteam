import pandas as pd
import ast
hometown_data = pd.read_csv("raw_data/hometowns.csv")
hometown_data.columns =  [x.replace("\ufeff","") for x in list(hometown_data.columns)]
just_for_towns_cols = ["Artist Name", "Latitude", "Longitude", "City", "Country Edited", "State Edited", "Region"]
hometown_data = hometown_data[just_for_towns_cols].drop_duplicates(subset=["Artist Name", "City", "Country Edited", "State Edited", "Region"])
hometown_data.columns = ['Artist_Name', 'Latitude', 'Longitude', 'City','Country','State', "Region"]
hometown_data = hometown_data[hometown_data.Country == "United States"]
hometown_data.to_csv("data/hometowns.csv",index=False)

spotify_hits = pd.read_csv("raw_data/Hot_Stuff.csv")
spotify_hits["Year"] = spotify_hits.WeekID.apply(lambda x: x[-4:])
spotify_hits = spotify_hits[spotify_hits.Year >= "2000"]
spotify_hits["Month"] = spotify_hits.WeekID.apply(lambda x: x.split("/")[0])
peakpos =  spotify_hits[['Peak Position',"SongID"]]
peakpos = peakpos.groupby("SongID", as_index=False)["Peak Position"].min()
spotify_hits = spotify_hits[['Song', 'Performer', 'SongID', 'Year']].drop_duplicates()
spotify_hits = spotify_hits.merge(peakpos)
spotify_hits.to_csv("data/spotify_hits.csv",index=False)

spotify_feat = pd.read_csv("raw_data/Hot_100_Audio_Features.csv")
set_of_songs = list(set(spotify_hits.SongID))
spotify_feat = spotify_feat[spotify_feat.SongID.isin(set_of_songs)]
spotify_feat["spotify_genre"] = spotify_feat.spotify_genre.apply(lambda x: ast.literal_eval(x) if type(x)==str else [])

glist = list(spotify_feat['spotify_genre'])
flat_list = [item for sublist in glist for item in sublist]
gcounts = {x:flat_list.count(x) for x in set(flat_list)}
gcounts = {k: v for k, v in sorted(gcounts.items(), key=lambda item: item[1])}

l = []
for g in glist:
	best_genre = ""
	max_cnt = 0
	for gen in g:
		if gcounts[gen] > max_cnt:
			max_cnt = gcounts[gen]
			best_genre = gen
	l.append(best_genre)

spotify_feat["genre"] = l
spotify_feat["genre_larger"] = spotify_feat["genre"].apply(lambda x: "rap" if "rap" in x 
	else ("country" if "country" in x 
	else("hip hop" if "hip hop" in x 
	else("rock" if "rock" in x 
	else("r&b" if "r&b" in x 
	else("jazz" if "jazz" in x 
	else ("reggaeton" if "reggaeton" in x 
	else ("christian" if "christian" in x 
	else ("christian" if "gospel" in x  
	else ("children" if "children" in x 
	else ("children" if "kids" in x 
	else ("country" if "adult standards" in x 
	else ("folk" if "folk" in x 
	else ("soul" if "soul" in x 
	else ("house" if "house" in x 
	else ("reggae" if "reggae" in x 
	else ("blues" if "blues" in x 
	else ("metal" if "metal" in x 
	else("pop" if "pop" in x else x)))))))))))))))))))

spotify_feat.to_csv("data/spotify_features.csv",index=False)


