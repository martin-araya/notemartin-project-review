class ProyectosController < ApplicationController
  before_action :set_proyecto, only: %i[show edit update destroy]

  def index
    @proyectos = Proyecto.activos.limit(50)
    # P05: n_plus_one latente. El view itera `@proyectos` y muestra
    # `recordatorios_pendientes`; cada llamada dispara una query extra.
    respond_to do |format|
      format.html
      format.json { render json: @proyectos.map { |p| proyecto_json(p) } }
    end
  end

  def show
    respond_to do |format|
      format.html
      format.json { render json: proyecto_json(@proyecto) }
    end
  end

  def new
    @proyecto = Proyecto.new
  end

  def create
    @proyecto = Proyecto.new(proyecto_params)
    if @proyecto.save
      redirect_to @proyecto, notice: "Proyecto creado."
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit; end

  def update
    if @proyecto.update(proyecto_params)
      redirect_to @proyecto, notice: "Proyecto actualizado."
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @proyecto.destroy
    redirect_to proyectos_path, notice: "Proyecto eliminado."
  end

  private

  def set_proyecto
    @proyecto = Proyecto.find_by!(codigo: params[:id])
  rescue ActiveRecord::RecordNotFound
    head :not_found
  end

  def proyecto_params
    params.require(:proyecto).permit(:nombre, :codigo, :presupuesto, :estado)
  end

  def proyecto_json(p)
    {
      id: p.id,
      codigo: p.codigo,
      nombre: p.nombre,
      presupuesto: p.presupuesto,
      estado: p.estado,
      recordatorios_pendientes: p.recordatorios_pendientes,
      tracking_code: p.tracking_code
    }
  end
end
