# Import smtplib for the actual sending function
import smtplib
 
# Import the email modules we'll need
from email.mime.text import MIMEText

import getters

def overdue_email(body,
                  to,
                  from_addr='cs304reclib@wellesley.edu',
                  subject='Overdue Item(s) from WZLY Record Library'):
    
    results = getters.getOverdueEmails
    usernames = []

    for result in results:
        username.append[result + "@wellesley.edu"]
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To']
 
# def overdue_email(body,
#           to=(username + '@wellesley.edu'),
#           from_addr='cs304reclib@wellesley.edu',
#           subject='Overdue Item(s) from WZLY Record Library'):
#     msg = MIMEText(body)
#     msg['Subject']=subject
#     msg['From']=from_addr
#     msg['To']=to
     
#     # Send the message via our own SMTP server.
#     s = smtplib.SMTP('localhost')
#     s.send_message(msg)
#     s.quit()
 
# if __name__ == '__main__':
#     import pymysql
#     import dbi
#     dsn = dbi.read_cnf('/home/cs304/.my.cnf')
#     conn = dbi.connect(dsn)
#     dbi.select_db(conn,'webdb')
#     curs = dbi.dictCursor(conn)
#     curs.execute('select addr from emails')
#     for row in curs.fetchall():
#         print(row['addr'])
#         email('Just a reminder ...',
#               to=row['addr'],
#               subject='confirmation')