# registra os blueprints

from src.route.endpoint.ocorrencia import ocorrencia_bp

def registrar_rotas(app):
    app.register_blueprint(ocorrencia_bp)