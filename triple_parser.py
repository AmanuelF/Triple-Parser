#!/usr/bin/python

import re
import pandas as pd
import json

def parse(filepath):
	df = pd.read_csv(filepath)
	columns = df.columns
	df_ = pd.DataFrame(columns=columns)
	for i,row in df.iterrows():
		REL_indices = list()  #list of indices of relations in a string
		for item in row[3].split(': '):
			if 'REL ' in item:
				REL_indices.append(row[3].split(': ').index(item))
		predicates = list()
		for rel_idx in REL_indices:
			predicates.append(row[3].split(': ')[rel_idx])
        
		REL_idx_first = REL_indices[0]
		REL_idx_last = REL_indices[len(REL_indices)-1]
        
		subjects = row[3].split(': ')[:REL_idx_first]
        
		objects = row[3].split(': ')[REL_idx_last+1:]

		for subj in subjects:
			for obj in objects:
				for pred in predicates:
					subj = re.sub(r'ARG[0-9]', '', subj)
					obj = re.sub(r'ARG[0-9]', '', obj)
					predicate = re.sub(r'REL ', '', pred)
					df_ = df_.append({'tweet_id':row[0], 'date_time':row[1], 'tweet_text':row[2], 'subject': subj.strip(), 'predicate':predicate , 'object': obj.strip()}, ignore_index=True)
    
	return df_.drop(columns='tuples_clean')


df_parsed = parse('cleantuples.csv')

column_order = ['tweet_id','date_time','tweet_text','subject','predicate','object']

df_parsed = pd.DataFrame(df_parsed, columns=column_order)

df_parsed.to_csv('swati_cleantuples_10192019.tsv', sep='\t', index=False)

