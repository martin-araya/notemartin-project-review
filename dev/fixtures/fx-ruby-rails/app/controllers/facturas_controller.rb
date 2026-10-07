class FacturasController < ApplicationController
  before_action :set_factura, only: %i[show update destroy]

  def index
    @facturas = Factura.includes(:proyecto).order(created_at: :desc).limit(50)
    respond_to do |format|
      format.html
      format.json { render json: @facturas.map { |f| factura_json(f) } }
    end
  end

  def show
    respond_to do |format|
      format.html
      format.json { render json: factura_json(@factura) }
    end
  end

  def create
    @factura = Factura.new(factura_params)
    if @factura.save
      render json: factura_json(@factura), status: :created
    else
      render json: { errors: @factura.errors.full_messages }, status: :unprocessable_entity
    end
  end

  def update
    if @factura.update(factura_params)
      render json: factura_json(@factura), status: :ok
    else
      render json: { errors: @factura.errors.full_messages }, status: :unprocessable_entity
    end
  end

  def destroy
    @factura.destroy
    head :no_content
  end

  private

  def set_factura
    @factura = Factura.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    head :not_found
  end

  def factura_params
    params.require(:factura).permit(:proyecto_id, :monto_cents, :tarifa_iva, :estado)
  end

  def factura_json(f)
    {
      id: f.id,
      proyecto_id: f.proyecto_id,
      monto_cents: f.monto_cents,
      monto_euros: f.monto_euros,
      tarifa_iva: f.tarifa_iva,
      total_con_iva: f.total_con_iva,
      estado: f.estado,
      tracking_code: f.tracking_code
    }
  end
end
