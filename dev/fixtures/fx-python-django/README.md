# Fixture F06p — fx-python-django

Proyecto **Django 5** con API REST via **Django REST Framework 3.15**,
tareas asincronas con **Celery 5.3** (modo EAGER en tests),
configuracion dividida en **`base`/`dev`/`prod`** via
`DJANGO_SETTINGS_MODULE`, y suite de tests con **pytest-django 4.8**.
Plantada para que la skill tenga que rastrear las trampas
clasicas del ecosistema Python/Django:

## Stack

- **Lenguaje:** Python 3.11.
- **Framework web:** Django 5.0.6 + Django REST Framework 3.15.1.
- **Async:** Celery 5.3.6 (`EAGER` en dev y tests).
- **DB:** SQLite (`:memory:` en dev/tests; file-based en prod).
- **Tests:** pytest 8.2.0 + pytest-django 4.8.0.

## Como se ejecutan los tests

```bash
make test           # pytest -q --ds=fxdjango.settings.dev
make build          # python manage.py migrate
make history        # regenera la historia git (8 commits)
```

En contenedor (con Python 3.11 + make):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-python-django --container
```

## Estructura

- `manage.py`: `DJANGO_SETTINGS_MODULE=fxdjango.settings.dev` por defecto.
- `fxdjango/settings/{base,dev,prod}.py`: configuracion por entorno.
- `fxdjango/urls.py`: `include()` anidados + admin.
- `fxdjango/celery.py`: Celery app con `memory://` broker.
- `apps/enrollments/`: modelo `Enrollment`, `EnrollmentItem`,
  `EnrollmentQuerySet` (custom Manager), `post_save` signal,
  `EnrollmentViewSet` (DRF), `@admin.display`,
  `@shared_task procesar_inscripcion`, template tag
  `enrollment_status_label`, context processor
  `enrollment_counts`.
- `apps/payments/`: modelo `Payment`, `PaymentManager`,
  `payment_paid` signal, `PaymentViewSet`, template tag.
- `apps/certificates/`: modelo `Certificate`,
  `CertificateQuerySet`, `CertificateViewSet`, legacy dead viewset,
  context processor.
- `apps/audit/`: modelo `AuditLog`, `@admin.action` con
  `export_csv` y `mark_reviewed` (sin ruta publica).
- `tests/`: 4 tests por feature + 15 tests de trampas.

## Features

1. **matriculas** (FEAT-001): crear, listar, obtener.
   7 R-NN.
2. **pagos** (FEAT-002): crear, marcar como completado, listar.
   7 R-NN.
3. **certificados** (FEAT-003): emitir, listar, descargar.
   7 R-NN.
4. **acciones-de-admin** (FEAT-004): export_csv, mark_reviewed,
   ejecutar via shell de admin. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): signals en apps.py:ready, routers
  DRF, custom Manager+QuerySet, settings divididos, admin actions
  sin ruta publica, template tags y context processors.
- 6 del paquete (CC-04): signals sin transaccion, queryset sin
  indice, admin action sin permission check, Celery EAGER
  enmascara excepciones, router basename mismatch, SECRET_KEY
  no definido en prod.
- 3 superficiales (CC-05): legacy viewset no registrado, signal
  handler desconectado, template tag no usado.