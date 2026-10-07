require "rails_helper"

RSpec.describe "Facturas feature", type: :feature do
  it "muestra el listado" do
    visit "/facturas"
    expect(page.status_code).to eq(200)
  end
end
