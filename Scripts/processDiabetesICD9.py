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

# Make sure only have those terms above
def process_diabetes_file(diabetes_records, file_name):
   # Generate list of list from input file
   lol = list(csv.reader(open(file_name, 'rb'), delimiter='\t'))

   for record in lol:
      patient_key = record[0]
      patient_id = record[0].split("-")[1]
      icd9_code = record[1]
      dataA = record[2]
      dataB = record[3]
      dataC = record[4]
      #dataE = record[5].split(' ')[0]
      #s1 = datetime.strptime('2012-1-01', "%Y-%m-%d")
      #s2 = datetime.strptime('2014-1-01', "%Y-%m-%d")  

      if patient_id in diabetes_records:
         diabetes_records[patient_id].append(icd9_code)
      else:
         diabetes_records[patient_id] = list()
         diabetes_records[patient_id].append(icd9_code)

# 2012-07-11
def get_date(record):
   return datetime.strptime(record[0], "%Y-%m-%d")

def process_DiabetesICD9(input_file):
   diabetes_records = dict()
   if (input_file != "ALL"):
      process_diabetes_file(diabetes_records, input_file)
   else:
      for input_file in glob.glob("??????_?"):
         process_diabetes_files(diabetes_records, input_file)
   return diabetes_records

def main_DiabetesICD9():
   parser = argparse.ArgumentParser(description='Parsing')
   parser.add_argument('input_file', help="Need an input file")
   parser.add_argument('output_file', default=None, nargs='?')
   args = parser.parse_args()
   input_file = args.input_file
   output_file = args.output_file

   diabetes_records = process_DiabetesICD9(input_file)

   if output_file != None:
      summary_records = dict()
      for patient_id in diabetes_records:
         summary_records[patient_id] = 1
      with open(output_file, 'w') as outfile:
         json.dump(summary_records, outfile)
   else:
      for patient_id in diabetes_records:
         if (len(diabetes_records[patient_id]) > 1):
             print patient_id, len(diabetes_records[patient_id]),
             print diabetes_records[patient_id]

if __name__ == "__main__":
   main_DiabetesICD9()
