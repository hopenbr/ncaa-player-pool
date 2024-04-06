
from chalice import Chalice
from chalicelib.ui import get_scores


app = Chalice(app_name="ncaaplayerssquads")

@app.schedule(Rate(5, unit=Rate.MINUTES))
def periodic_task(event):
    return {"hello": "world"}