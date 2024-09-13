import os

from flask import Flask


def create_app(test_config=None): #fabrica de apps
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) # indica a la aplicación que los archivos de configuración 
                                                         # son relativos a la carpeta instance. 
    app.config.from_mapping( # establece alguna configuración por defecto que la aplicación utilizará
        SECRET_KEY='dev',    # es utilizada por Flask y las extensiones para mantener los datos seguros.
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), # crea la ruta para la base de datos  
        # app.instance_path que es la ruta que Flask ha elegido para la carpeta de la instancia. 
    )

    if test_config is None: #
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True) #  anula la configuración por defecto con valores tomados del archivo config.py
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path) # crea la carpeta instance
    except OSError:
        pass

    # crea una ruta simple para que puedas ver la aplicación funcionando
    @app.route('/hello') 
    def hello():
        return '<title>Hello, World!</title> <p>Hello, word</p> '
    
    # existing code omitted

    from . import db
    db.init_app(app) # inicializar base de datos
    
    from . import auth
    app.register_blueprint(auth.bp) # registra el objeto blue sprint de auth

    from . import blog
    app.register_blueprint(blog.bp)# registra el objeto blue sprint del blog
    app.add_url_rule('/', endpoint='index') # establee el origen de la página y el endpoint
    
    
    
    return app

    