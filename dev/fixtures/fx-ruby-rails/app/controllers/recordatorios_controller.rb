class RecordatoriosController < ApplicationController
  before_action :set_recordatorio, only: %i[show cancel]

  def index
    @recordatorios = Recordatorio.includes(:sujeto).order(fecha_envio: :asc).limit(50)
    respond_to do |format|
      format.html
      format.json { render json: @recordatorios.map { |r| recordatorio_json(r) } }
    end
  end

  def show
    respond_to do |format|
      format.html
      format.json { render json: recordatorio_json(@recordatorio) }
    end
  end

  def create
    @recordatorio = build_recordatorio(recordatorio_params)
    if @recordatorio.save
      respond_to do |format|
        format.html { redirect_to recordatorios_path, notice: "Recordatorio creado." }
        format.turbo_stream do
          render turbo_stream: turbo_stream.append("recordatorios", partial: "recordatorios/recordatorio", locals: { recordatorio: @recordatorio })
        end
        format.json { render json: recordatorio_json(@recordatorio), status: :created }
      end
    else
      respond_to do |format|
        format.html { render plain: @recordatorio.errors.full_messages.join(", "), status: :unprocessable_entity }
        format.json { render json: { errors: @recordatorio.errors.full_messages }, status: :unprocessable_entity }
      end
    end
  end

  def cancel
    @recordatorio.cancel!
    redirect_to recordatorios_path, notice: "Recordatorio cancelado."
  end

  private

  def set_recordatorio
    @recordatorio = Recordatorio.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    head :not_found
  end

  def recordatorio_params
    params.require(:recordatorio).permit(:mensaje, :fecha_envio, :sujeto_type, :sujeto_id, :type, :destinatario_email, :destinatario_telefono, :device_token)
  end

  def build_recordatorio(params)
    case params[:type]
    when "Recordatorio::Email"
      Recordatorio::Email.new(params.except(:type))
    when "Recordatorio::Sms"
      Recordatorio::Sms.new(params.except(:type))
    when "Recordatorio::Push"
      Recordatorio::Push.new(params.except(:type))
    else
      Recordatorio.new(params.except(:type))
    end
  end

  def recordatorio_json(r)
    {
      id: r.id,
      type: r.type,
      mensaje: r.mensaje,
      fecha_envio: r.fecha_envio,
      estado: r.estado,
      canal: r.respond_to?(:canal) ? r.canal : nil,
      cancelled: r.respond_to?(:cancelled?) ? r.cancelled? : false
    }
  end
end
