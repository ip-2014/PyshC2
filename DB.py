#!/usr/bin/python

import datetime, time
import sqlite3
from sqlite3 import Error
from C2Server import DB
from ImplantHandler import DB

def initializedb():
  create_implants = """CREATE TABLE IF NOT EXISTS Implants (
        ImplantID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        RandomURI VARCHAR(20),
        User TEXT,
        Hostname TEXT,
        IpAddress TEXT,
        Key TEXT,
        FirstSeen TEXT,
        LastSeen TEXT,
        PID TEXT,
        Proxy TEXT,
        Arch TEXT,
        Domain TEXT,
        Alive TEXT,
        Sleep TEXT,
        ModsLoaded TEXT,
        Pivot TEXT);"""

  create_autoruns = """CREATE TABLE AutoRuns (
        TaskID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        Task TEXT);"""

  create_completedtasks = """CREATE TABLE CompletedTasks (
        CompletedTaskID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        TaskID TEXT,
        RandomURI TEXT,
        Command TEXT,
        Output TEXT,
        Prompt TEXT);"""

  create_tasks = """CREATE TABLE NewTasks (
        TaskID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        RandomURI TEXT,
        Command TEXT);"""

  create_creds = """CREATE TABLE Creds (
        credsID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        Username TEXT,
        Password TEXT,
        Hash TEXT);"""

  create_c2server = """CREATE TABLE C2Server (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        HostnameIP TEXT,
        EncKey TEXT,
        DomainFrontHeader TEXT,
        DefaultSleep TEXT,
        KillDate TEXT,
        HTTPResponse TEXT,
        FolderPath TEXT,
        ServerPort TEXT,
        QuickCommand TEXT,
        DownloadURI TEXT,
        ProxyURL TEXT,
        ProxyUser TEXT,
        ProxyPass TEXT,
        Sounds TEXT,
        APIKEY TEXT,
        MobileNumber TEXT,
        URLS TEXT,
        SocksURLS TEXT,
        Insecure TEXT,
        UserAgent TEXT,
        Referer TEXT);""" 

  create_history = """CREATE TABLE History (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        Command TEXT);"""  

  conn = sqlite3.connect(DB)
  c = conn.cursor()

  if conn is not None:
    c.execute(create_implants)
    c.execute(create_autoruns)
    c.execute(create_completedtasks)
    c.execute(create_tasks)
    c.execute(create_creds)
    c.execute(create_c2server)
    c.execute(create_history)
    conn.commit()
  else:
    print("Error! cannot create the database connection.")

