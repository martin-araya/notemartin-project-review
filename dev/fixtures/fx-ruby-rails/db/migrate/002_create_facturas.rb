class CreateFacturas < ActiveRecord::Migration[7.1]
  def change
    create_table :facturas do |t|
      t.references :proyecto, null: false, foreign_key: true
      t.integer :monto_cents, null: false, default: 0
      t.integer :tarifa_iva, null: false, default: 21
      t.string :estado, default: "borrador"
      t.string :tracking_id
      t.datetime :last_seen_at
      t.timestamps
    end
    add_index :facturas, :tracking_id
  end
end
