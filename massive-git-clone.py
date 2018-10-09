import sys, getopt
import time, datetime
import os
from git import Repo # pip install gitpython

# Reads and checks input parameters.
def read_input(argv):
   usage = "massive-git-clone.py -i|--input <input_file> [-d|--destination <destination_folder>] [-u|--username <git_username>] [-p|--password <git_password>]"
   input_file = None
   destination = '.'
   username = None
   password = None
   
   try:
      opts, args = getopt.getopt(argv,"hi:d:u:p:",["input=","destination=","username=","password="])
   except getopt.GetoptError:
      print usage
      sys.exit(2)
	  
   for opt, arg in opts:
      if opt in ("-h", "--help"):
         print usage
         sys.exit()
      elif opt in ("-i", "--input"):
         input_file = arg
      elif opt in ("-d", "--destination"):
         destination = arg
      elif opt in ("-u", "--username"):
         username = arg
      elif opt in ("-p", "--password"):
         password = arg

   if input_file is None or len(input_file.strip()) < 1:
      print "[!] The input file can not be empty!"
      sys.exit(2)

   input_file = input_file.strip()
   destination = destination.strip()
   print "[*] Input file is: {}".format(input_file)
   print "[*] Destination folder is: {}".format(destination)
   
   if not os.path.isfile(input_file):
      print "[!] Input file provided is not a file!"
      sys.exit(2)
   if not os.path.isdir(destination):
      print "[!] Destination provided is not a folder!"
      sys.exit(2)

   if not destination.endswith("/"):
      destination = destination + "/"

   if (username is None or len(username.strip()) < 1) and (password is not None and len(password.strip()) > 0):
      print "[!] Username must be present!"
      sys.exit(2)
   if (password is None or len(password.strip()) < 1) and (username is not None and len(username.strip()) > 0):
      print "[!] Password must be present!"
      sys.exit(2)

   if username is not None:
      username = username.strip()
   if password is not None:
      password = password.strip()

   return input_file, destination, username, password

# Parses file to read repositories that will be cloned.
def parse_file(input_file):
   print "[*] Reading file '{}'.".format(input_file)
   with open(input_file) as f:
      repositories = f.readlines()
   repositories = [r.strip() for r in repositories]
   print "[*] There are '{}' repositories in the file.".format(len(repositories))
   return repositories

# Git clone all the repositories.
def git_clone(repositories, destination, username, password):
   num = 0
   for r in repositories:
      num = num + 1
      if r.startswith("#"):
         print "[-] ({}) Ignoring repository '{}' because excluded.".format(num, r)
      else:
         f = destination + (r.split("/")[-1]).split(".")[0]
         if os.path.exists(f):
		    print "[-] ({}) Ignoring repository '{}' because folder '{}' exists.".format(num, r, f)
         else:
            print "[*] ({}) Cloning repository '{}' into folder '{}'.".format(num, r, f)
            if username is not None and password is not None:
               r_splitted = r.split("://")
               r = r_splitted[0] + "://" + username + ":" + password + "@" + r_splitted[1]
            Repo.clone_from(r, f)

# Main execution.
if __name__ == "__main__":
   print "Massive Git Clone - v1.0 (2018-10-09)"
   input_file, destination, username, password = read_input(sys.argv[1:])
   repositories = parse_file(input_file)
   git_clone(repositories, destination, username, password)
   print "Finished at '{}'.".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))