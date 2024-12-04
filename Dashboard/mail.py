import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

admin_email = "alokamvarun@gmail.com"
admin_name = "Varun Alokam"

def send_alert_email(non_compliant_count, total_personnel):
    """
    Sends an email alert to the admin if non-compliance exceeds 50% of personnel count.
    """
    non_compliance_percentage = (non_compliant_count / total_personnel) * 100
    
    if non_compliance_percentage > 50:
        subject = "Safety Non-Compliance Alert"
        body = (f"Dear {admin_name},\n\n"
                f"Alert: More than 50% of the personnel on site are not compliant.\n"
                f"Total Personnel Detected: {total_personnel}\n"
                f"Non-Compliant Personnel: {non_compliant_count}\n"
                f"Non-Compliance Percentage: {non_compliance_percentage:.2f}%\n\n"
                f"Please take immediate action to ensure safety compliance.\n\n"
                f"Regards,\nSafety Monitoring System")
        
        msg = MIMEMultipart()
        msg['From'] = "chandramouli.misc@gmail.com" 
        msg['To'] = admin_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587) 
            server.starttls()
            server.login("constructionanalytics569@gmail.com", "jcnp vtrv dbhn jsxc")
            server.sendmail("constructionanalytics569@gmail.com",admin_email,msg.as_string())
            server.quit()
            print("Alert email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")


detected_personnel = 100  
non_compliant = 60  

send_alert_email(non_compliant, detected_personnel)
