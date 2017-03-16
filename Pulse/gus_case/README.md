# gus_case

Check python openssl version

    python -c "import ssl; print ssl.OPENSSL_VERSION"

If the openssl version is less than 1.0.1, then follow below steps.

#Mac
Installing new OpenSSl on python

     1) brew update
     2) brew install openssl
     3) brew install python --with-brewed-openssl

This will install a python on your desktop at /usr/local/opt/python/bin/python2.7

Create virtual env with new version of python

    1) virtualenv -p /usr/local/opt/python/bin/python2.7 venv
    2) source venv/bin/activate
    3) pip install requests

Run gus case creation

    1)git clone ssh://git@git.soma.salesforce.com/sboddepalli/gus_case.git

Create a test.py and run

    from gus_case.create_case import create_case
    print create_case()

Create_case method will create a gus incident with these default values - create_case(category="capacity", status="New", subject="Dummy Anomaly", desc="Dummy Anomaly", subcategory=None, dc=None, priority="sev4")
