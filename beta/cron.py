import dbi
import pymysql
from datetime import datetime

# Import smtplib for the actual sending function
import smtplib
 
# Import the email modules we'll need
from email.mime.text import MIMEText

import getters

def overdue_email(body,
                  to,
                  from_addr='cs304reclib@wellesley.edu',
                  subject='Overdue Item(s) from WZLY Record Library'):
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

def send_emails():
    conn = getters.getConn('cs304reclib_db')
    results = getters.getOverdueEmails(conn)

    for result in results:
        email_address = result['username'] + '@wellesley.edu'

        bid = getters.getBIDFromUsername(conn, result['username'])
        materials_overdue = getters.getOverdueReservationsByID(bid['bid'], conn)

        message = []
        
        message.append("Hello,\n\n" +
                       "You have the following material(s) checked out from the Records Library that are now overdue:\n\n")

        for material in materials_overdue:
            message.append(material['album_name'] + ", which was due on " +
                           material['due'].strftime("%m/%d/%Y") + ".\n")
        
        message.append("Please return your materials to the Records Library.\n\n" +
                       "THIS EMAIL IS NOT MONITORED. To contact the Records Library, " +
                       "email us at ")

        email_message = ''.join(message)

        print(email_message)

        overdue_email(email_message,
                      # 'ngates@wellesley.edu')
                      email_address)
 
if __name__ == '__main__':
    send_emails()