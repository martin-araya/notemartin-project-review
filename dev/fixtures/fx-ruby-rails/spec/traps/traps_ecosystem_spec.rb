require "rails_helper"

RSpec.describe "Trampas del ecosistema Rails" do
  # E01: convencion sobre configuracion
  it "expone resources :proyectos en routes.rb" do
    routes = File.read(Rails.root.join("config/routes.rb"))
    expect(routes).to include("resources :proyectos")
    expect(routes).to include("resources :facturas")
    expect(routes).to include("resources :recordatorios")
  end

  # E02: callbacks
  it "Proyecto declara before_save y after_destroy" do
    model = File.read(Rails.root.join("app/models/proyecto.rb"))
    expect(model).to include("before_save :normaliza_codigo")
    expect(model).to include("after_destroy :registrar_baja_en_log")
  end

  it "Factura declara after_commit" do
    model = File.read(Rails.root.join("app/models/factura.rb"))
    expect(model).to include("after_commit :encolar_generacion_pdf")
  end

  # E03: concerns con included do
  it "Trackable usa included do con before_create" do
    concern = File.read(Rails.root.join("app/models/concerns/trackable.rb"))
    expect(concern).to include("included do")
    expect(concern).to include("before_create :assign_tracking_id")
    expect(concern).to include("before_save :stamp_last_seen_at")
  end

  it "Proyecto incluye Trackable" do
    model = File.read(Rails.root.join("app/models/proyecto.rb"))
    expect(model).to include("include Trackable")
  end

  it "Factura incluye Trackable" do
    model = File.read(Rails.root.join("app/models/factura.rb"))
    expect(model).to include("include Trackable")
  end

  # E04: method_missing + define_method legacy
  it "config/initializers/legacy_constants.rb define Resolver con method_missing" do
    init = File.read(Rails.root.join("config/initializers/legacy_constants.rb"))
    expect(init).to include("module LegacyConstants")
    expect(init).to include("module Resolver")
    expect(init).to include("method_missing")
    expect(init).to include("define_method")
  end

  # E05: STI con columna type
  it "Recordatorio declara self.inheritance_column = :type" do
    model = File.read(Rails.root.join("app/models/recordatorio.rb"))
    expect(model).to include("self.inheritance_column = :type")
  end

  it "existen subclases STI Recordatorio::Email y Recordatorio::Sms" do
    expect(Object.const_defined?("Recordatorio::Email")).to be true
    expect(Object.const_defined?("Recordatorio::Sms")).to be true
    expect(Object.const_defined?("Recordatorio::Push")).to be true
  end

  it "la migracion incluye columna type en recordatorios" do
    mig = File.read(Rails.root.join("db/migrate/003_create_recordatorios.rb"))
    expect(mig).to include('t.string :type')
  end

  # E06: monkey patch en initializers
  it "config/initializers/patch_array.rb redefine Array#sum_safe" do
    init = File.read(Rails.root.join("config/initializers/patch_array.rb"))
    expect(init).to include("class Array")
    expect(init).to include("def sum_safe")
  end
end
