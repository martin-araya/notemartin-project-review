class CreateProyectos < ActiveRecord::Migration[7.1]
  def change
    create_table :proyectos do |t|
      t.string :codigo, null: false
      t.string :nombre, null: false
      t.integer :presupuesto, default: 0
      t.string :estado, default: "activo"
      t.string :tracking_id
      t.datetime :last_seen_at
      t.timestamps
    end
    add_index :proyectos, :codigo, unique: true
    add_index :proyectos, :tracking_id
  end
end
