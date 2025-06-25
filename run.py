from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db
from controllers import cliente_controller, usuario_controller, caso_controller, audiencia_controller, pago_controller, seguimiento_controller, documento_controller
from models.usuario_model import Usuario
from models.caso_model import Caso
from models.cliente_model import Cliente
from models.audiencia_model import Audiencia
from auth.user_login import UserLogin  # clase adaptadora de login

app = Flask(__name__)
app.secret_key = "una_cadena_muy_secreta_y_unica_123456789"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///casos_juridicos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar base de datos
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    usuario = Usuario.get_by_id(int(user_id))
    return UserLogin(usuario) if usuario else None

# Registrar Blueprints
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(cliente_controller.cliente_bp)
app.register_blueprint(caso_controller.caso_bp)
app.register_blueprint(audiencia_controller.audiencia_bp)
app.register_blueprint(seguimiento_controller.seguimiento_bp)
app.register_blueprint(pago_controller.pago_bp)
app.register_blueprint(documento_controller.documento_bp)

# Navbar activo
@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return dict(is_active=is_active)

# Ruta raíz
@app.route("/")
def home():
    return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = Usuario.query.filter_by(usuario=username).first()

        if usuario and usuario.verify_password(password):
            if not usuario.activo:
                flash('Usuario inactivo', 'danger')
                return redirect(url_for('login'))

            login_user(UserLogin(usuario))
            rol = usuario.rol.nombre_rol

            if rol == 'Administrador':
                return redirect(url_for('admin_dashboard'))
            elif rol == 'Secretaria':
                return redirect(url_for('secretaria_dashboard'))
            elif rol == 'Abogado':
                return redirect(url_for('abogado_dashboard'))
            else:
                flash('Rol no reconocido', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('home'))

# Dashboards según rol
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html', user=current_user)

@app.route('/secretaria/dashboard')
@login_required
def secretaria_dashboard():
    return render_template('secretaria/dashboard.html', user=current_user)

@app.route('/abogado/dashboard')
@login_required
def abogado_dashboard():
    if current_user.rol != 'Abogado':
        flash("Acceso no autorizado", "danger")
        return render_template('abogado/dashboard.html', user=current_user)

    # Casos del abogado
    casos = Caso.query.filter_by(id_usuario=current_user.usuario.id_usuario).all()

    # Clientes asociados a esos casos
    clientes = Cliente.query.join(Caso).filter(Caso.id_usuario == current_user.usuario.id_usuario).distinct().all()

    # Audiencias de esos casos
    audiencias = Audiencia.query.join(Caso).filter(Caso.id_usuario == current_user.usuario.id_usuario).all()

    return render_template(
        'abogado/dashboard.html',
        user=current_user,
        casos=casos,
        clientes=clientes,
        audiencias=audiencias
    )


# Inicialización de datos si es primera vez
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        from models.rol_model import Rol
        from models.especialidad_model import Especialidad
        from models.estado_usuario_model import EstadoUsuario
        from models.estado_pago_model import EstadoPago
        from models.tipo_caso_model import TipoCaso
        from models.estado_caso_model import EstadoCaso
        from models.estado_audiencia_model import EstadoAudiencia

        # Insertar roles
        if not Rol.query.first():
            db.session.add_all([
                Rol(nombre_rol="Administrador"),
                Rol(nombre_rol="Abogado"),
                Rol(nombre_rol="Secretaria")
            ])
            db.session.commit()

        # Insertar especialidades
        if not Especialidad.query.first():
            esp_civil = Especialidad(nombre_especialidad="Derecho Civil")
            esp_penal = Especialidad(nombre_especialidad="Derecho Penal")
            esp_laboral = Especialidad(nombre_especialidad="Derecho Laboral")
            db.session.add_all([esp_civil, esp_penal, esp_laboral])
            db.session.commit()
        else:
            esp_civil = Especialidad.query.filter_by(nombre_especialidad="Derecho Civil").first()
            esp_penal = Especialidad.query.filter_by(nombre_especialidad="Derecho Penal").first()
            esp_laboral = Especialidad.query.filter_by(nombre_especialidad="Derecho Laboral").first()

        # Estado usuario
        if not EstadoUsuario.query.first():
            db.session.add_all([
                EstadoUsuario(nombre_estado="Activo"),
                EstadoUsuario(nombre_estado="Inactivo"),
                EstadoUsuario(nombre_estado="Suspendido")
            ])
            db.session.commit()

        # Estado de pago
        if not EstadoPago.query.first():
            db.session.add_all([
                EstadoPago(estado="Pendiente"),
                EstadoPago(estado="Pagado")
            ])
            db.session.commit()

        # Tipos de caso
        if not TipoCaso.query.first():
            db.session.add_all([
                TipoCaso(nombre_tipo="Demanda Civil", id_especialidad=esp_civil.id_especialidad),
                TipoCaso(nombre_tipo="Defensa Penal", id_especialidad=esp_penal.id_especialidad),
                TipoCaso(nombre_tipo="Demanda Laboral", id_especialidad=esp_laboral.id_especialidad)
            ])
            db.session.commit()

        # Estados del caso
        if not EstadoCaso.query.first():
            db.session.add_all([
                EstadoCaso(estado_caso="Abierto"),
                EstadoCaso(estado_caso="En Proceso"),
                EstadoCaso(estado_caso="Cerrado"),
                EstadoCaso(estado_caso="Archivado")
            ])
            db.session.commit()

        # Estados de audiencia
        if not EstadoAudiencia.query.first():
            db.session.add_all([
                EstadoAudiencia(nombre_estado_audiencia="Pendiente"),
                EstadoAudiencia(nombre_estado_audiencia="Realizada"),
                EstadoAudiencia(nombre_estado_audiencia="Suspendida")
            ])
            db.session.commit()

    app.run(debug=True)
