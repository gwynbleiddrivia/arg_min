import pandas as pd
df = pd.read_excel('lung_neoplasms_seqcls.xlsx')
checklist = []
tabularasa = pd.DataFrame()
target = []
for pmid in df['pmid']:
	if pmid not in checklist:
		checklist.append(pmid)
		limit = df[df['pmid']==pmid]['count'].values[0]
		#print(limit)
		df_abs = df[df['pmid']==pmid]
		for n in range(limit):
			target = df_abs['text'].values[n]
			target_group = df_abs[df_abs['text']==target]['ann_group'].values[0]
			#df_abs['target'] = target * (limit-(n+1))
			df_abs['target'] = target
			df_abs['target_group'] = target_group
			first = df_abs.pop('target')
			second = df_abs.pop('target_group')
			df_abs.insert(2,'target', first)
			df_abs.insert(3,'target_group', second)
			temp = df_abs[n+1:]
			tabularasa = tabularasa.append(temp)
			df_abs = df_abs[0:]
	else:
		continue
#tabularasa['target'] = target

print(tabularasa)
tabularasa.to_excel('lung_neoplasms_relcls.xlsx')
