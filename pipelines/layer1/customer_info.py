import os 
import json
import time 
import random
import configparser
from datetime import datetime
from pathlib import Path
from commons.logs import get_logger
from commons.extract import load_json_data



def measure_processing_time(start_time, end_time, target, logger):
    execution_time = (end_time - start_time) * 1000

    if (execution_time > 1000):
        logger.info(f'2. Execution time for {target}: {execution_time} ms ({ round(execution_time/1000, 2) } secs)')
        logger.info(f'')
    else:
        logger.info(f'2. Execution time for {target}: {execution_time} ms ')
        logger.info(f'')



def exec_query_and_check(cursor, exec_query, check_query, schema_name, logger):
    # Set up SQL statements for schema creation and validation check  
    create_schema = f'''CREATE SCHEMA IF NOT EXISTS {schema_name};'''

    check_if_schema_exists  = f'''SELECT schema_name from information_schema.schemata WHERE schema_name= '{schema_name}';'''

    CREATING_SCHEMA_PROCESSING_START_TIME = time.time()
    cursor.execute(create_schema)
    CREATING_SCHEMA_PROCESSING_END_TIME = time.time()


    CREATING_SCHEMA_VAL_CHECK_START_TIME = time.time()
    cursor.execute(check_if_schema_exists)
    CREATING_SCHEMA_VAL_CHECK_END_TIME = time.time()


    sql_result = cursor.fetchone()[0]
    if sql_result:
        root_logger.info(f"=================================================================================================")
        root_logger.info(f"SCHEMA CREATION SUCCESS: Managed to create {schema_name} schema")
        root_logger.info(f"Schema name in Postgres: {sql_result} ")


    else:
        root_logger.debug(f"")
        root_logger.error(f"=================================================================================================")
        root_logger.error(f"SCHEMA CREATION FAILURE: Unable to create schema for {schema_name}")
        root_logger.info(f"SQL Query for check: {check_if_schema_exists} ")
    
    logger.debug(f"")
    logger.debug(f"")

    measure_processing_time(CREATING_SCHEMA_PROCESSING_START_TIME, CREATING_SCHEMA_PROCESSING_END_TIME, 'CREATE SCHEMA', root_logger)



def create_table(cursor, table_name, root_logger): 
    CREATING_TABLE_PROCESSING_START_TIME = time.time()
    cursor.execute(create_raw_customer_info_tbl)
    CREATING_TABLE_PROCESSING_END_TIME = time.time()

    
    CREATING_TABLE_VAL_CHECK_PROCESSING_START_TIME  =   time.time()
    cursor.execute(check_if_raw_customer_info_tbl_exists)
    CREATING_TABLE_VAL_CHECK_PROCESSING_END_TIME    =   time.time()


    sql_result = cursor.fetchone()[0]
    if sql_result:
        root_logger.debug(f"")
        root_logger.info(f"=============================================================================================================================================================================")
        root_logger.info(f"TABLE CREATION SUCCESS: Managed to create {table_name} table.  ")
        root_logger.info(f"SQL Query for validation check:  {check_if_raw_customer_info_tbl_exists} ")
        root_logger.info(f"=============================================================================================================================================================================")
        root_logger.debug(f"")
    else:
        root_logger.debug(f"")
        root_logger.error(f"==========================================================================================================================================================================")
        root_logger.error(f"TABLE CREATION FAILURE: Unable to create {table_name}... ")
        root_logger.error(f"SQL Query for validation check:  {check_if_raw_customer_info_tbl_exists} ")
        root_logger.error(f"==========================================================================================================================================================================")
        root_logger.debug(f"")
    
    measure_processing_time(CREATING_TABLE_PROCESSING_START_TIME, CREATING_TABLE_PROCESSING_END_TIME, 'CREATE SCHEMA', root_logger)

def delete_table_if_exists(cursor, schema_name, table_name):



