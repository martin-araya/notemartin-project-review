require "rails_helper"

RSpec.describe "Trampas del paquete por feature" do
  # P01: job_silent_retry
  it "EnviarRecordatorioJob declara retry_on StandardError con attempts" do
    job = File.read(Rails.root.join("app/jobs/enviar_recordatorio_job.rb"))
    expect(job).to include("retry_on StandardError")
    expect(job).to include("attempts: 3")
  end

  it "GenerarFacturaPdfJob declara retry_on con attempts" do
    job = File.read(Rails.root.join("app/jobs/generar_factura_pdf_job.rb"))
    expect(job).to include("retry_on StandardError")
  end

  # P02: stale_record_in_callback
  it "Recordatorio STI no valida que la clase type exista silenciosamente" do
    model = File.read(Rails.root.join("app/models/recordatorio.rb"))
    expect(model).to include("def asegurar_clase_sti")
  end

  it "STI acepta un type arbitrario sin error" do
    proyecto = create(:proyecto)
    r = Recordatorio.new(
      type: "NPRGT_FXRAILS_BADTYPE",
      sujeto: proyecto,
      mensaje: "Tipo invalido",
      fecha_envio: 1.day.from_now
    )
    expect(r).to be_valid
  end

  # P03: concern_included_twice
  it "Trackable esta incluido en dos modelos (Proyecto + Factura)" do
    proyecto = File.read(Rails.root.join("app/models/proyecto.rb"))
    factura = File.read(Rails.root.join("app/models/factura.rb"))
    expect(proyecto).to include("include Trackable")
    expect(factura).to include("include Trackable")
  end

  # P04: sti_invalid_type_silent (cubierto arriba)
  it "Recordatorio STI con clase inexistente no falla" do
    proyecto = create(:proyecto)
    expect {
      Recordatorio.create!(
        type: "NoExiste::Clase",
        sujeto: proyecto,
        mensaje: "x",
        fecha_envio: 1.day.from_now
      )
    }.not_to raise_error
  end

  # P05: route_convention_override
  it "config/routes.rb declara ruta dead /panel/legacy" do
    routes = File.read(Rails.root.join("config/routes.rb"))
    expect(routes).to include("panel/legacy")
  end

  # P06: initializer_load_order
  it "config/initializers/legacy_constants.rb existe y se carga antes de ActiveRecord" do
    init = File.read(Rails.root.join("config/initializers/legacy_constants.rb"))
    expect(init).to be_present
  end
end