def setupserver(HostnameIP,EncKey,DomainFrontHeader,DefaultSleep,KillDate,HTTPResponse,FolderPath,ServerPort,QuickCommand,DownloadURI,ProxyURL,ProxyUser,ProxyPass,Sounds,APIKEY,MobileNumber,URLS,SocksURLS,Insecure,UserAgent,Referer):
  conn = sqlite3.connect(DB)
  conn.text_factory = str
  c = conn.cursor()
  c.execute("INSERT INTO C2Server (HostnameIP,EncKey,DomainFrontHeader,DefaultSleep,KillDate,HTTPResponse,FolderPath,ServerPort,QuickCommand,DownloadURI,ProxyURL,ProxyUser,ProxyPass,Sounds,APIKEY,MobileNumber,URLS,SocksURLS,Insecure,UserAgent,Referer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(HostnameIP,EncKey,DomainFrontHeader,DefaultSleep,KillDate,HTTPResponse,FolderPath,ServerPort,QuickCommand,DownloadURI,ProxyURL,ProxyUser,ProxyPass,Sounds,APIKEY,MobileNumber,URLS,SocksURLS,Insecure,UserAgent,Referer))
  conn.commit()

def get_c2server_all():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM C2Server")
  result = c.fetchone()
  if result:
    return result
  else:
    return None

def get_implants_all():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM Implants")
  result = c.fetchall()
  if result:
    return result
  else:
    return None

def get_nettasks_all():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM NewTasks")
  result = c.fetchall()
  if result:
    return result
  else:
    return None

def drop_nettasks():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("DELETE FROM NewTasks ")
  conn.commit()

def new_task( task, randomuri ):
  conn = sqlite3.connect(DB)
  conn.text_factory = str
  c = conn.cursor()
  c.execute("INSERT INTO NewTasks (RandomURI, Command) VALUES (?, ?)",(randomuri, task))
  conn.commit()

def get_lastcommand():
  conn = sqlite3.connect(DB)
  conn.text_factory = str
  c = conn.cursor()
  c.execute("SELECT * FROM History ORDER BY ID DESC LIMIT 1")
  try:
    result = c.fetchone()[1]
  except Exception as e:
    result = None
  if result:
    return result
  else:
    return None

def new_commandhistory( command ):
  conn = sqlite3.connect(DB)
  conn.text_factory = str
  c = conn.cursor()
  c.execute("INSERT INTO History (Command) VALUES (?)",(command,))
  conn.commit()

def get_history_dict():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM History")
  result = c.fetchall()
  if result:
    return result
  else:
    return None 

def get_history():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM History")
  result = c.fetchall()
  history = ""
  for command in result:
  	history = "%s \r\n %s" % (history, command[1])
  history = "%s \r\n" % (history)
  if history:
    return history
  else:
    return None 

def get_implants():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM Implants WHERE Alive='Yes'")
  result = c.fetchall()
  if result:
    return result
  else:
    return None 

def get_implanttype( randomuri ):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT Pivot FROM Implants WHERE RandomURI=?",(randomuri,))
  result = str(c.fetchone()[0])
  if result:
    return result
  else:
    return None

def get_implantdetails( randomuri ):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM Implants WHERE RandomURI=?",(randomuri,))
  result = c.fetchone()
  if result:
    return result
  else:
    return None

def get_randomuri( implant_id ):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT RandomURI FROM Implants WHERE ImplantID=?",(implant_id,))
  result = str(c.fetchone()[0])
  if result:
    return result
  else:
    return None 

def add_autorun(Task):
  conn = sqlite3.connect(DB)
  conn.text_factory = str
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("INSERT INTO AutoRuns (Task) VALUES (?)", (Task,))
  conn.commit()

def update_sleep( sleep, randomuri ):
  conn = sqlite3.connect(DB)
  c = conn.cursor()
  c.execute("UPDATE Implants SET Sleep=? WHERE RandomURI=?",(sleep, randomuri))
  conn.commit()

def update_mods( modules, randomuri ):
  conn = sqlite3.connect(DB)
  c = conn.cursor()
  c.execute("UPDATE Implants SET ModsLoaded=? WHERE RandomURI=?",(modules, randomuri))
  conn.commit()

def kill_implant( randomuri ):
  conn = sqlite3.connect(DB)
  c = conn.cursor()
  c.execute("UPDATE Implants SET Alive='No' WHERE RandomURI=?",(randomuri,))
  conn.commit()

def unhide_implant( randomuri ):
  conn = sqlite3.connect(DB)
  c = conn.cursor()
  c.execute("UPDATE Implants SET Alive='Yes' WHERE RandomURI=?",(randomuri,))
  conn.commit()

def select_mods( randomuri ):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT ModsLoaded FROM Implants WHERE RandomURI=?", (randomuri,))
  result = str(c.fetchone()[0]) 
  if result:
    return result
  else:
    return None  

def select_item(column, table):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT %s FROM %s" % (column, table))
  result = str(c.fetchone()[0]) 
  if result:
    return result
  else:
    return None

def del_newtasks(TaskID):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("DELETE FROM NewTasks WHERE TaskID=?", (TaskID,))
  conn.commit()

def del_autorun(TaskID):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("DELETE FROM AutoRuns WHERE TaskID=?", (TaskID,))
  conn.commit()

def del_autoruns():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("DELETE FROM AutoRuns ")
  conn.commit()

def update_implant_lastseen(time, randomuri):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("UPDATE Implants SET LastSeen=? WHERE RandomURI=?", (time,randomuri))
  conn.commit()

def new_implant(RandomURI, User, Hostname, IpAddress, Key, FirstSeen, LastSeen, PID, Proxy, Arch, Domain, Alive, Sleep, ModsLoaded, Pivot):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("INSERT INTO Implants (RandomURI, User, Hostname, IpAddress, Key, FirstSeen, LastSeen, PID, Proxy, Arch, Domain, Alive, Sleep, ModsLoaded, Pivot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (RandomURI, User, Hostname, IpAddress, Key, FirstSeen, LastSeen, PID, Proxy, Arch, Domain, Alive, Sleep, ModsLoaded, Pivot))
  conn.commit()

def insert_completedtask(randomuri, command, output, prompt):
  now = datetime.datetime.now()
  TaskID = now.strftime("%m/%d/%Y %H:%M:%S")
  conn = sqlite3.connect(DB)
  conn.text_factory = str
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("INSERT INTO CompletedTasks (TaskID, RandomURI, Command, Output, Prompt) VALUES (?, ?, ?, ?, ?)", (TaskID, randomuri, command, output, prompt))
  conn.commit()

def update_item(column, table, value, wherecolumn=None, where=None):
  conn = sqlite3.connect(DB)
  c = conn.cursor()
  if wherecolumn is None:
    c.execute("UPDATE %s SET %s=?" % (table,column), (value,))
  else:
    c.execute("UPDATE %s SET %s=? WHERE %s=?" % (table,column,wherecolumn), (value, where))
  conn.commit()

def get_implantbyid(id):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM Implants WHERE ImplantID=%s" % id)
  result = c.fetchone()
  if result:
    return result
  else:
    return None

def get_completedtasksbyid(id):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM CompletedTasks WHERE CompletedTaskID=%s" % id)
  result = c.fetchone()
  if result:
    return result
  else:
    return None

def get_newtasksbyid(taskid):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM NewTasks WHERE TaskID=%s" % taskid)
  result = c.fetchone()
  if result:
    return result
  else:
    return None

def get_seqcount(table):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT seq FROM sqlite_sequence WHERE name=\"%s\"" % table)
  result = int(c.fetchone()[0])
  if result:
    return result
  else:
    return None

def get_baseenckey():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT EncKey FROM C2Server")
  result = str(c.fetchone()[0])
  if result:
    return result
  else:
    return None

def get_defaultuseragent():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT UserAgent FROM C2Server")
  result = str(c.fetchone()[0])
  if result:
    return result
  else:
    return None

def get_defaultbeacon():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT DefaultSleep FROM C2Server")
  result = str(c.fetchone()[0])
  if result:
    return result
  else:
    return None

def get_killdate():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT KillDate FROM C2Server")
  result = str(c.fetchone()[0])
  if result:
    return result
  else:
    return None

def get_sharpurls():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT SocksURLS FROM C2Server")
  result = str(c.fetchone()[0]) 
  if result:
    return result
  else:
    return None

def get_allurls():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT URLS FROM C2Server")
  result1 = str(c.fetchone()[0]) 
  c.execute("SELECT SocksURLS FROM C2Server")
  result2 = str(c.fetchone()[0]) 
  result = result1+","+result2
  if result:
    return result
  else:
    return None

def get_beaconurl():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT URLS FROM C2Server")
  result = str(c.fetchone()[0]) 
  if result:
    url = result.split(",")
    return url[0]
  else:
    return None

def get_otherbeaconurls():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT URLS FROM C2Server")
  result = str(c.fetchone()[0]) 
  if result:
    return result
  else:
    return None

def get_newimplanturl():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT URLS FROM C2Server")
  result = str(c.fetchone()[0]) 
  if result:
    url = result.split(",")
    return "/"+url[0].replace('"', '')
  else:
    return None

def get_hostinfo(randomuri):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM Implants WHERE RandomURI=?", (randomuri,))
  result = c.fetchall()
  if result:
    return result[0]
  else:
    return None 

def get_autoruns():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM AutoRuns")
  result = c.fetchall()
  if result:
    return result
  else:
    return None 

def get_autorun():
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM AutoRuns")
  result = c.fetchall()
  autoruns = ""
  for autorun in result:
    autoruns += "%s:%s\r\n" % (autorun[0],autorun[1])
  if autoruns:
    return autoruns
  else:
    return None 

def get_pid(randomuri):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT PID FROM Implants WHERE RandomURI=?", (randomuri,))
  result = c.fetchone()[0]
  if result:
    return result
  else:
    return None

def get_newtasks(randomuri):
  conn = sqlite3.connect(DB)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * FROM NewTasks WHERE RandomURI=?", (randomuri,))
  result = c.fetchall()
  if result:
    return result
  else:
    return None