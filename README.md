# spidy
Spidy is python script for based on zmap scan execution

# Commands
<pre>
./spidy.py db_init  -- Creates database table to store the data and words.txt file with short user:pass list for bruteforcing

./spidy.py ip_list ru
./spidy.py ip_list by  -- Starts downloading list of IP pools by domains zone (by country)

./spidy.py scan 21  -- Executes scanning of IP pool for 21 open port and storing results into database
./spidy.py scan 27017  -- Executes scanning of IP pool for mongodb port and storing results into database
Any port can be used for scanning

./spidy.py check ftp   -- Executes FTP Anonymous access check for hosts with open 21 port from database, if connection was successful and banner accepted, in database column "banner" will be success, otherwise it will be "fail"
Available checks: ftp, ssh, mongo, heartbleed

./spidy.py export 21 ftp.txt   -- Exports all results from database where port is "21" into ftp.txt file within the same directory with spidy
Can be used to export results for any port from database with output in any type of file
</pre>
