import faust


class EmailView(faust.Record):
    email: str
    code: str


app = faust.App('job_portal', brocker='kafka://localhost:9092', autodiscover=True, origin='faust_app')
