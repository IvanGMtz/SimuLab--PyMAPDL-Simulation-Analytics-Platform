import os
import tempfile
from ansys.mapdl.core import launch_mapdl
from ansys.dpf import core as dpf
import numpy as np
from ansys.mapdl import core as pymapdl
import matplotlib.pyplot as plt

def analizar_viga_doble_voladizo(longitud, precorte, ancho, altura, desplazamiento):
    mapdl = pymapdl.launch_mapdl()
   
    # Una pequeña cantidad definida para evitar errores de redondeo al seleccionar entidades geométricas
    eps = 1e-1

    # Configurar el modelo
    mapdl.prep7()
    mapdl.units("mpa")

    # Definir elementos y tamaños para simulación completamente tridimensional
    mapdl.et(1, 185)
    mapdl.et(2, 170)
    mapdl.et(3, 174)
    mapdl.esize(10.0)

    # Propiedades del material para las placas compuestas
    mapdl.mp("ex", 1, 61340)
    mapdl.mp("dens", 1, 1.42e-09)
    mapdl.mp("nuxy", 1, 0.1)

    # Ley cohesiva bilineal para elementos de contacto
    mapdl.mp("mu", 2, 0)
    mapdl.tb("czm", 2, 1, "", "bili")
    mapdl.tbtemp(25.0)
    mapdl.tbdata(1, 50.0, 0.5, 50, 0.5, 0.01, 2)

    # Creación y malla de la geometría
    vnum0 = mapdl.block(0.0, longitud + precorte, 0.0, ancho, 0.0, altura)
    vnum1 = mapdl.block(0.0, longitud + precorte, 0.0, ancho, altura, 2 * altura)
    mapdl.mat(1)
    mapdl.type(1)
    mapdl.vmesh(vnum0)
    mapdl.vmesh(vnum1)
    mapdl.eplot()

    # Generación de elementos cohesivos entre superficies de contacto
    mapdl.allsel()
    mapdl.asel("s", "loc", "z", 1.7)
    areas = mapdl.geometry.anum
    mapdl.geometry.area_select(areas[0], "r")
    mapdl.nsla("r", 1)
    mapdl.nsel("r", "loc", "x", precorte, longitud + precorte + eps)
    mapdl.components["cm_1"] = "node"

    mapdl.allsel()
    mapdl.asel("s", "loc", "z", 1.7)
    areas = mapdl.geometry.anum
    mapdl.geometry.area_select(areas[1], "r")
    mapdl.nsla("r", 1)
    mapdl.nsel("r", "loc", "x", precorte, longitud + precorte + eps)
    mapdl.components["cm_2"] = "node"

    # Configuración de opciones reales y de elementos
    mapdl.allsel()
    mapdl.components["_elemcm"] = "elem"
    mapdl.mat(2)
    mapdl.r(3, "", "", 1.0, 0.1, 0, "")
    mapdl.rmore("", "", 1.0e20, 0.0, 1.0, "")
    mapdl.rmore(0.0, 0.0, 1.0, "", 1.0, 0.5)
    mapdl.rmore(0.0, 1.0, 1.0, 0.0, "", 1.0)
    mapdl.rmore("", "", "", "", "", 1.0)
    mapdl.keyopt(3, 4, 0)
    mapdl.keyopt(3, 5, 0)
    mapdl.keyopt(3, 7, 0)
    mapdl.keyopt(3, 8, 0)
    mapdl.keyopt(3, 9, 0)
    mapdl.keyopt(3, 10, 0)
    mapdl.keyopt(3, 11, 0)
    mapdl.keyopt(3, 12, 3)
    mapdl.keyopt(3, 14, 0)
    mapdl.keyopt(3, 18, 0)
    mapdl.keyopt(3, 2, 0)
    mapdl.keyopt(2, 5, 0)

    # Generate TARGE170 elements on top of cm_1
    mapdl.nsel("s", "", "", "cm_1")
    mapdl.components["_target"] = "node"
    mapdl.type(2)
    mapdl.esln("s", 0)
    mapdl.esurf()

    # Generate CONTA174 elements on top of cm_2
    mapdl.cmsel("s", "_elemcm")
    mapdl.nsel("s", "", "", "cm_2")
    mapdl.components["_contact"] = "node"
    mapdl.type(3)
    mapdl.esln("s", 0)
    mapdl.esurf()

    # Condiciones de contorno y resolución del modelo
    mapdl.allsel()
    mapdl.nsel(type_="s", item="loc", comp="x", vmin=0.0, vmax=0.0)
    mapdl.nsel(type_="r", item="loc", comp="z", vmin=2 * altura, vmax=2 * altura)
    mapdl.d(node="all", lab="uz", value=desplazamiento)
    mapdl.components["top_nod"] = "node"

    mapdl.allsel()
    mapdl.nsel(type_="s", item="loc", comp="x", vmin=0.0, vmax=0.0)
    mapdl.nsel(type_="r", item="loc", comp="z", vmin=0.0, vmax=0.0)
    mapdl.d(node="all", lab="uz", value=-10)
    mapdl.components["bot_nod"] = "node"

    # Fijar el modelo y resolver
    mapdl.allsel()
    mapdl.nsel(
        type_="s",
        item="loc",
        comp="x",
        vmin=longitud + precorte,
        vmax=longitud + precorte,
    )
    mapdl.d(node="all", lab="ux", value=0.0)
    mapdl.d(node="all", lab="uy", value=0.0)
    mapdl.d(node="all", lab="uz", value=0.0)

    mapdl.eplot(plot_bc=True, bc_glyph_size=3, title="")
    mapdl.run("/SOLU")
    mapdl.antype("static")
    mapdl.nlgeom("on")
    mapdl.autots(key="on")
    mapdl.nsubst(nsbstp=100, nsbmx=100, nsbmn=100)
    mapdl.kbc(key=0)
    mapdl.outres("all", "all")
    mapdl.solve()

    # Postprocesamiento
    mapdl.post1()
    mapdl.set(1, 100)
    mapdl.allsel()
    mapdl.esel("s", "ename", "", 174)
    mapdl.post_processing.plot_element_values("nmisc", 70, scalar_bar_args={"title": "Daño Cohesivo"})

    mapdl.allsel()
    mapdl.esel("s", "ename", "", 174)
    mapdl.etable("damage", "nmisc", 70)
    damage_df = mapdl.pretab("damage").to_dataframe()

    directorio_temporal = tempfile.gettempdir()
    ruta_resultados = mapdl.download_result(directorio_temporal)
    dpf.core.make_tmp_dir_server(dpf.SERVER)

    if dpf.SERVER.local_server:
        fuente_path = ruta_resultados
    else:
        fuente_path = dpf.upload_file_in_tmp_folder(ruta_resultados)

    modelo = dpf.Model(fuente_path)
    seleccion_malla = modelo.metadata.named_selection("BOT_NOD")
    mapdl.exit()

    f_totales = []
    d_totales = []
    for i in range(100):
        evaluacion_fuerza = modelo.results.element_nodal_forces(time_scoping=i, mesh_scoping=seleccion_malla).eval()
        fuerza = evaluacion_fuerza[0].data
        f_totales.append(np.sum(fuerza[:, 2]))
        d = abs(modelo.results.displacement(time_scoping=i, mesh_scoping=seleccion_malla).eval()[0].data[0])
        d_totales.append(d[2])

    d_totales[0] = 0
    f_totales[0] = 0

    fig, ax = plt.subplots()
    plt.plot(d_totales, f_totales, "b")
    plt.title('Fuerza vs Desplazamiento')
    plt.xlabel('Desplazamiento [mm]')
    plt.ylabel('Fuerza [N]')
    ruta_imagen_fuerza = os.path.join('static/images', 'ForcevsDisplacement.png')
    plt.savefig(ruta_imagen_fuerza)
    plt.close(fig)

    return ruta_imagen_fuerza

# Uso de la función para análisis de una viga de doble voladizo
# print(analizar_viga_doble_voladizo(75.0, 10.0, 25.0, 1.7, 10.0))
