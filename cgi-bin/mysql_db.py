#!/usr/bin/python3



import cgi
import cgitb
import mysql.connector

cgitb.enable()

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'your_db_user',
    'password': 'your_db_password',
    'database': 'your_db_name'
}

# Function to fetch data from the database
def fetch_data():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)

        # Fetch data from the database
        cursor = connection.cursor()
        query = "SELECT * FROM your_table;"
        cursor.execute(query)
        data = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return data

    except mysql.connector.Error as err:
        # Handle database connection errors
        return f"Database Error: {err}"

# Main function to handle the HTTP request and generate the HTML response
def main():
    print("Content-type: text/html\n")

    # Fetch data from the database
    data = fetch_data()

    # Generate the HTML response
    print("<html>")
    print("<head><title>Sample CGI Backend</title></head>")
    print("<body>")
    print("<h1>Database Data</h1>")
    print("<ul>")
    for row in data:
        print(f"<li>{row}</li>")
    print("</ul>")
    print("</body>")
    print("</html>")

if __name__ == '__main__':
    main()

