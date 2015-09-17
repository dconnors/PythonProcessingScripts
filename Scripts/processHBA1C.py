#!/usr/bin/python

import math
import argparse
import numpy as np
import csv
import json
import os
import glob

from datetime import datetime

from collections import defaultdict

import matplotlib.pyplot as plt

def print_enumerated_list(type_name, record_list):
   for i,h in enumerate(record_list):
      print type_name, i,h

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def filter_file(file_name):
   lol = list(csv.reader(open(file_name, 'rb'), delimiter='\t'))
   for line in lol:
      print line[2]

def process_file(file_name):

   elim_terms = ["POC GLYCOHEMOGLOBIN A2C"]
   eliminate_terms =[item.lower() for item in elim_terms]

   # Build search terms
   orig_terms = [
       "%A1C",
       "%HBA1C",
       "*HGB A1C (glycohemoglobin) 83036",
       "A1C",
       "A1C%",
       "A1C% (DCA)",
       "CLIA WAIVE HGA1C",
       "DCA Glycosylated Hgb A1c",
       "Estim. Avg Glu (eAG)",
       "GLYCATED HEMOGLOBIN A1C",
       "GLYCO HGB (A1C) *",
       "GLYCO HGB (In House)",
       "GLYCOHEMOGLOBIN",
       "GLYCOHEMOGLOBIN (A1C)",
       "GLYCOHEMOGLOBIN A1C",
       "GLYCOSYLATED HEMOGLOBIN TEST",
       "Glyco HGB",
       "Glycosylated Hemoglobin",
       "Glycosylated Hemoglobin A1c",
       "Glycosylated Hgb A1c",
       "HA1C",
       "HA1C (Historical)",
       "HB A1C",
       "HBA1C",
       "HEMOGLOBIN",
       "HEMOGLOBIN A1C",
       "HEMOGLOBIN A1C (GLYCOHEMOGLOB)",
       "HEMOGLOBIN A1C (IN-HOUSE)",
       "HEMOGLOBIN A1C (L)",
       "HEMOGLOBIN A1C - IN OFFICE",
       "Hemoglobin A1C  (in office)",
       "HEMOGLOBIN A1C GLYH",
       "HEMOGLOBIN A1C(A1C5)",
       "HEMOGLOBIN A1C.",
       "HEMOGLOBIN GLYCLATED (HGB A1C)",
       "HEMOGLOBIN GLYCLATED (HGB A1C) in house",
       "HEMOGLOBIN GLYCLATED (HGB A1C) outside",
       "HGB A1C",
       "HGB A1C  (Tosoh G8)",
       "HGB A1C (FS AT PREMIER)",
       "HGB A1C (HEMOGLOBIN:  GLYCOSYLATED)",
       "HGB A1C (In Office)",
       "HGB A1C (Lab Corp)",
       "HGB A1C (in-house)",
       "HGB-AT10",
       "HGBA1C",
       "HGBA1C_D",
       "Hb A1c Diabetic Assessment",
       "HbA1C%",
       "Hemoglobin (A1C)",
       "Hemoglobin A1c (Labcorp: 001453)",
       "Hemoglobin A1c - 001464",
       "HgB",
       "Hgb A1C (496)",
       "MOAM (HGB A1C)",
       "POC GLYCOHEMOGLOBIN A1C",
       "RAPID A1C",
       "_HA1C"]

   search_terms = [term.lower() for term in orig_terms]

   #search_terms.sort(lambda x,y: cmp(len(x), len(y)), reverse=True)
   # Process lines
   lol = list(csv.reader(open(file_name, 'rb'), delimiter='\t'))

  
   # Make sure only have those terms above
   records = [line for line in lol if (any (s in line[2].lower() for s in search_terms))]


   # Only use scores from fields that have a 90% valid value rate and at least 100 entries
   support = dict()
   values = dict()
   for search in search_terms:
      support[search] = [line for line in records if (line[2].lower() == str(search))]
      base = [line for line in support[search] if (is_number(line[3]) and line[3] != "0")]
      base_zero = [line for line in support[search] if (is_number(line[3]) and line[3] == "0")]
      base_null = [line for line in support[search] if (not is_number(line[3]))]
      #print search, ":", len(support[search]), ":", len(base), len(base_zero), len(base_null)
      #if ( len(base) > 10 and float(len(base)) / len (support[search]) > .90):
      #     values[search] = base
      values[search] = base

   return values

def generate_patient_timelines(values):
   # Generate a patient oriented dictionary
   patient_records = defaultdict(list)
   for key in values.keys():
      for record in values[key]:
         patient_id = record[0].split("-")[1]
         date_stamp = record[1]
         score = record[3]
         patient_records[patient_id].append((date_stamp,score))
         #print patient_id, date_stamp, score
   return patient_records

# 2012-07-11
def get_date(record):
   return datetime.strptime(record[0], "%Y-%m-%d")

def sort_timeline(record_list):
   return sorted(record_list, key=get_date, reverse=False)

def sort_patient_timelines(patient_records):
   for patient in patient_records: 
      patient_records[patient] = sort_timeline(patient_records[patient])

def print_patient_timelines(patient_records, num_points=2):
   # Filter based on number of records
   ids = [patient for patient in patient_records if (len(patient_records[patient]) >= num_points)]
   for id in ids: 
      print id, ":", len(patient_records[id]), ":", sort_timeline(patient_records[id])

def output_json_patient_timelines(patient_data, outfile_name="output.json"):
   with open(outfile_name, 'w') as outfile:
       json.dump(patient_data, outfile)

def process_file_list():
   # Read all of the files
   file_records = dict()
   for input_file in glob.glob("??????_?"):
      # generate patient values
      file_records[input_file] = generate_patient_timelines(process_file(input_file))

   # combine judgement 
   super_dict = defaultdict(list)
   for d in file_records:
      for k, v in file_records[d].iteritems():
         for item in v:
            super_dict[k].append(item)

   # super  
   return super_dict

def process_hba1c(input_file, output_file):
   if (input_file != "ALL"):
      records = generate_patient_timelines(process_file(input_file))
   else:
      records = process_file_list()

   sort_patient_timelines(records)
   #print_patient_timelines(records)
   output_json_patient_timelines(records, output_file)

def main_HBA1C():
   parser = argparse.ArgumentParser(description='Parsing')
   parser.add_argument('input_file', help="Need an input file")
   parser.add_argument('output_file', default="output.json", nargs='?')
   args = parser.parse_args()

   input_file = args.input_file
   output_file = args.output_file
   process_hba1c(input_file, output_file)

if __name__ == "__main__":
   main_HBA1C()
