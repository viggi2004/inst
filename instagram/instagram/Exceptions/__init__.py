class CsrfNotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self,
                           'CSRF token not found. Check your parse logic of home page')
