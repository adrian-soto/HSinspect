
# coding: utf-8

# # Create database for OSHA inspection and violation data
# 
# Data can be downloaded from here:
# https://public.enigma.com/browse/occupational-safety-and-health-administration-osha/98fa73e5-f974-4c46-8419-8010543c3cd2
# 
# The relevant files for this project are
# - OSHA - Inspection Report
# - OSHA - Violation Event
# 
# 
# ## Note: remember to start PostgreSQL server!


## Python packages
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd

import numpy as np



# Define a database name and username for this computer
dbname = 'osha_db'
username = 'asc'

# Define connection to database
con = None
con = psycopg2.connect(database = dbname, user = username)


# ## Create a database


## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
print engine.url



## create a database (if it doesn't exist)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))



# Data dir
data_dir = '/Users/asc/Documents/Insight/test_projects/OSHA/data/'



# CREATE TABLE OF INSPECTION DATA

sql_query = '''

CREATE TABLE inspections_table(
activity_nr integer NULL,
reporting_id integer NULL,
state_flag char(2) NULL,
estab_name text NULL,
site_address text NULL,
site_city text NULL,
site_state text NULL,
site_zip integer NULL,
owner_type char(1) NULL,
owner_type_definition text NULL,
owner_code text NULL,
adv_notice char(1) NULL,
safety_hlth char(1) NULL,
safety_hlth_definition text NULL,
sic_code char(4) NULL,
naics_code char(6) NULL,
insp_type char(1) NULL,
insp_type_definition text NULL,
insp_scope char(1) NULL,
insp_scope_definition text NULL,
why_no_insp char(1) NULL,
why_no_insp_definition text NULL,
union_status char(1) NULL,
union_status_definition text NULL,
safety_manuf char(1) NULL,
safety_const char(1) NULL,
safety_marit char(1) NULL,
health_manuf char(1) NULL,
health_const char(1) NULL,
health_marit char(1) NULL,
migrant char(1) NULL,
mail_street text NULL,
mail_city text NULL,
mail_state char(2) NULL,
mail_zip char(5) NULL,
host_est_key text NULL,
nr_in_estab integer NULL,
open_date date NULL,
case_mod_date date NULL,
close_conf_date date NULL,
close_case_date date NULL,
ld_dt timestamp NULL);


COPY inspections_table FROM 
'/Users/asc/Documents/Insight/test_projects/OSHA/data/7a743434-d016-4c87-b85a-28af3fc78abb_OSHA-InspectionReport.csv' 
WITH DELIMITER ',' HEADER CSV;

SELECT activity_nr FROM inspections_table;

'''

inspection_table = pd.read_sql_query(sql_query,con)



# CREATE TABLE OF VIOLATION DATA
# 
#
# activity_nr,citation_id,pen_fta,pen_fta_definition,hist_event,
# hist_event_definition,hist_date,hist_penalty,hist_abate_date,
# hist_vtype,hist_insp_nr,load_dt

sql_query = '''
CREATE TABLE violations_table(
activity_nr integer NULL,
citation_id text NULL,
pen_fta char(1) NULL,
pen_fta_definition text NULL,
hist_event char(1) NULL,
hist_event_definition text NULL,
hist_date date NULL,
hist_penalty float NULL,
hist_abate_date date NULL,
hist_vtype text NULL,
hist_insp_nr text NULL,
ld_dt timestamp NULL);


COPY violations_table FROM 
'/Users/asc/Documents/Insight/test_projects/OSHA/data/9c14534c-d40a-4c29-8714-e1f29005b3bc_OSHA-ViolationEvent.csv' 
WITH DELIMITER ',' HEADER CSV;

COMMIT;

SELECT activity_nr, hist_penalty FROM violations_table;

'''

violations_table = pd.read_sql_query(sql_query,con)


# # CLEAN DATA (ON DATABASE)
# 
# *The data, as provided by Enigma, has equivalent representations for some categorical variables of interest. In particular, 'union_status' has the equivalent representations Y=A=U and N=B=NULL. Homgeneize to only take values Y/N*
# 


## Homogeneize labor union affiliations

sql_query = '''
UPDATE inspections_table 
SET union_status='Y'
WHERE union_status='A' OR union_status='U';

UPDATE inspections_table
SET union_status='N'
WHERE union_status='B' or union_status IS NULL;

'''

pd.read_sql_query(sql_query,con)


# # CREATE TARGET VALUES (ON DATABASE)
# *inspections_table does not contain information about whether that inspection ended with or without a violation. That piece of information needs to be obtained from violations_table. By matching the activity_nr in the two tables, which is the code that characterizes the inspection, create new BINARY column on inspections_table with a 0 for inspections that have no found violations and 1 for those that do.*


# Create additional column with all zeros
sql_query = '''
ALTER TABLE inspections_table
ADD is_violation integer DEFAULT 0;
ADD is_violation integer DEFAULT 0;

COMMIT;
'''

pd.read_sql_query(sql_query,con)
    
# Turn into ones the zeros corresponding to violation events
print "ATTENTION! This execution can be pretty slow. Be patient ..."
# NOTE: there may be a more efficient way of doing this via SQL LEFT JOIN command.
#       See https://www.w3schools.com/sql/sql_join_left.asp
#

sql_query = '''
UPDATE inspections_table
SET is_violation=1
WHERE activity_nr IN
(SELECT activity_nr FROM violations_table);

COMMIT;
'''

print "WATCH! This command will place matching values (with is_violation==1) at the BOTTOM of table."

pd.read_sql_query(sql_query,con)

