ActiveRecord::Schema[7.0].define(version: 3) do
  create_table "proyectos", force: :cascade do |t|
    t.string "codigo", null: false
    t.string "nombre", null: false
    t.integer "presupuesto", default: 0
    t.string "estado", default: "activo"
    t.string "tracking_id"
    t.datetime "last_seen_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["codigo"], name: "index_proyectos_on_codigo", unique: true
    t.index ["tracking_id"], name: "index_proyectos_on_tracking_id"
  end

  create_table "facturas", force: :cascade do |t|
    t.integer "proyecto_id", null: false
    t.integer "monto_cents", default: 0, null: false
    t.integer "tarifa_iva", default: 21, null: false
    t.string "estado", default: "borrador"
    t.string "tracking_id"
    t.datetime "last_seen_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["proyecto_id"], name: "index_facturas_on_proyecto_id"
    t.index ["tracking_id"], name: "index_facturas_on_tracking_id"
  end

  create_table "recordatorios", force: :cascade do |t|
    t.string "type", default: "Recordatorio", null: false
    t.string "sujeto_type", null: false
    t.bigint "sujeto_id", null: false
    t.string "mensaje", null: false
    t.datetime "fecha_envio", null: false
    t.string "estado", default: "pendiente"
    t.datetime "enviado_at"
    t.datetime "cancelled_at"
    t.string "destinatario_email"
    t.string "destinatario_telefono"
    t.string "device_token"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["sujeto_type", "sujeto_id"], name: "index_recordatorios_on_sujeto"
    t.index ["type"], name: "index_recordatorios_on_type"
  end
end
