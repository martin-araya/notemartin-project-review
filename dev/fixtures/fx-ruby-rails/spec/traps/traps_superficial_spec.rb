require "rails_helper"

RSpec.describe "Trampas superficiales" do
  it "S01: LegacyTextFormatter existe y nadie lo invoca en la app" do
    service = File.read(Rails.root.join("app/services/legacy_text_formatter.rb"))
    expect(service).to include("class LegacyTextFormatter")
    expect(service).to include("def self.legacy_format")

    # Verificamos que no hay llamadas a legacy_format en el resto de app/.
    app_root = Rails.root.join("app")
    consumers = Dir[app_root.join("**/*.rb")].reject { |f| f.include?("legacy_text_formatter.rb") }
    consumers = consumers.select { |f| File.read(f, encoding: "utf-8", errors: "replace").include?("legacy_format") }
    expect(consumers).to be_empty, "LegacyTextFormatter.legacy_format no deberia tener consumidores pero aparece en: #{consumers.inspect}"
  end

  it "S02: app/controllers/concerns/ esta vacio (solo .keep)" do
    concerns = Rails.root.join("app/controllers/concerns")
    files = Dir.children(concerns).reject { |f| f == ".keep" }
    expect(files).to be_empty
  end

  it "S03: existe partial recordatorios/_unused_partial.html.erb" do
    expect(Rails.root.join("app/views/recordatorios/_unused_partial.html.erb")).to be_file
  end
end
