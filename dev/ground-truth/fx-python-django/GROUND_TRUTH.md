# Ground truth de fx-python-django (F06p)

Proyecto **Django 5** con API REST via **Django REST Framework 3.15**,
tareas asincronas con **Celery 5.3** (modo EAGER en dev/tests),
configuracion dividida en **`base`/`dev`/`prod`** via
`DJANGO_SETTINGS_MODULE`, y suite de tests con **pytest-django 4.8**.
Plantada para que la skill tenga que rastrear las trampas clasicas
del ecosistema Python/Django.

## Features

1. **matriculas** (FEAT-001): crear, listar, obtener, actualizar,
   eliminar via DRF + signal post_save + Celery task EAGER. 7 R-NN.
2. **pagos** (FEAT-002): crear, marcar completado, listar via DRF +
   signal post_save vacio + handler dead. 7 R-NN.
3. **certificados** (FEAT-003): emitir, listar, obtener via DRF con
   OneToOne a Enrollment. 7 R-NN.
4. **acciones-de-admin** (FEAT-004): export_csv + mark_reviewed via
   Django admin shell, sin ruta publica. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. `signals_in_apps_ready`: `EnrollmentsConfig.ready()` conecta
   `@receiver(post_save, sender=Enrollment)` via `from . import signals`.
2. `drf_router_generated_routes`: `DefaultRouter().register(r'', ViewSet,
   basename='enrollment')` genera las rutas.
3. `custom_manager_queryset`: `EnrollmentQuerySet` con `.active()`,
   `.paid()`, `.by_user()` + `EnrollmentManager.from_queryset()`.
4. `settings_split_by_env`: `fxdjango/settings/{base,dev,prod}.py`
   activados por `DJANGO_SETTINGS_MODULE`.
5. `admin_action_no_public_route`: `export_csv` y `mark_reviewed` en
   `AuditLogAdmin` accesibles solo desde `/admin/`.
7. `template_tags_and_context_processors`: 3 template tags y 2
   context processors registrados en `TEMPLATES['OPTIONS']`.

## Trampas del paquete (CC-04)

1. `signals_sin_transaction_envelope`: el `@receiver` ejecuta la
   Celery task sin `transaction.on_commit`.
2. `queryset_metodo_sin_indice`: `PaymentQuerySet.completed()` /
   `pending()` / `for_enrollment()` sin indice en enrollment.
3. `admin_action_sin_permission_check`: `export_csv` no verifica
   `request.user.has_perm` extra.
4. `celery_eager_swallows_exceptions`: `CELERY_TASK_ALWAYS_EAGER=True`
   en dev/tests hace que las tasks ejecuten sincronamente.
5. `router_basename_payment`: `basename='payment'` en `payments/urls.py`
   determina `reverse('payment-list')`.
6. `settings_prod_no_secret_key_env`: `SECRET_KEY` default inseguro
   si no hay `FXDJ_SECRET_KEY`.

## Trampas superficiales (CC-05)

1. `dead_viewset`: `LegacyCertificateViewSet` existe pero no esta
   registrado en `urls.py`.
2. `dead_signal_handler`: `handler_pago_fallido` existe pero no
   tiene `@receiver`.
3. `dead_template_tag`: `format_certificate_id` existe pero no se usa
   en ninguna template.

## Archivos clave del fixture

- `manage.py`: `DJANGO_SETTINGS_MODULE=fxdjango.settings.dev` por defecto.
- `requirements.txt`: Django 5.0.6, djangorestframework 3.15.1,
  celery 5.3.6, pytest 8.2.0, pytest-django 4.8.0.
- `pytest.ini`: `DJANGO_SETTINGS_MODULE = fxdjango.settings.dev`.
- `fxdjango/__init__.py`: importa `celery_app` para autodiscovery.
- `fxdjango/settings/base.py`: INSTALLED_APPS (django.contrib.* +
  rest_framework + apps.enrollments + apps.payments + apps.certificates
  + apps.audit), TEMPLATES con context processors, REST_FRAMEWORK,
  CELERY_BROKER_URL=memory://, CELERY_TASK_ALWAYS_EAGER=False.
- `fxdjango/settings/dev.py`: `from .base import *` + `DEBUG=True` +
  DB `:memory:` + `CELERY_TASK_ALWAYS_EAGER=True` +
  `AllowAny`.
- `fxdjango/settings/prod.py`: `DEBUG=False` + `ALLOWED_HOSTS=['*']` +
  EAGER=False.
- `fxdjango/urls.py`: `path('admin/', admin.site.urls)` + 4
  `path('api/<x>/', include('apps.<x>.urls'))` + `path('admin/audit/')`.
- `fxdjango/celery.py`: `Celery('fxdjango', broker='memory://',
  backend='cache+memory://')` + `autodiscover_tasks()`.
- `apps/enrollments/`: 13 (apps.py con `ready()` importa signals,
  models.py con `EnrollmentManager` custom, managers.py con
  `EnrollmentQuerySet.active()`, signals.py con `@receiver(post_save)`
  que llama `procesar_inscripcion.delay()`, tasks.py con
  `@shared_task`, views.py con `EnrollmentViewSet`, urls.py con
  `DefaultRouter().register('', EnrollmentViewSet, basename='enrollment')`,
  admin.py, templatetags/enrollment_tags.py con
  `@register.simple_tag`, context_processors.py con `enrollment_counts`).
- `apps/payments/`: 9 (apps.py, models.py con `Index(['status'])`,
  managers.py con `PaymentQuerySet`, signals.py con `payment_post_save`
  + `handler_pago_fallido` dead, tasks.py con `emitir_recibo`,
  views.py con `PaymentViewSet`, urls.py con `basename='payment'`,
  admin.py, templatetags/payment_tags.py con `payment_status_badge`).
- `apps/certificates/`: 9 (apps.py, models.py con OneToOne,
  managers.py con `CertificateQuerySet`, signals.py, tasks.py con
  `generar_pdf`, views.py con `CertificateViewSet` + `LegacyCertificateViewSet`
  dead, urls.py, admin.py, templatetags/certificate_tags.py con
  `format_certificate_id` dead + `certificate_is_valid`,
  context_processors.py con `certificate_metadata`).
- `apps/audit/`: 6 (apps.py, models.py con `AuditLog`, signals.py,
  admin.py con `AuditLogAdmin` + 2 `@admin.action` `export_csv` y
  `mark_reviewed`, urls_admin.py con vista `export_audit_csv` no
  enlazada, migrations/0001_initial.py).
- `tests/`: 4 tests por feature + 6 ecosystem + 6 package + 3
  superficial = 30 tests pytest-django.

## Decisiones tecnicas (ver DECISIONS.md D-221..D-229)

- D-221: Python 3.11 + Django 5.0 + DRF 3.15 + Celery 5.3 +
  pytest-django 4.8 + SQLite.
- D-222: apps en ingles (enrollments, payments, certificates, audit)
  para CC-11; ground truth mantiene nombres en espanol.
- D-223: Celery en modo EAGER en dev/tests.
- D-224: Settings split en base/dev/prod.
- D-225: Prefijo `NPRGT-FXDJ-` para unique tokens.
- D-226: `Makefile` envuelve `pytest -q --ds=fxdjango.settings.dev`.
- D-227: Imagen Docker `python:3.11-slim` + `apt-get install make`.
- D-228: `requires: [linux, macos, windows]`.
- D-229: `fixtures_matrix.py` y `target_matrix.yml` extendidos para
  detectar Django/DRF/Celery/pytest-django.