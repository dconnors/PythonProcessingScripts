#!/usr/bin/python

# System control
import argparse

# Processing
import math
import numpy as np

# File IO
import csv
import json
import os
import glob

# Date/time
from datetime import datetime
from datetime import date

# Data structure
from collections import defaultdict

#Plotting
import matplotlib.pyplot as plt



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def calculate_age(born_year):
    today = date.today()
    return today.year - born_year

def process_file(demographics, file_name):
   # Generate list of list from input file
   lol = list(csv.reader(open(file_name, 'rb'), delimiter='\t'))

   # Patient : Date : Score
   for line in lol:
      # Don't split patient ID until later
      patient_id = line[0].split("-")[1]
      #patient_id = line[0]
      gender = (line[2] == "Male")
      state = line[3]
      zip = line[4]
      if (not is_number(line[1])):
         continue
      age = calculate_age(int(line[1]))
      demographics[patient_id] = (age,gender,state,zip)


# alternative : dict((k, v) for (k, v) in somedict.iteritems() if not k.startswith('someprefix'))
def filter_demographics(demographics, filter_age=None, filter_gender=None, filter_zip=None):

   records = dict()
   # age, gender, state, zip
   for id in demographics: 
      if (filter_age != None):
         age = demographics[id][0]
         if (not (filter_age[0] <= age and age < filter_age[1])):
            continue

      if (filter_gender != None):
         gender = demographics[id][1]
         if (gender !=  filter_gender):
            continue

      if (filter_zip!= None):
         zip = demographics[id][3]
         if (zip !=  filter_zip):
            continue
             
      records[id] = demographics[id]
   return records 

def process_demographics(input_file):
   demographics = dict()
   if (input_file != "ALL"):
      process_file(demographics, input_file)
   else:
      for input_file in glob.glob("??????_?"):
         process_file(demographics, input_file)
   return demographics

def output_json_file(data, outfile_name="output.json"):
   with open(outfile_name, 'w') as outfile:
      json.dump(data, outfile)

def main_Demographics():
   parser = argparse.ArgumentParser(description='Parsing')
   parser.add_argument('input_file', help="Need an input file")
   parser.add_argument('output_file', default=None, nargs='?')

   args = parser.parse_args()
   input_file = args.input_file
   output_file = args.output_file

   demographics = process_demographics(input_file) 

   # Example filtering
   #records = filter_demographics(demographics, filter_age=[50,80])
   records = filter_demographics(demographics)

   if (output_file):
      output_json_file(records, output_file)
   else:
      print len(records)  

if __name__ == "__main__":
   main_Demographics()
