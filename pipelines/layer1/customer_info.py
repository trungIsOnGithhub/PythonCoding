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


def exec_query_and_check(cursor, exec_query, check_query, logger):
    # Set up SQL statements for schema creation and validation check  
    create_schema = f'''CREATE SCHEMA IF NOT EXISTS {schema_name};'''
    check_if_schema_exists  = f'''SELECT schema_name from information_schema.schemata WHERE schema_name= '{schema_name}';'''

    EXECUTION_START_TIME = time.time()
    cursor.execute(exec_query)
    EXECUTION_END_TIME = time.time()

    CHECK_START_TIME = time.time()
    cursor.execute(check_query)
    CHECK_END_TIME = time.time()

    sql_result = cursor.fetchone()[0]
    if sql_result:
        root_logger.info(f"=================================================================================================")
        root_logger.info(f"EXECUTE SUCCESS {exec_query} schema")
        root_logger.info(f"=================================================================================================")
        root_logger.info(f"RESULT: {sql_result} ")


    else:
        root_logger.debug(f"")
        root_logger.error(f"=================================================================================================")
        root_logger.error(f"EXECUTE FAILED: {exec_query}")
        root_logger.error(f"CHECK QUERY: {check_query}")
        root_logger.error(f"=================================================================================================")
    
    logger.debug(f"")
    logger.debug(f"")

    measure_processing_time(EXECUTION_START_TIME, EXECUTION_END_TIME, 'Query Exec', logger)
    measure_processing_time(CHECK_START_TIME, CHECK_END_TIME, 'Query Check', logger)


# def delete_table_if_exists(cursor, schema_name, table_name):


def table_profiling_metrics(cursor, count_column_query, count_unique_records_query, get_column_names_query, successful_rows_count, failed_rows_count, total_rows_in_table, logger):
    cursor.execute(count_column_query)
    total_columns_in_table = cursor.fetchone()[0]

    cursor.execute(count_unique_records_query)
    total_unique_records_in_table = cursor.fetchone()[0]
    total_duplicate_records_in_table = total_rows_in_table - total_unique_records_in_table


    cursor.execute(get_column_names_query)
    list_of_column_names = cursor.fetchall()
    column_names = [sql_result[0] for sql_result in list_of_column_names]

    if successful_rows_count != total_rows_in_table:
        logger.error(f"ERROR: There are only {successful_rows_count} records upload to table....")
        raise Exception('successful_rows_count != total_rows_in_table')
    elif failed_rows_count > 0:
        logger.error(f"ERROR: A total of {failed_rows_count} records failed to upload to table....")
        raise Exception()
    elif total_unique_records_in_table != total_rows_in_table:
        logger.error(f"ERROR: There are {total_duplicate_records_in_table} duplicated records in the uploads for table....")
        raise Exception("total_unique_records_in_table != total_rows_in_table")
    elif total_duplicate_records_in_table > 0:
        logger.error(f"ERROR: There are {total_duplicate_records_in_table} duplicated records in the uploads for table....")
        raise Exception("total_duplicate_records_in_table > 0")

    return column_names


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



    create_schema = f'''CREATE SCHEMA IF NOT EXISTS {schema_name};'''
    check_if_schema_exists = f'''SELECT schema_name from information_schema.schemata WHERE schema_name= '{schema_name}';'''

    cursor = exec_query_and_check(cursor, create_schema, check_if_schema_exists, root_logger)



    create_raw_table = f'''CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                                        customer_id UUID PRIMARY KEY,
                                        address varchar(255),
                                        age NUMERIC(18, 6),
                                        city varchar(255),
                                        created_date bigint,
                                        credit_card varchar(255),
                                        credit_card_provider varchar(255),
                                        customer_contact_preference_desc        varchar,
                                        customer_contact_preference_id          UUID,
                                        dob                                     bigint,
                                        email                                   varchar(255),
                                        first_name                              varchar(255),
                                        last_name                               varchar(255),
                                        last_updated_date                       bigint,
                                        nationality                             varchar(255),
                                        phone_number                            varchar(255),
                                        place_of_birth                          varchar(255),
                                        state                                   varchar(255),
                                        zip                                     varchar(255));'''
    check_if_raw_table_exists  =   f'''SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');'''

    cursor = exec_query_and_check(cursor, create_raw_table, check_if_raw_table_exists, root_logger)



    delete_raw_table_if_exists = f'''DROP TABLE IF EXISTS {schema_name}.{table_name} CASCADE;'''
    check_if_raw_table_deleted = f'''SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');'''

    cursor = exec_query_and_check(cursor, delete_raw_table_if_exists, check_if_raw_table_deleted, root_logger)





    add_data_lineage  =   f'''ALTER TABLE {schema_name}.{table_name}
                            ADD COLUMN  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            ADD COLUMN  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                            ADD COLUMN  source_system VARCHAR(255),
                            ADD COLUMN  source_file VARCHAR(255),
                            ADD COLUMN  load_timestamp TIMESTAMP,
                            ADD COLUMN  dwh_layer VARCHAR(255);'''
    check_data_lineage = f'''SELECT * 
                             FROM    information_schema.columns 
                             WHERE   table_name      = '{table_name}' 
                                AND     (column_name    = 'created_at'
                                OR      column_name     = 'updated_at' 
                                OR      column_name     = 'source_system' 
                                OR      column_name     = 'source_file' 
                                OR      column_name     = 'load_timestamp' 
                                OR      column_name     = 'dwh_layer');'''

    cursor = exec_query_and_check(cursor, delete_raw_table_if_exists, check_if_raw_table_deleted, root_logger)


    sql_results = cursor.fetchall()

    
    if len(sql_results) != 6: # 6 col
        root_logger.error(f"==========================================================================================================================================================================")
        root_logger.error(f"DATA LINEAGE FIELDS CREATE FAILURE: {schema_name}.{table_name}.... ")
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
    root_logger.info(f"TOTAL ROW INSERTED: {total_rows_in_table} ")
    root_logger.debug(f"")


    


    # Display data profiling metrics
    
    root_logger.info(f'')
    root_logger.info(f'')
    root_logger.info(f'TABLE STATISTICS')
    root_logger.info(f'')
    root_logger.info(f'')
    root_logger.info(f'Table name:                                  {table_name} ')
    root_logger.info(f'Schema name:                                 {schema_name} ')
    root_logger.info(f'Database name:                               {dbname} ')
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
    



    # Add conditional statements for data profile metrics
    check_total_row_count_after_insert_statement = f'''SELECT COUNT(*) FROM {schema_name}.{table_name}'''    
    count_columns_in_table = f'''SELECT COUNT(column_name) 
                                            FROM information_schema.columns 
                                            WHERE table_name = '{table_name}'
                                            AND table_schema = '{schema_name}'
    '''
    count_unique_records_in_table = f'''SELECT COUNT(*) FROM (SELECT DISTINCT * FROM {schema_name}.{table_name}) as unique_records'''
    get_column_names = f'''SELECT      column_name
                                        FROM        information_schema.columns  
                                        WHERE       table_name   =  '{table_name}'
                                        ORDER BY    ordinal_position '''

    table_profiling_metrics(cursor, count_columns_in_table, count_unique_records_in_table, get_column_names)





    # Commit the changes made in Postgres 
    root_logger.info("Now saving changes made by SQL statements to Postgres DB....")
    # postgres_connection.commit()
    root_logger.info("Saved successfully, now terminating cursor and current session....")