import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2
from itertools import islice

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Repositories Decoder").sheet1

dbhost = 'localhost' 
dbuser = 'postgres' 
dbpass = 'MY PASSWORD' 
database = 'postgres' 

dwarehouse_conn = psycopg2.connect(dbname=database, 
                                    user=dbuser, 
                                    host=dbhost,
                                    password=dbpass,
                                    port='5432')
cursor = dwarehouse_conn.cursor()

repo_product_info_count_sql = 'SELECT COUNT(*) FROM repositories_product_information'
cursor.execute(repo_product_info_count_sql)
count_result = cursor.fetchone()

num_rows_repo_products = count_result[0]

num_rows_sheets = len(sheet.get_all_values())

num_rows_sheets = num_rows_sheets - 1

iterable_results = iter(sheet.get_all_values())

next(iterable_results)

for i, value in islice(enumerate(iterable_results), num_rows_repo_products, None):
    if not value[0]:
        continue
    referer = value[0]
    hardware_platform = "" if not value[1] else value[1]
    os = "" if not value[2] else value[2]
    os_version = "" if not value[3] else value[3]
    product_name = "" if not value[4] else value[4]
    product_version = "" if not value[5] else value[5]
    packaging = "" if not value[6] else value[6]
    campaign = "" if not value[7] else value[7]

    query = (
        "INSERT INTO repositories_product_information (referer, hardware_platform, os, os_version, product, product_version, packaging, campaign_id)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (
        referer, hardware_platform, os, os_version, product_name, product_version, packaging, campaign))
    dwarehouse_conn.commit()

    print (value)
