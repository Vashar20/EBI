import xmltodict
import pandas as pd

# Converting xml databank file to dictionary
with open("Data.xml","r") as xml_obj:
     my_dict = xmltodict.parse(xml_obj.read())
     xml_obj.close()

# Extracting first and last name of authors of each article
N_Articles = len(my_dict['MedlineCitationSet']['Article'])
articles   = []
authorsdb  = []
# Extract authors of each article
for a in range(N_Articles):
    authors = []
    N_Authors  = len(my_dict['MedlineCitationSet']['Article'][a]['AuthorList']['Author'])
    # Extract first and last names of each author
    for au in range(N_Authors):
        LN = my_dict['MedlineCitationSet']['Article'][a]['AuthorList']['Author'][au]['LastName']
        FN = my_dict['MedlineCitationSet']['Article'][a]['AuthorList']['Author'][au]['ForeName']        
        authors.append(LN + ", " + FN)
        authorsdb.append(LN + ", " + FN)
    articles.append(authors)

authorsdb = sorted(list(set(authorsdb)))
        
# Searching all authors in all articles 
MAT = []
for i in articles:
    mat = []
    for ii in authorsdb:
        if ii in i:
            mat.append('1')
        if ii not in i:             
            mat.append('0')
    MAT.append(mat)

         
# Making Dataframe and co-occurance for authors in pandas
df = pd.DataFrame(MAT, columns=authorsdb)
df_asint = df.astype(int)
coocc = df_asint.T.dot(df_asint)
         
