import boto3
import time
from datetime import datetime, timezone
# Configuration
REGION_NAME = 'your-region'  # e.g., 'us-west-2'
IDLE_THRESHOLD_MINUTES = 30  # e.g., 30 minutes
# Initialize Boto3 client
client = boto3.client('sagemaker', region_name=REGION_NAME)
def get_studio_apps():
   response = client.list_apps()
   return response['Apps']
def is_idle(app):
   app_name = app['AppName']
   response = client.describe_app(
       DomainId=app['DomainId'],
       UserProfileName=app['UserProfileName'],
       AppType=app['AppType'],
       AppName=app_name
   )
   # Assuming 'LastActivityTimestamp' is provided
   last_activity = response['LastActivityTimestamp']
   now = datetime.now(timezone.utc)
   idle_time = (now - last_activity).total_seconds() / 60
   return idle_time > IDLE_THRESHOLD_MINUTES
def stop_idle_apps():
   apps = get_studio_apps()
   for app in apps:
       if is_idle(app):
           print(f"Stopping idle app: {app['AppName']} (User: {app['UserProfileName']})")
           client.delete_app(
               DomainId=app['DomainId'],
               UserProfileName=app['UserProfileName'],
               AppType=app['AppType'],
               AppName=app['AppName']
           )
if __name__ == "__main__":
   while True:
       stop_idle_apps()
       time.sleep(60)  # Check every minute
