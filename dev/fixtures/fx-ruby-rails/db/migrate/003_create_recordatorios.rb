class CreateRecordatorios < ActiveRecord::Migration[7.1]
  def change
    create_table :recordatorios do |t|
      t.string :type, null: false, default: "Recordatorio"
      t.references :sujeto, polymorphic: true, null: false
      t.string :mensaje, null: false
      t.datetime :fecha_envio, null: false
      t.string :estado, default: "pendiente"
      t.datetime :enviado_at
      t.datetime :cancelled_at
      t.string :destinatario_email
      t.string :destinatario_telefono
      t.string :device_token
      t.timestamps
    end
    add_index :recordatorios, [:sujeto_type, :sujeto_id]
    add_index :recordatorios, :type
  end
end
