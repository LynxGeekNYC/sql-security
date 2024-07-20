import smtplib
from email.mime.text import MIMEText
import psycopg2
import cx_Oracle
import mysql.connector
import time

# Database connection details
db_configs = {
    'postgresql': {
        'host': 'your_postgresql_host',
        'dbname': 'your_postgresql_dbname',
        'user': 'your_postgresql_user',
        'password': 'your_postgresql_password',
        'log_file': '/path/to/postgresql/log/file'
    },
    'oracle': {
        'dsn': 'your_oracle_dsn',
        'user': 'your_oracle_user',
        'password': 'your_oracle_password',
        'log_file': '/path/to/oracle/log/file'
    },
    'mysql': {
        'host': 'your_mysql_host',
        'database': 'your_mysql_database',
        'user': 'your_mysql_user',
        'password': 'your_mysql_password',
        'log_file': '/path/to/mysql/log/file'
    }
}

# Keywords indicative of SQL dump activities
dump_keywords = ['pg_dump', 'exp', 'mysqldump']

# Email alert configuration
smtp_server = 'your_smtp_server'
smtp_port = 587
smtp_user = 'your_email@example.com'
smtp_password = 'your_email_password'
alert_email = 'alert_recipient@example.com'

def send_alert(database, log_line):
    msg = MIMEText(f'SQL dump detected in {database} log:\n\n{log_line}')
    msg['Subject'] = f'SQL Dump Alert for {database}'
    msg['From'] = smtp_user
    msg['To'] = alert_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, alert_email, msg.as_string())
        print(f'Alert sent for {database}')

def monitor_logs():
    log_positions = {db: 0 for db in db_configs}

    while True:
        for db, config in db_configs.items():
            try:
                with open(config['log_file'], 'r') as log_file:
                    log_file.seek(log_positions[db])
                    for line in log_file:
                        if any(keyword in line for keyword in dump_keywords):
                            send_alert(db, line)
                    log_positions[db] = log_file.tell()
            except Exception as e:
                print(f'Error monitoring {db} logs: {e}')

        time.sleep(60)  # Check logs every 60 seconds

if __name__ == '__main__':
    monitor_logs()
