import logging.debug
from base import Auth
from base import Gus
from common import Common 
import sys
try:
    import pyczar
except:
    print('no %s installed' % 'pyczar')
    sys.exit(1)

savedsession = config.get('Session', 'savedsession')

def validLogin(session):
    gusObj = Gus()
    object = 'Case'
    query = "select Id from " + object +" limit 1"
    logging.debug(query)
    try:
        case_query = gusObj.run_query(query,session)
        if case_query['totalSize'] == 1 and case_query['done'] == True:
            return True
        else:
            return False
    except Exception as e:
        print('%s' % e)
        return False
    
def saveSession(savedsession,session):
    with open(savedsession, 'w') as f:
        json.dump(session, f)
        
def getSession(savedsession):
    with open(savedsession, 'r') as f:
        session = json.load(f)
        return session  

def creds():
    session = ''
    valid_login = ''
    if os.path.isfile(savedsession):
        session = getSession(savedsession)
        logging.debug(session)
    try:
        valid_login = validLogin(session)
        logging.debug(valid_login)
    except Exception as e:
        print('error %s' % e)
    if valid_login != True:
        try:
            client_id,client_secret,username,passwd = getCreds()
            logging.debug('%s, %s, %s' % (client_id,client_secret,username))
        except Exception as e:
            print('Problem getting username, client_id or client_secret: %s' % e)
            sys.exit()
        authObj = Auth(username,passwd,client_id,client_secret)
        #save latest session info
        try:
            session = authObj.login()
            logging.debug(session)
            saveSession(savedsession,session)
        except Exception as e:
            print('Failed to store session : %s' % e)
    return session
            
def getCreds():
    if os.path.isfile('vaultcreds.config'):
        pc = pyczar.Pyczar()
        keyDir = config.get('VAULT', 'keydir')
        valut = config.get('VAULT', 'vault')
        server = config.get('VAULT', 'servera')
        port = config.get('VAULT', 'port') 
        new_server = pc.change_server(server,port)
        client_id = pc.get_secret(valut, 'client_id', keyDir)
        client_secret = pc.get_secret(valut, 'client_secret', keyDir)
        username = pc.get_secret(valut, 'username', keyDir)
        passwd = pc.get_secret(valut, 'passwd', keyDir)
        return client_id,client_secret,username,passwd
    elif not os.path.isfile('vaultcreds.config') and os.path.isfile('creds.config'):
        try:
            passwd = config.get('GUS', 'guspassword')
        except ConfigParser.NoOptionError,e:
            passwd = getpass.getpass("Please enter your GUS password: ")
        try:
            username = config.get('GUS', 'username')
            client_id = config.get('GUS', 'client_id')
            client_secret = config.get('GUS', 'client_secret')
        except:
            print('Problem getting username, client_id or client_secret')
            sys.exit()
        return client_id,client_secret,username,passwd
    else:
        print('Problem getting username, client_id or client_secret')
        sys.exit()