from base import Auth
from base import Gus
from sys import exit
import ConfigParser
import os

def exit_message(msg):
    exit(1)

#configdir = os.environ['HOME'] + "/.cptops/config"
configdir = "./"
config = ConfigParser.ConfigParser()
try:
    config.readfp(open(configdir + 'creds.config'))
except IOError:
    exit_message("No creds.config file found in %s" %configdir)

def getCaseNum(caseId,session):
    gusObj = Gus()
    case_details = gusObj.get_case_details(caseId,session)
    return case_details

def create_incident(cat, subcat, subject, desc, dc, status, priority, session):
    gusObj = Gus()
    recordType = 'Incident'
    incidentDict = { 'Category': cat,
                                     'SubCategory': subcat,
                                     'Subject': subject,
                                     'Description': desc,
                                     'DC': dc,
                                     'Status': status,
                                     'Priority': priority,
                                    }
    caseId = gusObj.create_incident_case(recordType, incidentDict, session)
    return caseId

def create_case(category="capacity", status="New", subject="Dummy Anomaly", desc="Dummy Anomaly", subcategory=None, dc=None, priority="sev4"):

    try:
        username = config.get('GUS', 'username')
        pa5s = config.get('GUS', 'pa5sword')
        client_id = config.get('GUS', 'client_id')
        client_secret = config.get('GUS', 'client_secret')
    except:
        exit_message('Problem getting username, pa5sword, client_id or client_secret')

    authObj = Auth(username,pa5s,client_id,client_secret)
    session = authObj.login()

    caseId = create_incident(category, subcategory, subject, desc, dc, status, priority, session)
    return getCaseNum(caseId, session)['CaseNumber'], "https://gus.my.salesforce.com/%s" %caseId
