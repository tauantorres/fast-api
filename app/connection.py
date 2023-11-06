import psycopg

database = "fastapi"
host = "localhost"
user = "postgres"
password = "admin"

def get_connected(max_attempts=3):

    attempts = 1

    while attempts <= max_attempts:
        try:
            connection = psycopg.connect(host=host,
                                        dbname=database, 
                                        user=user, 
                                        password=password)
            cursor = connection.cursor()
            print("Connection status: [\033[32mSUCCESS\033[0m]")
            return {
                    "status" : True,
                    "connection": connection,
                    "cursor": cursor,
                    "attempts": attempts
                }

        except Exception as error:
            print("Connection status: [\033[31mFAILED\033[0m]")
            print(f"Error: {error}")
            attempts += 1

    return {
            "status" : False,
            "connection": None,
            "cursor": None,
            "attempts": attempts
        }


        
