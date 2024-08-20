import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def create_database_if_not_exists():
    """
    Create the database if it does not exist.
    """
    # Connect to the default database (postgres) to create a new database
    conn_str = 'postgresql://postgres:postgres@postgres:5432/postgres'
    
    # Use psycopg2 to connect and create the database
    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = True  # Enable autocommit mode to run CREATE DATABASE
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier('healthcare_data')
                ))
                print("Database created successfully.")
            except psycopg2.errors.DuplicateDatabase:
                print("Database already exists.")
    except Exception as e:
        print(f"Failed to create database: {e}")
    finally:
        conn.close()

@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Load data from a local file, map data types, and load it into PostgreSQL.
    """
    # Step 1: Create the database if it doesn't exist
    create_database_if_not_exists()

    # Connect to the new database and load data
    db_params = {
        'dbname': 'healthcare_data',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'postgres',
        'port': '5432'
    }
    
    # Create a connection string for the new database
    conn_str = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
    
    # Create a SQLAlchemy engine for the new database
    engine = create_engine(conn_str)

    # Step 2: Load the data from the CSV file into a DataFrame
    filepath = '/home/src/archive/healthcare_dataset.csv'
    df = pd.read_csv(filepath)

    # Replace spaces with underscores for all column names
    df.columns = df.columns.str.replace(' ', '_')
    
    # Step 3: Map data types
    df['Date_of_Admission'] = pd.to_datetime(df['Date_of_Admission'])
    df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])
    df['Gender'] = df['Gender'].astype('category')
    df['Medical_Condition'] = df['Medical_Condition'].astype('category')
    df['Blood_Type'] = df['Blood_Type'].astype('category')
    df['Age'] = df['Age'].astype(int)
    
    # Step 4: Write the DataFrame to PostgreSQL
    df.to_sql('healthcare_data', engine, if_exists='replace', index=False)


    return df

@test
def test_output(output, *args) -> None:
    """
    Test the output of the data loader.
    """
    assert output is not None, 'The output is undefined'
