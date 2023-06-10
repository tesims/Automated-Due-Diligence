from pitch_deck import *
from input_fns import *
from website import *
from streamlit_extras.badges import badge
from pyairtable import Table
from fpdf import FPDF
import datetime
import time
import io



inject_ga()
st.set_page_config(
   page_title="Soothsayer Technology - VettedView",
   page_icon="http://soothsayer.technology/wp-content/uploads/2022/11/soothtech-logo-favicon-purp-01.png",
   layout="centered",
   initial_sidebar_state="expanded")

hide_streamlit_style = """
         <style>
         #MainMenu {visibility: hidden;}
         footer {visibility: hidden;}
         </style>
         """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# ------- SET DEFAULT VARIABLES ---------
default_key_terms = ["Customers", "Product ", "Demo", "Team", "Pricing"]

default_questions = ['What problem does your company solve?',
                     'How is your solution unique and innovative?',
                     'Who is your target customer and market size?']


# ------- SET HOME SCREEN ---------
st.title("Welcome to VettedView")

tcol1, tcol2 = st.columns(2)
with tcol1:
   st.video('https://www.youtube.com/watch?v=Xyj-BkuQICY&t=10s')
with tcol2:
   st.text("by Soothsayer Technology, Inc")
   st.caption("VettedView is a suite of AI-powered tools that aggregates all the key data and documents needed for "
              "due diligence, providing a clear and concise summary of any company. Simply fill in the fields below "
              "to generate a report on a specific company.")
   badge(type='twitter', name='soothsayertech')


tab1, tab2, tab3, tab4 = st.tabs(['Pitch Deck Overview', 'Website Scan', 'Team Evaluator', 'Market Comparator'])

with tab1:
   st.caption("Our pitch deck tool helps investors quickly and easily gather important information about a company. With "
           "just a few clicks, you can generate a summary report that includes key details such as the problem being "
           "solved, target audience, competition, business model, funding requirements, and more. Customization options "
           "allow you to tailor the report to your specific needs. With our tool, you can easily get a clear overview of"
           " a company's pitch deck in a simple, easy-to-read report.")
   st.text('')

with tab2:
   st.caption("Generate a comprehensive report on a company's website with our software. Discover what products and "
              "services are being offered, find out if demos are available, learn about the team, and more. You can "
              "customize the information included in the report to fit your needs. Save time by using our tool "
              "instead of manually searching a company's website, and quickly get a summary of all the important "
              "information.")


with tab3:
   st.caption("Our tool helps investors assess a company's team and their ability to execute the business plan, while "
              "also eliminating risk. By analyzing each team member's digital footprint, we are able to detect any bad "
              "behavior online that could potentially harm the company and its investors' reputations. With this information, "
              "investors can make informed decisions about the company's potential for success without worrying about "
              "reputational risk. Our tool is an essential resource that provides all the important information "
              "investors need in an easy-to-read report, helping them invest with confidence.")
   st.caption("***Development in Progress***")
   st.text('')

with tab4:
   st.caption("Gain a competitive edge by receive a detailed analysis of the company’s market. Our tool automatically "
              "gathers data from a variety of sources, including industry reports, company websites, and social media. "
              "It then uses advanced deep learning algorithms to analyze this data and generate a comprehensive report "
              "on the competitive landscape for the startup in question. The report includes information on key "
              "competitors, market trends, target customers, and potential challenges and opportunities. It is an "
              "essential resource for investors looking to make informed decisions about the potential of a startup.")
   st.caption("***Development in Progress***")
   st.text('')


