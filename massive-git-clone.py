#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from dulwich import porcelain
from getpass import getpass

VERSION = "2.0 (2025-02-26)"
DEFAULT_LOGGING_LEVEL = logging.INFO

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=f"This is a Python script that can be used to clone several Git repositories defined, via URL, into a text file. - {VERSION}"
    )
    parser.add_argument("-i", "--input",
                        required=True,
                        help="Input file with the Git repositories URLs.")
    parser.add_argument("-o", "--output",
                        required=True,
                        help="Output folder where the repositories will be cloned.")
    parser.add_argument("-a", "--auth",
                        required=False,
                        help="Will ask for username and password to clone private repositories.")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        required=False,
                        default=False,
                        help="Verbose mode")
    return parser.parse_args()

def validate_input(args):
      logging.debug("Validating input.")
      if not os.path.isfile(args.input):
         logging.fatal(f"Input file '{args.input}' does not exist.")
         sys.exit(1)
      if not os.path.isdir(args.output):
         logging.fatal(f"Output folder '{args.output}' does not exist.")
         sys.exit(1)

def read_repositories(input_file):
   logging.info(f"Reading repositories from file '{input_file}'.")
   with open(input_file) as f:
      repositories = f.readlines()
   repositories = [r.strip() for r in repositories]
   return repositories

def git_clone(repositories, output_folder, username, password):
   logging.info(f"Cloning repositories into folder '{output_folder}'.")
   for repository in repositories:
      if repository.startswith("#"):
         logging.debug("Ignoring commented line.")
      else:
         logging.info(f"Cloning repository '{repository}'.")
         repository_name = repository.split("/")[-1].replace(".git", "")
         repository_folder = os.path.join(output_folder, repository_name)
         if username is not None and password is not None:
            porcelain.clone(source=repository, target=repository_folder, depth=1, username=username, password=password)
         else:
            porcelain.clone(source=repository, target=repository_folder, depth=1)

def main():
   args = parse_arguments()
   logging_level = DEFAULT_LOGGING_LEVEL
   if args.verbose:
      logging_level = logging.DEBUG
   logging.basicConfig(level=logging_level, format="%(asctime)s - %(levelname)s - %(message)s")

   try:

      validate_input(args)
      input_file = args.input
      output_folder = args.output

      username = None
      password = None
      if args.auth:
         username = input("Username: ")
         password = getpass("Password: ")
      
      repositories = read_repositories(input_file)

      git_clone(repositories, output_folder, username, password)
   
   except KeyboardInterrupt:
      logging.error("Process interrupted by user.")
      sys.exit(1)
   except Exception as e:
      logging.fatal(f"An error occurred: {e}")
      sys.exit(1)

if __name__ == "__main__":
   main()
