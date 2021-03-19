def application(environ,start_response):
    status = '200 OK'
    html = '<html>\n' \
           '<body>\n' \
           ' Hooray, mod_wsgi is working\n' \
           '</body>\n' \
           '</html>\n'
    response_header = [('Content-type','text/html')]
    start_response(status,response_header)
    return [html]
