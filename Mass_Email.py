#code

import pandas as pd
import win32com.client as win32
outlook = win32.Dispatch('outlook.application')

file_path = r'C://Users/bubbl/Documents/test/file.xlsx' 
df1 = pd.read_excel(file_path, sheet_name = 'sheet1')
df2 = pd.read_excel(file_path, sheet_name = 'sheet2') 

df11 = df1['id'].unique()
list_carrier = list(df11)
name = list(df1['name'])
print(df11)
print(name)

path = r'C://Users/bubbl/Documents/test/'
import os
import codecs

signature_path = os.path.join((os.environ['USERPROFILE']),'AppData\Roaming\Microsoft\Signatures\Official\\')
html_doc = os.path.join((os.environ['USERPROFILE']),'AppData\Roaming\Microsoft\Signatures\Official.htm') 
html_doc = html_doc.replace('\\\\', '\\') #Removes escape backslashes from path string

html_file = codecs.open(html_doc, 'r', 'utf-8', errors='ignore') #Opens HTML file and ignores errors
signature_code = html_file.read()               #Writes contents of HTML signature file to a string
signature_code = signature_code.replace('Official/', signature_path)      #Replaces local directory with full directory path
html_file.close()


for i, name in zip(df11,name):
    mail = outlook.CreateItem(0)
    email = df2.loc[df2['id'] == i, 'email'].item()
    #mail.cc = 'xxx@test.com '
    mail.To = email
    mail.Subject = "test"

    mail.HTMLBody = f"""
        <html>
          <head></head>
          <body>
            Dear {name},
                <p> 
                Thank you. 
                </p>
            <p>Best Regards,</p>
          </body>
        </html>
        """ + signature_code
        
    i=str(i)
    while len(str(i))<3:
        i = '0' + i
    path_1=path+"file"+i+".pdf"
    
    mail.Attachments.Add(path_1)
    mail.Send()
