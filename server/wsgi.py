from eve import Eve
application = Eve(settings='/usr/local/cmdb/server/settings.py')

if __name__ == '__main__':
    application.run()