from email_validator import validate_email, EmailNotValidError
import pathlib
from bs4 import BeautifulSoup
import logging
import shutil
import streamlit as st
import re


def inject_ga():
   GA_ID = "google_analytics"

   GA_JS = """
   <!-- Global site tag (gtag.js) - Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-SRSJCKCBE9"></script>
   <script>
       window.dataLayer = window.dataLayer || [];
       function gtag(){dataLayer.push(arguments);}
       gtag('js', new Date());

       gtag('config', 'G-**********');
   </script>
   """
   # Insert the script in the head tag of the static template inside your virtual
   index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
   logging.info(f'editing {index_path}')
   soup = BeautifulSoup(index_path.read_text(), features="html.parser")
   if not soup.find(id=GA_ID):
      bck_index = index_path.with_suffix('.bck')
      if bck_index.exists():
         shutil.copy(bck_index, index_path)
      else:
         shutil.copy(index_path, bck_index)
      html = str(soup)
      new_html = html.replace('<head>', '<head>\n' + GA_JS)
      index_path.write_text(new_html)

# ------- CHECK IF VALID PDF URL ---------
@st.cache
def is_valid_pdf_url(url):
   regex = r'^(?:http|ftp)s?://.*\.pdf$'  # must start with http:// or https:// and end with .pdf
   return re.match(regex, url) is not None

# ------- CHECK IF VALID URL ---------
@st.cache
def is_valid_url(url):
   regex = r'^(?:http|ftp)s?://'  # http:// or https://
   return re.match(regex, url) is not None

# ------- CONVERT LIST TO STRING ---------
@st.cache
def list_to_string(lst):
   return ', '.join(str(elem) for elem in lst)


# ------- FUNCTION TO CHECK IF EMAIL IS VALID ---------
@st.cache
def is_valid_email(email):
   try:
      # validate and get info
      v = validate_email(email)
      # replace with normalized form
      email = v["email"]
      return True
   except EmailNotValidError as e:
      # email is not valid, exception message is human-readable
      # print(str(e))
      return False


# ------- FUNC ADJUST KEY_TERMS AND QUESTIONS ---------
@st.cache
def customize_string_list(default_list, *user_lists, add_to_default=False):
   # Combine all user-provided lists into a single list
   combined_list = []
   for user_list in user_lists:
      combined_list.extend(user_list)
   # If the user wants to add their list(s) to the default list
   if add_to_default:
      # Extend the default list with the combined user list
      default_list.extend(combined_list)
   # If the user has provided a list to replace the default list
   elif combined_list:
      # Replace the default list with the combined user list
      default_list = combined_list
   # Return the modified list
   return default_list


# ------- FUNC MAKE WORD POSSESSIVE ---------
@st.cache
def make_possessive(noun):
   # If the noun ends in "s"
   if noun[-1] == 's':
      # Add an apostrophe after the "s"
      return f"{noun}'"
   # If the noun does not end in "s"
   else:
      # Add an apostrophe and an "s"
      return f"{noun}'s"


# ------- FUNC CHECKS + ADDS COMMAS ---------
@st.cache
def add_commas(input_string):
   # Split the string into a list of words
   words = input_string.split()
   # Check if there is already a comma after every word
   if all(word[-1] == ',' for word in words):
      # If there is, return the input string as is
      return input_string
   # If not, add a comma after every word
   else:
      # Join the words with commas
      output_string = ', '.join(words)
      return output_string