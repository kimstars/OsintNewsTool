from sets import app, db


def main():
   
    host = app.config.get('HOST')
    port = app.config.get('PORT')
    debug = app.config.get('DEBUG')
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()