with st.sidebar.form(key="my_form"):

   # ------- GET USER PERSONAL INFORMATION ---------
   first_name_placeholder = st.empty()
   first_name = first_name_placeholder.text_input('First Name*', placeholder='John')

   last_name_placeholder = st.empty()
   last_name = last_name_placeholder.text_input('Last Name*', placeholder='Doe')

   email_placeholder = st.empty()
   email = email_placeholder.text_input('Email*', placeholder='user@email.com')

   phone_number_placeholder = st.empty()
   phone_number = phone_number_placeholder.text_input('Phone Number', placeholder='xxx-xxx-xxxx')

   st.caption("*Required fields")

   # ------- GET COMPANY VARIABLE INPUTS (FORM) ---------
   st.header("Company Information")
   company_name = st.text_input('Name of Company', placeholder='Example, Inc.')

   check_website = st.checkbox('Scan Company Website')
   check_pitch_deck = st.checkbox('Pitch Deck Summary')

   st.subheader("Website")
   company_url_placeholder = st.empty()
   company_url = company_url_placeholder.text_input('Website URL', placeholder='https://example.com')

   add_key_terms_placeholder = st.empty()
   add_key_terms = add_key_terms_placeholder.multiselect('What do you want to know?',
                                                         ["Value", "Competition", "Growth",
                                                          "Contact", "Strategy", "Revenue"])

   new_key_terms_placeholder = st.empty()
   new_key_terms = new_key_terms_placeholder.text_area('Add Additional Key Terms. '
                                                       'Only list single words separated by a comma.',
                                                       placeholder='If left blank default questions will be used.')
   temp_key_terms = add_commas(new_key_terms)
   custom_key_terms = temp_key_terms.split(',')

   st.subheader("Pitch Deck")
   url_pitch_deck_placeholder = st.empty()
   url_pitch_deck = url_pitch_deck_placeholder.text_input('URL Link to PDF', placeholder='https://example.pdf')

   file_pitch_deck_placeholder = st.empty()
   file_pitch_deck = file_pitch_deck_placeholder.file_uploader('Upload PDF File', type="pdf")

   add_questions = st.multiselect('What do you want to know?',
                                  ['How will you acquire customers?',
                                   'What is the current state and roadmap of your product?',
                                   'Who is on your team and what are their qualifications?',
                                   'How much funding are you seeking and for what purpose?',
                                   'What traction or milestones have you achieved?',
                                   'How will you monetize your solution?',
                                   'How will you measure and achieve success?'])

   new_questions = st.text_area('Add Additional Questions. Separate questions with a comma.',
                                                       placeholder='If left blank default questions will be used.' )
   temp_questions = add_commas(new_questions)
   custom_questions = temp_questions.split(',')

   # ------- SUBMIT FORM BUTTON ---------
   submitted = st.form_submit_button(label='Generate Report 🔎',
                                     help='Generate a PDF of your report. ')

