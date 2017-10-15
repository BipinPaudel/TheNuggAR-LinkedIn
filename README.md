# TheNuggAR-LinkedIn
Repository for solution to the test question.

# How to run the script.
python main.py linkedinemail@domain.com 'linkedinpassword'

## It is necessary to keep quotes in case of password in order to generalize the usage of script since passwords may contain $ and unix doesnot take it as a string when without quotes.

# The script scrapes email(when possible), name, linkedin profile url and job title based on certain search criteria.

LinkedIn makes email's visible to only 1st degree connection. Even here, the user can choose to hide email. Therefore, only for the case of 1st degree connections, email is scraped if present. 

### All the scraped content is updated on a live google spreadsheet. It is required to enable sheets api on google developer console and get the secret credentials to be able to run the script. 
