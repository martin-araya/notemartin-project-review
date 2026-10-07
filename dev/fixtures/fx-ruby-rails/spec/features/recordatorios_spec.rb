require "rails_helper"

RSpec.describe "Recordatorios feature", type: :feature do
  it "muestra el formulario" do
    visit "/recordatorios"
    expect(page.status_code).to eq(200)
    expect(page).to have_content("Recordatorios")
  end
end