if submitted:
   with st.spinner(f'Hi {first_name}, we are generating your report. Hold tight it could take a minute.'):

      # ------ CHECK REQUIRED FIELDS ------
      if first_name and last_name and email:
         # ------ CHECK IF EMAIL IS VALID ------
         if is_valid_email(email):

            if company_name:
               company_name_possessive = make_possessive(company_name)
            else:
               company_name_possessive = ''

            # SET CHECK + SET KEY_TERMS LIST
            if add_key_terms or new_key_terms:
               add_to_default_key_terms = True

               if add_key_terms and not new_key_terms:
                  user_list_key_terms = add_key_terms

               elif not add_key_terms and new_key_terms:
                  user_list_key_terms = custom_key_terms

               else:
                  user_list1 = add_key_terms
                  user_list2 = custom_key_terms
                  user_list1.extend(user_list2)
                  user_list_key_terms = user_list1
            else:
               add_to_default_key_terms = False
               user_list_key_terms = []

            key_terms = customize_string_list(default_key_terms, user_list_key_terms,
                                              add_to_default=add_to_default_key_terms)
            # SET CHECK + SET QUESTIONS LIST
            if add_questions or new_questions:
               add_to_default_questions = True

               if add_questions and not new_questions:
                  user_list_questions = add_questions

               elif not add_questions and new_questions:
                  user_list_questions = custom_questions

               else:
                  user_list3 = add_questions
                  user_list4 = custom_questions
                  user_list3.extend(user_list4)
                  user_list_questions = user_list3
            else:
               add_to_default_questions = False
               user_list_questions = []

            questions = customize_string_list(default_questions, user_list_questions,
                                              add_to_default=add_to_default_questions)


            # ------ CHECK SELECTED FEATURES -----url
            if check_website or check_pitch_deck:
               # ------ CHECK COMPANY WEBSITE FIELD ------
               if not company_url:
                  if check_website:
                     web_summary ="We have detected that you have not provided input for the Company Website field. " \
                                  "Please provide a valid URL, and then regenerate the report."
                     st.warning(web_summary)
                     st.stop()
                  else:
                     web_summary = f"Analysis of {company_name_possessive} website not requested."
                     st.caption(web_summary)

               elif not is_valid_url(company_url):
                  web_summary = "We have detected that you have not provided a valid URL for the Company Website field. " \
                                "Please provide a valid URL, and then regenerate the report."
                  st.warning(web_summary)
                  st.stop()

               else:
                  web_summary = get_final_web_report(company_url, key_terms)
                  st.write(f"**{company_name_possessive} Website:**  ", web_summary)

               # ------ CHECK PITCH DECK FIELD ------
               if check_pitch_deck:
                  if not url_pitch_deck:
                     if not file_pitch_deck:
                        input_type = 'empty'
                        deck_summary = "We have detected that you have not provided input for the URL Link to PDF " \
                                       "and Upload PDF File fields. Please provide either a URL to the PDF or upload " \
                                       "the file directly, and then regenerate the report."
                        st.warning("deck_summary")
                        st.stop()

                     else:
                        input_type = 'doc'

                        #file = io.BytesIO(file_pitch_deck.read())
                        # Open the PDF file using the PyPDF2 library
                        #pdf_reader = PyPDF2.PdfReader(file)
                        # Create a new PDF file to write the optimized version
                        #pdf_writer = PyPDF2.PdfWriter()

                        # Iterate over all pages in the PDF file
                        #for page in range(len(pdf_reader.pages)):
                           # Get the current page
                        #   current_page = pdf_reader.pages[page]
                           # Optimize the current page
                        #   current_page.compress_content_streams()
                           # Add the optimized page to the new PDF file
                        #   pdf_writer.add_page(current_page)

                        # Save the optimized PDF file
                        #with open("optimized.pdf", "wb") as f:
                        #   pdf_writer.write(f)
                        bytes_data = file_pitch_deck.getvalue()
                        deck_summary = get_pitch_deck_summary(bytes_data, input_type, questions)
                        st.write(f"**{company_name} Pitch Deck:**  ", deck_summary)

                        # Open the optimized PDF file
                        #with open("optimized.pdf", "rb") as f:
                        #   st.write('f"**{company_name} Pitch Deck:**  "', deck_summary)

                  if url_pitch_deck:
                     if file_pitch_deck:
                        input_type = 'double'
                        deck_summary = "We have detected that you have provided input for both the URL Link to PDF and" \
                                       " Upload PDF File fields. Please provide input for only one of these fields and " \
                                       "then regenerate the report."
                        st.warning(deck_summary)
                        st.stop()

                     elif not is_valid_pdf_url(url_pitch_deck):
                        deck_summary = "We have detected that you have provided an invalid PDF URL to the URL Link to PDF" \
                                       " input Upload a valid PDF URL input or upload PDF file. Please provide input for " \
                                       "only one of these fields and then regenerate the report."
                        st.warning(deck_summary)
                        st.stop()


                     else:
                        pitch_deck = url_pitch_deck
                        input_type = 'url'
                        deck_summary = get_pitch_deck_summary(pitch_deck, input_type, questions)

                        st.write(f"**{company_name_possessive} Pitch Deck:**  ", deck_summary)


                  # ---------- CREATE OUTPUT PDF ----------
                  logo_url = 'http://soothsayer.technology/wp-content/uploads/2022/12/sooth-logo-half.png'
                  st_web_url = 'https://soothsayer.technology/'
                  filename = f"{company_name}_investor_report"


                  # Update the Airtable with our data (timestamp and output value)
                  timestamp = datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')


                  @st.cache
                  def generate_pdf(web_summary, deck_summary, name_company):
                     pdf = FPDF()
                     pdf.add_page()
                     pdf.image('http://soothsayer.technology/wp-content/uploads/2022/12/sooth-logo-half.png', 10, 8, 33,
                               link='https://soothsayer.technology/')

                     pdf.set_font('Times', 'B', 18)
                     pdf.cell(60, 10, " ", 0, 1, 'C')
                     pdf.cell(60, 13, "Due Diligence Report", 0, 1, 'C')


                     pdf.set_font('Times', 'I', 14)
                     pdf.cell(60, 1, " ", 0, 1, 'L')
                     pdf.cell(20, 10, f'Company: {company_name}', 0, 1, 'L')
                     pdf.cell(20, 10, f'Report Date: {timestamp}', 0, 1, 'L')
                     pdf.cell(60, 1, " ", 0, 1, 'L')

                     pdf.set_font('Times', 'B', 16)
                     pdf.cell(20, 10, 'Website Assessment:  ', 0, 1, 'L')
                     pdf.set_font('Times', '', 12)
                     pdf.multi_cell(0, 5, txt=web_summary)
                     pdf.set_font('Times', 'B', 16)
                     pdf.cell(40, 1, " ", 0, 1, 'L')
                     pdf.cell(20, 10, 'Pitch Deck Summary: ', 0, 1, 'L')
                     pdf.set_font('Times', '', 12)
                     pdf.multi_cell(0, 5, txt=deck_summary)

                     pdf = bytes(pdf.output())

                     return pdf


                  pdf = generate_pdf(web_summary, deck_summary, company_name_possessive)


                  # Embed PDF to display it:
                  #base64_pdf = b64encode(gen_pdf()).decode("utf-8")
                  #pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
                  #st.markdown(pdf_display, unsafe_allow_html=True)

                  # Add a download button: .multi_cell(0, 5, deck_summary)
                  time.sleep(1)
                  st.download_button(
                     label="Download PDF",
                     data=pdf,
                     file_name="file_name.pdf",
                  )


                  # ------- SET AIRTABLE ACCESS CREDENTIALS ---------
                  base_id = 'appMLUAVcdSQPIv2N'
                  table_id = 'tbl1yyrDxxmWlPnDn'
                  table_name = 'VettedView1.0'
                  table_name_feed = 'VettedView_Feedback'
                  table_name_bug = "VettedView_Bug"
                  api_key = 'key9H34Nzu4DcHIpd'
                  AIRTABLE_API_TOKEN = 'patGu9uDssefsRUD8.593e500e58198b60a84fdae7b8c150b454634010fed024794693a7f5399617fb'
                  #base_table_api_url = 'https://api.airtable.com/v0/{}{}'.format(base_id, table_id)
                  table = Table(api_key, base_id, table_name)
                  table_feedback = Table(api_key, base_id, table_name_feed)
                  table_bug_report =Table(api_key, base_id, table_name_bug)

                  # ---------- STORE USER PERSONAL DATA ----------

                  if check_website:
                     data_check_website = 'True'
                  else:
                     data_check_website = 'False'

                  if check_pitch_deck:
                     data_check_pitch_deck = 'True'
                  else:
                     data_check_pitch_deck = 'False'

                  timestamp = str(datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'))
                  firstname = str(first_name)
                  lastname = str(last_name)
                  user_email = str(email)
                  user_phone_number = str(phone_number)
                  input_company_name = str(company_name)
                  input_key_terms = str(custom_key_terms)
                  input_questions = str(custom_questions)

                  # Convert list input to strings
                  data_new_questions = list_to_string(new_questions)
                  data_custom_questions = list_to_string(custom_questions)
                  data_new_key_terms = list_to_string(new_key_terms)
                  data_custom_key_terms = list_to_string(custom_key_terms)

                  # Update the Airtable with our data (timestamp and output value)
                  data = {
                     "timestamp": timestamp,
                     "firstname": firstname,
                     "lastname": lastname,
                     "email": user_email,
                     "phonenumber": user_phone_number,
                     "companyname": input_company_name,
                     "check_website": data_check_website,
                     "check_pitch_deck": data_check_pitch_deck,
                     "new_questions": data_new_questions,
                     "custom_questions": data_custom_questions,
                     "new_key_terms": data_new_key_terms,
                     "custom_key_terms": data_custom_key_terms

                  }

                  table.create(fields=data, typecast=True)
                  st.caption("***Please Note: This is a beta version of VettedView***")

                  col1, col2 = st.columns(2)
                  with col1:
                     with st.expander('Help us improve. Tell us what you think.'):
                        with st.form(key="feedback_form"):
                           data_add_email = user_email

                           add_expect = st.selectbox('Did VettedView meet your expectations?',
                                                     ['Yes, it exceeded my expectations.',
                                                      'Yes, it met my expectations!',
                                                      'No, it did not meet my expectations.'])
                           add_pay = st.select_slider('How much would you be willing to pay for a monthly VettedView '
                                                      'subscription?',
                                                      options=['$10', '$20', '$30', '$40', '$50', '$60', '$70', '$80',
                                                               '$90', '$100'])
                           st.write('', add_pay)
                           add_features = st.text_input('What additional features would you like to see added?')
                           add_help = st.text_input('Can you think of any other people or groups that might find '
                                                    'this product helpful?')
                           add_suggest = st.text_area('Additional Suggestions')

                           # ------- SUBMIT FORM BUTTON ---------
                           submitted = st.form_submit_button(label='Submit',
                                                             help='All fields are optional, but greatly appreciated.')

                           if submitted:
                              st.caption('Thank you for your feedback!')

                              data_add_expect = str(add_expect)
                              data_add_pay = str(add_pay)
                              data_add_features = str(add_features)
                              data_add_help = str(add_help)
                              data_add_suggest = str(add_suggest)

                              feedback_data = {
                                 "email": data_add_email,
                                 "add_expect": data_add_expect,
                                 "add_pay": data_add_pay,
                                 "add_features": data_add_features,
                                 "add_help": data_add_help,
                                 "add_suggest": data_add_suggest,
                              }
                              table_feedback.create(fields=feedback_data, typecast=True)
                  with col2:
                     with st.expander("Report a Bug"):
                        with st.form("help_form"):
                           st.write(
                              "We're sorry you're experiencing an issue with our platform.Please fill out the form below to report "
                              "a bug and our team will investigate and work to resolve the issue as soon as possible.")

                           bug_report = st.text_area("",
                                                     placeholder="")

                           # Every form must have a submit button.
                           submitted = st.form_submit_button("Submit")

                           if submitted:
                              st.caption('Thank you for your patience and support!')
                              new_bug_report = str(bug_report)


                              report_bug_data = {
                                 "timestamp": timestamp,
                                 "bug": new_bug_report,
                                 "email": user_email
                              }
                              table_report_bug.create(fields=report_bug_data, typecast=True)

               else:
                  st.caption(f"Analysis of {company_name_possessive} pitch deck not requested. Fix your input and "
                             f"regenerate the report.")
            else:
               st.warning("Please check at least one of the boxes to include analysis tools in your report. Fix your "
                          "input and regenerate the report.")

         else:
            st.warning("The email you entered is invalid. Please submit a valid email address.Fix your input and "
                       "regenerate the report.")
      else:
         st.warning("Please make sure to fill out all required fields before generating your report. Fix your input "
                    "and regenerate the report.")



