require "rails_helper"

RSpec.describe "Proyectos feature", type: :feature do
  it "lista proyectos" do
    create(:proyecto, codigo: "FX-FEAT-1", nombre: "Feature 1")
    visit "/proyectos"
    expect(page.status_code).to eq(200)
    expect(page).to have_content("FX-FEAT-1")
  end
end
