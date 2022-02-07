# !/usr/bin/env python3
#coding=UTF-8

#importing necessary packages
import paramiko
import os.path
import stat
from collections import defaultdict
import pandas as pd

#password for sftp portal
host = "upload.fakehostname.com"
port = fakeport
username = "insertusername"
password = "sftpfakepassword"

#using paramiko library to connect to sftp
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

ftp = ssh.open_sftp()
#directing it on where to point within sftp
ftp.chdir('/d/Uploads')

files = ftp.listdir()

def recursive_ftp(ftp, path='/d/Uploads', files=None):
    if files is None:
        files = defaultdict(list)

    # loop over list of SFTPAttributes (files with modes)
    for attr in ftp.listdir_attr(path):

        if stat.S_ISDIR(attr.st_mode):
            # If the file is a directory, recurse it
            recursive_ftp(ftp, os.path.join(path,attr.filename), files)

        else:
            #  if the file is a file, add it to our dict
            files[path].append(attr.filename)

    return files

files = recursive_ftp(ftp)

files = dict(files)

#grabbing the dictionary of file names and add it to a dataframe using Pandas
df = pd.DataFrame(list(files.items()),columns = ['key','value']) 

#all the code below is taking the dataframe and doing some filtering, such as removing files from before 2021
#im sure there are more efficient ways to do this such as looping over the files or something but this seems to work okay for now
fake_df = df.value.apply(pd.Series) \
    .merge(df, right_index = True, left_index = True) \
    .drop(["value"], axis = 1) \
    .melt(id_vars = ['key'], value_name = "file")

fake_df = fake_df.dropna()

del fake_df['variable']

fake_df = fake_df.sort_values(by=['key'])

fake_df = fake_df[fake_df.key != '/d/Uploads\idi\.filerun.trash']

fake_df = fake_df[~(fake_df['file'].str.contains("2016"))]

fake_df = fake_df[~(fake_df['file'].str.contains("2017"))]

fake_df = fake_df[~(fake_df['file'].str.contains("2018"))]

fake_df = fake_df[~(fake_df['file'].str.contains("2019"))]

fake_df = fake_df[~(fake_df['file'].str.contains("2020"))]

df = fake_df.rename(columns={"key": "folder"})

#sending the list as a csv to a local folder on my laptop
df.to_csv(r'C:\Users\rober\lists.csv', index=False)

#importing package to email file
import yagmail

try:
    #initializing the server connection
    yag = yagmail.SMTP(user='fakeemailbotname@gmail.com', password='passwordplaceholder')
    #sending the email
    yag.send(to='insertwhereyouwanttosend@gmail.com', subject='Current Lists in /Uploads Dir', contents='See attached', attachments='lists.csv')
    print("Email sent successfully")
except:
    print("Error, email was not sent")

ssh.close()