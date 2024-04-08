
from chalice import Chalice, Cron
from chalicelib.ui import  output_html
import boto3


app = Chalice(app_name="ncaaplayerssquads")

#Rate(15, unit=Rate.MINUTES)
@app.schedule(Cron('0/15', '*', '?', 4, "MON-TUE", 2024))
def periodic_task(event):
    html = output_html()

    s3 = boto3.resource("s3")

    s3.Object("brianhop.info", "page/ncaa/index.html").put(
        Body=bytes(html, 'utf-8'),
        ACL='public-read', 
        ContentType='text/html'
    )
