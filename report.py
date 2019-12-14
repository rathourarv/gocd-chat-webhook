import requests
import os
import logging
import untangle

env_vars = os.environ
if 'GoCD_URL' not in env_vars:
    raise Exception("GoCD url not found")
url = env_vars['GoCD_URL']

logging.info("getting pipelines xml file")
cctray_xml_template = "{}/go/cctray.xml"
cctray_xml_url = str.format(cctray_xml_template, url)
res = requests.get(cctray_xml_url)
projects = untangle.parse(res.text)
pipelines = projects.Projects.Project


def is_failed_pipeline(pl):
    return pl['lastBuildStatus'] == "Failure"


url_template = "{}/go/api/pipelines/{}/instance/{}"
failedPipelines = filter(is_failed_pipeline, pipelines)
for pipeline in failedPipelines:
    pipeline_name = pipeline['name'].split(" ::")[0]
    pipeline_number = pipeline['lastBuildLabel']
    pipeline_json_url = str.format(url_template, url, pipeline_name, pipeline_number)
    res = requests.get(pipeline_json_url)
    print(res.json())
