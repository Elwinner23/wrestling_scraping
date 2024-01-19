# importing the required modules
import glob
import pandas as pd

# specifying the path to csv files
path = r"C:\Users\TARIEL\Desktop\wrestling_scraping"

# csv files in the path
file_list = glob.glob(path + "/*.xlsx")

# list of excel files we want to merge.
# pd.read_excel(file_path) reads the excel
# data into pandas dataframe.
excl_list = []

for file in file_list:
	excl_list.append(pd.read_excel(file))

# create a new dataframe to store the 
# merged excel file.
excl_merged = pd.DataFrame(columns = ['tournament_name','tournament_date',
                             'style' , 'stage', 'weight', 'opponent1',
                             'opponent1_country',
                             'opponent1_points','opponent2_points',
                             'opponent2','opponent2_country',
                             'decision','links'])

for excl_file in excl_list:
	
	# appends the data into the excl_merged 
	# dataframe.
	excl_merged = pd.concat(excl_list, ignore_index=True)

# exports the dataframe into excel file with
# specified name.
excl_merged.to_excel('meeting.xlsx', index=False)
