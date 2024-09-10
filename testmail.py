import smtplib,os
import requests
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def get_nist_vuln():

    # Base URL for the NVD API
    base_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

    # Example CPE names for your products (Replace with your actual CPEs)
    cpe_list = [
        "cpe:2.3:o:microsoft:windows_10:-:*:*:*:*:*:*:*",
        "cpe:2.3:a:adobe:acrobat_reader_dc:-:*:*:*:*:*:*:*"
    ]
    # Construct the CPE filter for the API
    cpe_filter = '&'.join([f'cpeName={cpe}' for cpe in cpe_list])

    # Construct the full API URL
    full_url = f'{base_url}?{cpe_filter}&resultsPerPage=1&startIndex=0'

    # Headers including API key if you have one
    #headers = {
    #    'apiKey': api_key
    #}

    # Send the request to the NVD API
    #response = requests.get(full_url, headers=headers)
    response = requests.get(full_url)

    # Parse the response
    if response.status_code == 200:
        cve_data = response.json()
        print(json.dumps(cve_data, indent=4))
    else:
        print(f"Error: {response.status_code}")
        return(-1)
    for vuln in cve_data['vulnerabilities']:
        print(vuln)
        
    

def send_email(subject, body, to_email, from_email, from_password, smtp_server, smtp_port):
    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body to the MIME message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection

        # Log in to the server
        server.login(from_email, from_password)

        # Send the email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        
        # Close the server connection
        server.quit()
        
        print("Email sent successfully!")
    
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

# Example usage
if __name__ == "__main__":
    for i in range(0,10):
        subject = "Test Email"
        body = "This is a test email sent from Python!"+str(i)
        to_email = os.getenv('destination_mail')
        from_email = os.getenv('source_mail')
        from_password = os.getenv('dest_passwd') 
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
#
        send_email(subject, body, to_email, from_email, from_password, smtp_server, smtp_port)
    get_nist_vuln()