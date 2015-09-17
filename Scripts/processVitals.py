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

# Make sure only have those terms above
def process_file(file_name, vital_type = ["Systolic", "Diastolic", "Weight", "BMI"]):
   # Generate list of list from input file
   lol = list(csv.reader(open(file_name, 'rb'), delimiter='\t'))

   vitals = dict()

   # Patient : Date : Score
   for stat in vital_type:
      vitals[stat] = [(line[0], line[2], line[4]) for line in lol if (line[1] == stat)]

   # print vitals
   return vitals

def generate_patient_vitals(patient_records, vitals):
   # Process each vital - add to patient record
   for vital_type in vitals.keys():
      for record in vitals[vital_type]:
         patient_id = record[0].split("-")[1]
         patient_dict = patient_records[patient_id]

         if vital_type not in patient_dict.keys():
            patient_dict[vital_type] = list()
        
         score = record[1]
         date_stamp = record[2]
         #print "data is", patient_id, date_stamp, score
         patient_dict[vital_type].append((date_stamp,score))

# 2012-07-11
def get_date(record):
   return datetime.strptime(record[0], "%Y-%m-%d")

def sort_timeline(record_list):
   return sorted(record_list, key=get_date, reverse=False)

def sort_all_types_patient_timelines(patient_records):
   for patient in patient_records: 
      patient_dict = patient_records[patient]
      for vital_type in patient_dict: 
         #print vital_type
         patient_dict[vital_type] = sort_timeline(patient_dict[vital_type])

def output_json_patient_timelines(patient_data, outfile_name="output.json"):
   with open(outfile_name, 'w') as outfile:
       json.dump(patient_data, outfile)

def process_patient_vitals(input_file, output_file=None):
   # Generate a patient oriented dictionary
   records = defaultdict(dict)

   if (input_file != "ALL"):
      generate_patient_vitals(records, process_file(input_file))
   else:
      for input_file in glob.glob("??????_?"):
          generate_patient_vitals(process_file(input_file))

   sort_all_types_patient_timelines(records)

   if output_file != None:
      output_json_patient_timelines(records, output_file)

def main_vitals():
   parser = argparse.ArgumentParser(description='Parsing')
   parser.add_argument('input_file', help="Need an input file")
   parser.add_argument('output_file', default="output.json", nargs='?')

   # Args parsing
   args = parser.parse_args()
   input_file = args.input_file
   output_file = args.output_file

   # Process patient
   process_patient_vitals(input_file, output_file)

if __name__ == "__main__":
   main_vitals()
