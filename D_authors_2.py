# This is Object Oriented Programming (OOP) format of D_Authors.py File

import xmltodict
import pandas as pd


class Author:
    # Converting xml databank file to dictionary
    def read_file (self, xml_file):
        with open(xml_file,"r") as xml_obj:
            self.my_dict = xmltodict.parse(xml_obj.read())
            xml_obj.close()
            
    # Extracting first and last name of authors of each article
    def get_authors (self):
        N_Articles = len(self.my_dict['MedlineCitationSet']['Article'])
        self.articles   = []
        self.authorsdb  = []
        # Extract authors of each article
        for a in range(N_Articles):
            self.authors = []
            N_Authors  = len(self.my_dict['MedlineCitationSet']['Article'][a]['AuthorList']['Author'])
            # Extract first and last names of each author
            for au in range(N_Authors):
                LN = self.my_dict['MedlineCitationSet']['Article'][a]['AuthorList']['Author'][au]['LastName']
                FN = self.my_dict['MedlineCitationSet']['Article'][a]['AuthorList']['Author'][au]['ForeName']        
                self.authors.append(LN + ", " + FN)
                self.authorsdb.append(LN + ", " + FN)
            self.articles.append(self.authors)
            
        # Sort authors db
        self.authorsdb = sorted(list(set(self.authorsdb)))
        
    # Searching all authors in all articles 
    def authors_matrix (self):
        self.MAT = []
        for i in self.articles:
            mat = []
            for ii in self.authorsdb:
                if ii in i:
                    mat.append('1')
                if ii not in i:             
                    mat.append('0')
            self.MAT.append(mat)

         
    # Making Dataframe and co-occurance for authors in pandas
    def coocc_matrix (self):
        df = pd.DataFrame(self.MAT, columns=self.authorsdb)
        df_asint = df.astype(int)
        self.coocc = df_asint.T.dot(df_asint)
        
        
# Running Class with example file 'Data.xml'        
test = Author()
test.read_file('Data.xml')
test.get_authors()
test.authors_matrix()
test.coocc_matrix()
print(test.coocc)
