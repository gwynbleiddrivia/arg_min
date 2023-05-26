import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('max_colwidth',400)
import random
from itertools import repeat
from nltk import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stop_words = stopwords.words("english") + [",",":",";","(",")","{","}","[","]","AB","TRIAL","BACKGROUND","CONCLUSION","METHOD","RESULT","REGISTRATION","FUNDING","PURPOSE"]
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

class dtpr:


	def strings_in_a_list(self,txt): 
		text = open(txt,'r')
		nobreak = '\n'.join(text.readlines())
		iron = nobreak.replace('\n',' ')
		iron = iron.replace("AB  -",". AB  -")
		iron = iron.replace("FAU  -",". FAU  -")
		iron = iron.replace("CI  -",". CI  -")
		sent = sent_tokenize(iron)
		without_gap = [n.strip() for n in sent]
		without_period = [na.strip(".") for na in without_gap]
		str_lis = [' '.join(nam.split()) for nam in without_period]
		return str_lis


	def filtered(self,txt):
		lis = []
		switchh = False
		for string in txt:
			if switchh == False:
				if string[:5] == "PMID-":
					pmid = string[6:14]
				elif string[:4] == "AB -":
					switchh = True
					lis.append("pmid:"+pmid+"~ "+string)
				else:
					continue
			elif switchh == True:
				if string[:5] == "PMID-":
					pmid = string[6:14]
				elif string[:5] == "FAU -" or string[:4] == "CI -":
					switchh = False
					continue
				else:
					lis.append("pmid:"+pmid+"~ "+string)
		for nam in lis:
			if nam[-2:] == "~ ":
				lis.remove(nam)
		return lis
 
	def stopp(self,string):
		return ''.join([word+" " for word in word_tokenize(string) if word not in stop_words])


	def lemma(self,string):
		return ''.join([lemmatizer.lemmatize(word)+" " for word in word_tokenize(string)])



	def stemm(self,string):
		return ''.join([ps.stem(word)+" " for word in word_tokenize(string)])


	def get_dummies(self):
		#These are dummy data for mow
		#NMCE
		#NonArgument --> 0
		#MajorClaim --> 1
		#Claim --> 2
		#Evidence --> 3
		NonArg, MajorClaim, Claim, Evidence = "0","1","2","3"
		N,M,C,E = [],[],[],[]
		N.extend(repeat(NonArg,25150))
		M.extend(repeat(MajorClaim,25147))
		C.extend(repeat(Claim,25147))
		E.extend(repeat(Evidence,25147))
		A = N+M+C+E
		random.shuffle(A)
		return A
		
	
	
	
	def stop_stem_lemma(self,txt):
		corpora = dtpr().strings_in_a_list(txt)
		filtered = dtpr().filtered(corpora)
		stopped = [dtpr().stopp(sent) for sent in filtered]
		lemmed = [dtpr().lemma(sent) for sent in stopped]
		stemmed = [dtpr().stemm(nam) for nam in lemmed]
		#return stemmed
		return filtered

	def all_files(self):
		files = ['lung_neoplasms.txt','breast_neoplasms.txt','hepatocellular_carcinoma(liver_cancer).txt','pancreatic_neoplasms.txt','prostatic_neoplasms.txt','colonic_neoplasms.txt','ovarian_neoplasms.txt','gastrointestinal_neoplasms.txt','leukemia.txt','stomach_neoplasms.txt','myeloma.txt']
		lis, temp, main_list = [],[],[]
		for txt in files:
			lis.append([txt +" "+sent for sent in dtpr().stop_stem_lemma(txt)])
		lis = sum(lis,[])
		return lis

	def dataframe(self):
		corpora = dtpr().all_files()
		main_list = corpora
		text = [' '.join(sent.split()[2:]) for sent in main_list]
		disease = [sent.split()[0][:-4] for sent in main_list]
		pmid = [sent.split()[1][5:-1] for sent in main_list]
		dummies_df = pd.DataFrame({'dummies':dtpr().get_dummies()})
		dummies_df.to_excel('dummies.xlsx')
		dummies = pd.read_excel('dummies.xlsx')
		data =  {'pmid':pmid,
			'disease':disease,
			'text':text}
		tabularasa = pd.DataFrame(data)
		tabularasa.drop_duplicates(subset="text",keep="first",inplace=True,ignore_index=True)
		tabularasa['annotation'] = dummies_df['dummies']
		tabularasa['words'] = [len(x.split()) for x in tabularasa['text'].tolist()]
		tabularasa.to_excel('tabularasa.xlsx',index=False)
		#return tabularasa.describe(), tabularasa.info()
		return tabularasa

if __name__ == "__main__":
	#txt = dtpr().all_files()
	#print(dtpr().stop_stem_lemma(txt),dtpr().dummies())
	#print(dtpr().strings_in_a_list(txt))
	#print(dtpr().dataframe())
	data = dtpr().dataframe()
	#data.text.str.split().map(lambda x: len(x)).hist()
	#print(data.text.str.split().map(lambda x: len(x)))
	sns.histplot(data = data,x = 'words',bins = 10)
	plt.show(block=True)
#pattern = r"^([A-Z^:][A-Z^:]*):"