def load_customer_data_to_raw_table(postgres_connection, cursor, dbname):
    root_logger = None
    current_filename = Path(__file__).stem

    if __name__=="__main__":
        root_logger = get_logger('layer1', current_filename)
    else:
        root_logger = get_logger('layer1', current_filename)


    customer_info_data = load_json_data('customer_info.json')

    root_logger.info("---------------------------------------------")
    root_logger.info("Start Extract Customer Info Data")

    # Set up constants
    CURRENT_TIMESTAMP               =   datetime.now()
    db_layer_name = dbname
    schema_name = 'main'
    table_name                      =   'raw_customer_info_tbl'
    data_warehouse_layer            =   'RAW'
    source_system                   =   ['CRM', 'ERP', 'Mobile App', 'Website', '3rd party apps', 'Company database']
    row_counter                     =   0 
    column_index                    =   0 
    total_null_values_in_table      =   0 
    successful_rows_upload_count    =   0 
    failed_rows_upload_count        =   0 

    # Set up SQL statements for table deletion and validation check  
    delete_raw_customer_info_tbl_if_exists     =   f''' DROP TABLE IF EXISTS {schema_name}.{table_name} CASCADE;
    '''

    check_if_raw_customer_info_tbl_is_deleted  =   f'''SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}' );
    '''


    # Set up SQL statements for adding data lineage and validation check 
    add_data_lineage_to_raw_customer_info_tbl  =   f'''ALTER TABLE {schema_name}.{table_name}
                                                            ADD COLUMN  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                                            ADD COLUMN  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                                            ADD COLUMN  source_system VARCHAR(255),
                                                            ADD COLUMN  source_file VARCHAR(255),
                                                            ADD COLUMN  load_timestamp TIMESTAMP,
                                                            ADD COLUMN  dwh_layer VARCHAR(255);'''

    check_if_data_lineage_fields_are_added_to_tbl   =   f'''        
                                                                SELECT * 
                                                                FROM    information_schema.columns 
                                                                WHERE   table_name      = '{table_name}' 
                                                                    AND     (column_name    = 'created_at'
                                                                    OR      column_name     = 'updated_at' 
                                                                    OR      column_name     = 'source_system' 
                                                                    OR      column_name     = 'source_file' 
                                                                    OR      column_name     = 'load_timestamp' 
                                                                    OR      column_name     = 'dwh_layer');
                                                                            
    '''
    
    check_total_row_count_before_insert_statement   =   f'''   SELECT COUNT(*) FROM {schema_name}.{table_name}
    '''

    # Set up SQL statements for records insert and validation check
    insert_customer_info_data  =   f'''                       INSERT INTO {schema_name}.{table_name} (
                                                                            address, 
                                                                            age, 
                                                                            city, 
                                                                            created_date, 
                                                                            credit_card, 
                                                                            credit_card_provider, 
                                                                            customer_contact_preference_desc,
                                                                            customer_contact_preference_id, 
                                                                            customer_id, 
                                                                            dob, 
                                                                            email, 
                                                                            first_name, 
                                                                            last_name, 
                                                                            last_updated_date, 
                                                                            nationality,
                                                                            phone_number, 
                                                                            place_of_birth, 
                                                                            state, 
                                                                            zip, 
                                                                            created_at, 
                                                                            updated_at, 
                                                                            source_system, 
                                                                            source_file, 
                                                                            load_timestamp, 
                                                                            dwh_layer
                                                                        )
                                                                        VALUES (
                                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                                                        );
    '''

    check_total_row_count_after_insert_statement    =   f'''        SELECT COUNT(*) FROM {schema_name}.{table_name}
    '''


    
    count_total_no_of_columns_in_table  =   f'''            SELECT          COUNT(column_name) 
                                                            FROM            information_schema.columns 
                                                            WHERE           table_name      =   '{table_name}'
                                                            AND             table_schema    =   '{schema_name}'
    '''

    count_total_no_of_unique_records_in_table   =   f'''        SELECT COUNT(*) FROM 
                                                                        (SELECT DISTINCT * FROM {schema_name}.{table_name}) as unique_records   
    '''
    get_list_of_column_names    =   f'''                    SELECT      column_name
                                                            FROM        information_schema.columns  
                                                            WHERE       table_name   =  '{table_name}'
                                                            ORDER BY    ordinal_position 

    '''


    cursor = create_db_schema(cursor, schema_name)

    # Delete table if it exists in Postgres
    DELETING_SCHEMA_PROCESSING_START_TIME   =   time.time()
    cursor.execute(delete_raw_customer_info_tbl_if_exists)
    DELETING_SCHEMA_PROCESSING_END_TIME     =   time.time()

    
    DELETING_SCHEMA_VAL_CHECK_PROCESSING_START_TIME     =   time.time()
    cursor.execute(check_if_raw_customer_info_tbl_is_deleted)
    DELETING_SCHEMA_VAL_CHECK_PROCESSING_END_TIME       =   time.time()


    sql_result = cursor.fetchone()[0]
    if sql_result:
        root_logger.debug(f"")
        root_logger.info(f"=============================================================================================================================================================================")
        root_logger.info(f"TABLE DELETION SUCCESS: Managed to drop {table_name} table in {db_layer_name}. Now advancing to recreating table... ")
        root_logger.info(f"SQL Query for validation check:  {check_if_raw_customer_info_tbl_is_deleted} ")
        root_logger.info(f"=============================================================================================================================================================================")
        root_logger.debug(f"")
    else:
        root_logger.debug(f"")
        root_logger.error(f"==========================================================================================================================================================================")
        root_logger.error(f"TABLE DELETION FAILURE: Unable to delete {table_name}. This table may have objects that depend on it (use DROP TABLE ... CASCADE to resolve) or it doesn't exist. ")
        root_logger.error(f"SQL Query for validation check:  {check_if_raw_customer_info_tbl_is_deleted} ")
        root_logger.error(f"==========================================================================================================================================================================")
        root_logger.debug(f"")






    # Add data lineage to table 
    ADDING_DATA_LINEAGE_PROCESSING_START_TIME   =   time.time()
    cursor.execute(add_data_lineage_to_raw_customer_info_tbl)
    ADDING_DATA_LINEAGE_PROCESSING_END_TIME     =   time.time()

    
    ADDING_DATA_LINEAGE_VAL_CHECK_PROCESSING_START_TIME  =  time.time()
    cursor.execute(check_if_data_lineage_fields_are_added_to_tbl)
    ADDING_DATA_LINEAGE_VAL_CHECK_PROCESSING_END_TIME    =  time.time()


    sql_results = cursor.fetchall()
    
    if len(sql_results) == 6:
        root_logger.debug(f"")
        root_logger.info(f"=============================================================================================================================================================================")
        root_logger.info(f"DATA LINEAGE FIELDS CREATION SUCCESS: Managed to create data lineage columns in {schema_name}.{table_name}.  ")
        root_logger.info(f"SQL Query for validation check:  {check_if_data_lineage_fields_are_added_to_tbl} ")
        root_logger.info(f"=============================================================================================================================================================================")
        root_logger.debug(f"")
    else:
        root_logger.debug(f"")
        root_logger.error(f"==========================================================================================================================================================================")
        root_logger.error(f"DATA LINEAGE FIELDS CREATION FAILURE: Unable to create data lineage columns in {schema_name}.{table_name}.... ")
        root_logger.error(f"SQL Query for validation check:  {check_if_data_lineage_fields_are_added_to_tbl} ")
        root_logger.error(f"==========================================================================================================================================================================")
        root_logger.debug(f"")



    # Add insert rows to table 
    ROW_INSERTION_PROCESSING_START_TIME     =   time.time()
    cursor.execute(check_total_row_count_before_insert_statement)
    sql_result = cursor.fetchone()[0]
    root_logger.info(f"Rows before SQL insert in Postgres: {sql_result} ")
    root_logger.debug(f"")


    for customer_info in customer_info_data:
        values = (
            customer_info['address'], 
            customer_info['age'], 
            customer_info['city'], 
            customer_info['created_date'], 
            customer_info['credit_card'], 
            customer_info['credit_card_provider'], 
            json.dumps(customer_info['customer_contact_preference_desc']),
            customer_info['customer_contact_preference_id'], 
            customer_info['customer_id'], 
            customer_info['dob'], 
            customer_info['email'], 
            customer_info['first_name'], 
            customer_info['last_name'], 
            customer_info['last_updated_date'], 
            customer_info['nationality'],
            customer_info['phone_number'], 
            customer_info['place_of_birth'], 
            customer_info['state'], 
            customer_info['zip'],
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP,
            random.choice(source_system),
            src_file,
            CURRENT_TIMESTAMP,
            'RAW'
            )

        cursor.execute(insert_customer_info_data, values)


        # Validate if each row inserted into the table exists 
        if cursor.rowcount == 1:
            row_counter += 1
            successful_rows_upload_count += 1
            root_logger.debug(f'---------------------------------')
            root_logger.info(f'INSERT SUCCESS: Uploaded customer_info record no {row_counter} ')
            root_logger.debug(f'---------------------------------')
        else:
            row_counter += 1
            failed_rows_upload_count +=1
            root_logger.error(f'---------------------------------')
            root_logger.error(f'INSERT FAILED: Unable to insert customer_info record no {row_counter} ')
            root_logger.error(f'---------------------------------')


    
    ROW_INSERTION_PROCESSING_END_TIME   =   time.time()


    ROW_COUNT_VAL_CHECK_PROCESSING_START_TIME   =   time.time()
    cursor.execute(check_total_row_count_after_insert_statement)
    ROW_COUNT_VAL_CHECK_PROCESSING_END_TIME     =   time.time()


    total_rows_in_table = cursor.fetchone()[0]
    root_logger.info(f"Rows after SQL insert in Postgres: {total_rows_in_table} ")
    root_logger.debug(f"")



    # ======================================= SENSITIVE COLUMN IDENTIFICATION =======================================

    note_1 = """IMPORTANT NOTE: Invest time in understanding the underlying data fields to avoid highlighting the incorrect fields or omitting fields containing confidential information.          """
    note_2 = """      Involving the relevant stakeholders in the process of identifying sensitive data fields from the source data is a crucial step to protecting confidential information. """
    note_3 = """      Neglecting this step could expose customers and the wider company to serious harm (e.g. cybersecurity hacks, data breaches, unauthorized access to sensitive data), so approach this task with the utmost care. """
    
    root_logger.warning(f'')
    root_logger.warning(f'')
    root_logger.warning('================================================')
    root_logger.warning('           SENSITIVE COLUMN IDENTIFICATION              ')
    root_logger.warning('================================================')
    root_logger.warning(f'')
    root_logger.error(f'{note_1}')
    root_logger.error(f'')
    root_logger.error(f'{note_2}')
    root_logger.error(f'')
    root_logger.error(f'{note_3}')
    root_logger.warning(f'')
    root_logger.warning(f'')
    root_logger.warning(f'Now beginning the sensitive column identification stage ...')
    root_logger.warning(f'')
    

    # Add a flag for confirming if sensitive data fields have been highlighted  
    sensitive_columns_selected = ['customer_id',
                                    'address',
                                    'age',
                                    'city',
                                    'created_date',
                                    'credit_card',
                                    'credit_card_provider',
                                    'customer_contact_preference_desc',
                                    'customer_contact_preference_id',
                                    'dob',
                                    'email'  ,
                                    'first_name',
                                    'last_name',
                                    'last_updated_date',
                                    'nationality',
                                    'phone_number',
                                    'place_of_birth',
                                    'state',
                                    'zip'
                        ]
    
    

    if len(sensitive_columns_selected) == 0:
        SENSITIVE_COLUMNS_IDENTIFIED = False
        root_logger.error(f"ERROR: No sensitive columns have been selected for '{table_name}' table ")
        root_logger.warning(f'')
    
    elif sensitive_columns_selected[0] is None:
        SENSITIVE_COLUMNS_IDENTIFIED = True
        root_logger.error(f"There are no sensitive columns for the '{table_name}' table ")
        root_logger.warning(f'')

    else:
        SENSITIVE_COLUMNS_IDENTIFIED = True
        root_logger.warning(f'Here are the columns considered sensitive in this table ...')
        root_logger.warning(f'')

    
    if SENSITIVE_COLUMNS_IDENTIFIED is False:
        sql_statement_for_listing_columns_in_table = f"""        
        SELECT column_name FROM information_schema.columns 
        WHERE   table_name = '{table_name}'
        ORDER BY ordinal_position 
        """
        cursor.execute(get_list_of_column_names)
        list_of_column_names = cursor.fetchall()
        column_names = [sql_result[0] for sql_result in list_of_column_names]
        
        root_logger.warning(f"You are required to select the sensitive columns in this table. If there are none, enter 'None' in the 'sensitive_columns_selected' object.")
        root_logger.warning(f'')
        root_logger.warning(f"Here are the columns to choose from:")
        root_logger.warning(f'')
        total_sensitive_columns = 0
        for sensitive_column_name in column_names:
            total_sensitive_columns += 1
            root_logger.warning(f'''{total_sensitive_columns} : '{sensitive_column_name}'  ''')



        root_logger.warning(f'')
        root_logger.warning(f'You can use this SQL query to list the columns in this table:')
        root_logger.warning(f'              {sql_statement_for_listing_columns_in_table}                ')
    
    else:
        total_sensitive_columns = 0
        for sensitive_column_name in sensitive_columns_selected:
            total_sensitive_columns += 1
            root_logger.warning(f'''{total_sensitive_columns} : '{sensitive_column_name}'  ''')
        if sensitive_columns_selected[0] is not None:
            root_logger.warning(f'')
            root_logger.warning(f'')
            root_logger.warning(f'Decide on the appropriate treatment for these tables. A few options to consider include:')
            root_logger.warning(f'''1. Masking fields               -   This involves replacing sensitive columns with alternative characters e.g.  'xxxx-xxxx', '*****', '$$$$'. ''')
            root_logger.warning(f'''2. Encrypting fields            -   This is converting sensitive columns to cipher text (unreadable text format).        ''')
            root_logger.warning(f'''3. Role-based access control    -   Placing a system that delegates privileges based on team members' responsibilities        ''')
        
        root_logger.warning(f'')
        root_logger.warning(f'Now terminating the sensitive column identification stage ...')
        root_logger.warning(f'Sensitive column identification stage ended. ')
        root_logger.warning(f'')


    root_logger.warning(f'')
    root_logger.warning(f'')









    # ======================================= DATA PROFILING METRICS =======================================


    # Prepare data profiling metrics 


    # --------- A. Table statistics 
    cursor.execute(count_total_no_of_columns_in_table)
    total_columns_in_table = cursor.fetchone()[0]

    cursor.execute(count_total_no_of_unique_records_in_table)
    total_unique_records_in_table = cursor.fetchone()[0]
    total_duplicate_records_in_table = total_rows_in_table - total_unique_records_in_table


    cursor.execute(get_list_of_column_names)
    list_of_column_names = cursor.fetchall()
    column_names = [sql_result[0] for sql_result in list_of_column_names]


    EXECUTION_TIME_FOR_DROPPING_SCHEMA                   =   (DELETING_SCHEMA_PROCESSING_END_TIME                -       DELETING_SCHEMA_PROCESSING_START_TIME                   )   * 1000


    EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK         =   (DELETING_SCHEMA_VAL_CHECK_PROCESSING_END_TIME      -       DELETING_SCHEMA_VAL_CHECK_PROCESSING_START_TIME         )   * 1000


    EXECUTION_TIME_FOR_CREATING_TABLE                    =   (CREATING_TABLE_PROCESSING_END_TIME                 -       CREATING_TABLE_PROCESSING_START_TIME                    )   * 1000


    EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK          =   (CREATING_TABLE_VAL_CHECK_PROCESSING_END_TIME       -       CREATING_TABLE_VAL_CHECK_PROCESSING_START_TIME          )   * 1000


    EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE               =   (ADDING_DATA_LINEAGE_PROCESSING_END_TIME            -       ADDING_DATA_LINEAGE_PROCESSING_START_TIME               )   * 1000


    EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK     =   (ADDING_DATA_LINEAGE_VAL_CHECK_PROCESSING_END_TIME  -       ADDING_DATA_LINEAGE_VAL_CHECK_PROCESSING_START_TIME     )   * 1000


    EXECUTION_TIME_FOR_ROW_INSERTION                     =   (ROW_INSERTION_PROCESSING_END_TIME                  -       ROW_INSERTION_PROCESSING_START_TIME                     )   * 1000


    EXECUTION_TIME_FOR_ROW_COUNT                         =   (ROW_COUNT_VAL_CHECK_PROCESSING_END_TIME            -       ROW_COUNT_VAL_CHECK_PROCESSING_START_TIME               )   * 1000




    # Display data profiling metrics
    
    root_logger.info(f'')
    root_logger.info(f'')
    root_logger.info('================================================')
    root_logger.info('              DATA PROFILING METRICS              ')
    root_logger.info('================================================')
    root_logger.info(f'')
    root_logger.info(f'Now calculating table statistics...')
    root_logger.info(f'')
    root_logger.info(f'')
    root_logger.info(f'Table name:                                  {table_name} ')
    root_logger.info(f'Schema name:                                 {schema_name} ')
    root_logger.info(f'Database name:                               {database} ')
    root_logger.info(f'Data warehouse layer:                        {data_warehouse_layer} ')
    root_logger.info(f'')
    root_logger.info(f'')
    root_logger.info(f'Number of rows in table:                     {total_rows_in_table} ')
    root_logger.info(f'Number of columns in table:                  {total_columns_in_table} ')
    root_logger.info(f'')


    if successful_rows_upload_count == total_rows_in_table:
        root_logger.info(f'Successful records uploaded total :          {successful_rows_upload_count} / {total_rows_in_table}   ')
        root_logger.info(f'Failed/Errored records uploaded total:       {failed_rows_upload_count} / {total_rows_in_table}       ')
        root_logger.info(f'')
        root_logger.info(f'Successful records uploaded % :              {(successful_rows_upload_count / total_rows_in_table) * 100}    ')
        root_logger.info(f'Failed/Errored records uploaded %:           {(failed_rows_upload_count/total_rows_in_table) * 100}       ')
        root_logger.info(f'')
    else:
        root_logger.warning(f'Successful records uploaded total :          {successful_rows_upload_count} / {total_rows_in_table}   ')
        root_logger.warning(f'Failed/Errored records uploaded total:       {failed_rows_upload_count} / {total_rows_in_table}       ')
        root_logger.warning(f'')
        root_logger.warning(f'Successful records uploaded % :              {(successful_rows_upload_count / total_rows_in_table) * 100}    ')
        root_logger.warning(f'Failed/Errored records uploaded %:           {(failed_rows_upload_count/total_rows_in_table) * 100}       ')
        root_logger.warning(f'')


    if total_unique_records_in_table == total_rows_in_table:
        root_logger.info(f'Number of unique records:                    {total_unique_records_in_table} / {total_rows_in_table}')
        root_logger.info(f'Number of duplicate records:                 {total_duplicate_records_in_table} / {total_rows_in_table}')
        root_logger.info(f'')
        root_logger.info(f'Unique records %:                            {(total_unique_records_in_table / total_rows_in_table) * 100} ')
        root_logger.info(f'Duplicate records %:                         {(total_duplicate_records_in_table / total_rows_in_table)  * 100} ')
        root_logger.info(f'')
    
    else:
        root_logger.warning(f'Number of unique records:                    {total_unique_records_in_table} / {total_rows_in_table}')
        root_logger.warning(f'Number of duplicate records:                 {total_duplicate_records_in_table} / {total_rows_in_table}')
        root_logger.warning(f'')
        root_logger.warning(f'Unique records %:                            {(total_unique_records_in_table / total_rows_in_table) * 100} ')
        root_logger.warning(f'Duplicate records %:                         {(total_duplicate_records_in_table / total_rows_in_table)  * 100} ')
        root_logger.warning(f'')
    

    for column_name in column_names:
        cursor.execute(f'''
                SELECT COUNT(*)
                FROM {schema_name}.{table_name}
                WHERE {column_name} is NULL
        ''')
        sql_result = cursor.fetchone()[0]
        total_null_values_in_table += sql_result
        column_index += 1
        if sql_result == 0:
            root_logger.info(f'Column name: {column_name},  Column no: {column_index},  Number of NULL values: {sql_result} ')
        else:
            root_logger.warning(f'Column name: {column_name},  Column no: {column_index},  Number of NULL values: {sql_result} ')
    



    root_logger.info(f'')
    root_logger.info('================================================')
    root_logger.info(f'')
    root_logger.info(f'Now calculating performance statistics (from a Python standpoint)...')
    root_logger.info(f'')
    root_logger.info(f'')

    

    if (EXECUTION_TIME_FOR_DROPPING_SCHEMA > 1000) and (EXECUTION_TIME_FOR_DROPPING_SCHEMA < 60000):
        root_logger.info(f'3. Execution time for DELETING schema:  {EXECUTION_TIME_FOR_DROPPING_SCHEMA} ms ({  round   (EXECUTION_TIME_FOR_DROPPING_SCHEMA  /   1000, 2)} secs)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    elif (EXECUTION_TIME_FOR_DROPPING_SCHEMA >= 60000):
        root_logger.info(f'3. Execution time for DELETING schema:  {EXECUTION_TIME_FOR_DROPPING_SCHEMA} ms ({  round   (EXECUTION_TIME_FOR_DROPPING_SCHEMA  /   1000, 2)} secs)    ({  round ((EXECUTION_TIME_FOR_DROPPING_SCHEMA  /   1000) / 60,  4)   } min)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    else:
        root_logger.info(f'3. Execution time for DELETING schema:  {EXECUTION_TIME_FOR_DROPPING_SCHEMA} ms ')
        root_logger.info(f'')
        root_logger.info(f'')



    if (EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK > 1000) and (EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK < 60000):
        root_logger.info(f'4. Execution time for DELETING schema (VAL CHECK):  {EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK} ms ({  round   (EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK  /   1000, 2)} secs)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    elif (EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK >= 60000):
        root_logger.info(f'4. Execution time for DELETING schema (VAL CHECK):  {EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK} ms ({  round   (EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK  /   1000, 2)} secs)    ({  round ((EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK  /   1000) / 60,  4)   } min)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    else:
        root_logger.info(f'4. Execution time for DELETING schema (VAL CHECK):  {EXECUTION_TIME_FOR_DROPPING_SCHEMA_VAL_CHECK} ms ')
        root_logger.info(f'')
        root_logger.info(f'')

    

    if (EXECUTION_TIME_FOR_CREATING_TABLE > 1000) and (EXECUTION_TIME_FOR_CREATING_TABLE < 60000):
        root_logger.info(f'5. Execution time for CREATING table:  {EXECUTION_TIME_FOR_CREATING_TABLE} ms ({  round   (EXECUTION_TIME_FOR_CREATING_TABLE  /   1000, 2)} secs)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    elif (EXECUTION_TIME_FOR_CREATING_TABLE >= 60000):
        root_logger.info(f'5. Execution time for CREATING table:  {EXECUTION_TIME_FOR_CREATING_TABLE} ms ({  round   (EXECUTION_TIME_FOR_CREATING_TABLE  /   1000, 2)} secs)    ({  round ((EXECUTION_TIME_FOR_CREATING_TABLE  /   1000) / 60,  4)   } min)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    else:
        root_logger.info(f'5. Execution time for CREATING table:  {EXECUTION_TIME_FOR_CREATING_TABLE} ms ')
        root_logger.info(f'')
        root_logger.info(f'')



    if (EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK > 1000) and (EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK < 60000):
        root_logger.info(f'6. Execution time for CREATING table (VAL CHECK):  {EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK} ms ({  round   (EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK  /   1000, 2)} secs)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    elif (EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK >= 60000):
        root_logger.info(f'6. Execution time for CREATING table (VAL CHECK):  {EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK} ms ({  round   (EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK  /   1000, 2)} secs)  ({  round ((EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK  /   1000) / 60,  4)   } min)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    else:
        root_logger.info(f'6. Execution time for CREATING table (VAL CHECK):  {EXECUTION_TIME_FOR_CREATING_TABLE_VAL_CHECK} ms ')
        root_logger.info(f'')
        root_logger.info(f'')



    if (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE > 1000) and (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE < 60000):
        root_logger.info(f'7. Execution time for ADDING data lineage:  {EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE} ms ({  round   (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE  /   1000, 2)} secs)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    elif (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE >= 60000):
        root_logger.info(f'7. Execution time for ADDING data lineage:  {EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE} ms ({  round   (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE  /   1000, 2)} secs)  ({  round ((EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE  /   1000) / 60,  4)   } min)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    else:
        root_logger.info(f'7. Execution time for ADDING data lineage:  {EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE} ms ')
        root_logger.info(f'')
        root_logger.info(f'')



    if (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK > 1000) and (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK < 60000):
        root_logger.info(f'8. Execution time for ADDING data lineage (VAL CHECK):  {EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK} ms ({  round   (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK  /   1000, 2)} secs)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    elif (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK >= 60000):
        root_logger.info(f'8. Execution time for ADDING data lineage (VAL CHECK):  {EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK} ms ({  round   (EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK  /   1000, 2)} secs)   ({  round ((EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK  /   1000) / 60,  4)   } min)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    else:
        root_logger.info(f'8. Execution time for ADDING data lineage (VAL CHECK):  {EXECUTION_TIME_FOR_ADDING_DATA_LINEAGE_VAL_CHECK} ms ')
        root_logger.info(f'')
        root_logger.info(f'')



    if (EXECUTION_TIME_FOR_ROW_INSERTION > 1000) and (EXECUTION_TIME_FOR_ROW_INSERTION < 60000):
        root_logger.info(f'9. Execution time for INSERTING rows to table:  {EXECUTION_TIME_FOR_ROW_INSERTION} ms ({  round   (EXECUTION_TIME_FOR_ROW_INSERTION  /   1000, 2)} secs)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    elif (EXECUTION_TIME_FOR_ROW_INSERTION >= 60000):
        root_logger.info(f'9. Execution time for INSERTING rows to table:  {EXECUTION_TIME_FOR_ROW_INSERTION} ms ({  round   (EXECUTION_TIME_FOR_ROW_INSERTION  /   1000, 2)} secs)   ({  round ((EXECUTION_TIME_FOR_ROW_INSERTION  /   1000) / 60,  4)   } min)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    else:
        root_logger.info(f'9. Execution time for INSERTING rows to table:  {EXECUTION_TIME_FOR_ROW_INSERTION} ms ')
        root_logger.info(f'')
        root_logger.info(f'')



    if (EXECUTION_TIME_FOR_ROW_COUNT > 1000) and (EXECUTION_TIME_FOR_ROW_COUNT < 60000):
        root_logger.info(f'10. Execution time for COUNTING uploaded rows to table:  {EXECUTION_TIME_FOR_ROW_COUNT} ms ({  round   (EXECUTION_TIME_FOR_ROW_COUNT  /   1000, 2)} secs)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    elif (EXECUTION_TIME_FOR_ROW_COUNT >= 60000):
        root_logger.info(f'10. Execution time for COUNTING uploaded rows to table:  {EXECUTION_TIME_FOR_ROW_COUNT} ms ({  round   (EXECUTION_TIME_FOR_ROW_COUNT  /   1000, 2)} secs)    ({  round ((EXECUTION_TIME_FOR_ROW_COUNT  /   1000) / 60,  4)   } min)      ')
        root_logger.info(f'')
        root_logger.info(f'')
    else:
        root_logger.info(f'10. Execution time for COUNTING uploaded rows to table:  {EXECUTION_TIME_FOR_ROW_COUNT} ms ')
        root_logger.info(f'')
        root_logger.info(f'')



    root_logger.info(f'')
    root_logger.info('================================================')


    # Add conditional statements for data profile metrics 

    if successful_rows_upload_count != total_rows_in_table:
        if successful_rows_upload_count == 0:
            root_logger.error(f"ERROR: No records were upload to '{table_name}' table....")
            raise ImportError("Trace filepath to highlight the root cause of the missing rows...")
        else:
            root_logger.error(f"ERROR: There are only {successful_rows_upload_count} records upload to '{table_name}' table....")
            raise ImportError("Trace filepath to highlight the root cause of the missing rows...")
    

    elif failed_rows_upload_count > 0:
        root_logger.error(f"ERROR: A total of {failed_rows_upload_count} records failed to upload to '{table_name}' table....")
        raise ImportError("Trace filepath to highlight the root cause of the missing rows...")
    

    elif total_unique_records_in_table != total_rows_in_table:
        root_logger.error(f"ERROR: There are {total_duplicate_records_in_table} duplicated records in the uploads for '{table_name}' table....")
        raise ImportError("Trace filepath to highlight the root cause of the duplicated rows...")


    elif total_duplicate_records_in_table > 0:
        root_logger.error(f"ERROR: There are {total_duplicate_records_in_table} duplicated records in the uploads for '{table_name}' table....")
        raise ImportError("Trace filepath to highlight the root cause of the duplicated rows...")
    

    elif total_null_values_in_table > 0:
        root_logger.error(f"ERROR: There are {total_duplicate_records_in_table} NULL values in '{table_name}' table....")
        raise ImportError("Examine table to highlight the columns with the NULL values - justify if these fields should contain NULLs ...")



    else:
        root_logger.debug("")
        root_logger.info("DATA VALIDATION SUCCESS: All general DQ checks passed! ")
        root_logger.debug("")





    # Commit the changes made in Postgres 
    root_logger.info("Now saving changes made by SQL statements to Postgres DB....")
    # postgres_connection.commit()
    root_logger.info("Saved successfully, now terminating cursor and current session....")