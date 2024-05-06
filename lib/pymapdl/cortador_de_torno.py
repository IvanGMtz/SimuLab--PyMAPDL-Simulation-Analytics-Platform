import os
import numpy as np
from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.examples.downloads import download_example_data

def analizar_cortador_de_torno(EXX, NU, Fuerza):
    # Directorio de trabajo actual
    path = os.getcwd()
    PI = np.pi
    mapdl = launch_mapdl(additional_switches="-smp")

    # Reiniciar la base de datos de MAPDL y configurar el entorno
    mapdl.clear()
    
    # Importar la geometría y definir propiedades del material y malla
    archivo_geometria = download_example_data("LatheCutter.anf", "geometry")
    mapdl.input(archivo_geometria)
    mapdl.finish()
    longitud_presion = mapdl.parameters["PRESS_LENGTH"]
    
    mapdl.units("Bin")
    mapdl.title("Cortador de Torno")
    
    mapdl.prep7()
    mapdl.mp("EX", 1, EXX)
    mapdl.mp("NUXY", 1, NU)
    mapdl.et(1, 285)
    mapdl.smrtsize(4)
    mapdl.aesize(14, 0.0025)
    mapdl.vmesh(1)

    mapdl.da(11, "symm")
    mapdl.da(16, "symm")
    mapdl.da(9, "symm")
    mapdl.da(10, "symm")

    # Crear un sistema de coordenadas local y configurar la carga
    mapdl.cskp(11, 0, 2, 1, 13)
    mapdl.csys(1)
    mapdl.view(1, -1, 1, 1)
    mapdl.psymb("CS", 1)
    
    # Definir y aplicar la carga de presión
    puntos = 10
    longitud_x = np.linspace(0, longitud_presion, puntos)
    presion = Fuerza * np.sin(PI * longitud_x / longitud_presion)
    presion = np.stack((longitud_x, presion), axis=-1)
    mapdl.load_table("MY_PRESS", presion, "X", csysid=11)
    
    mapdl.asel("S", "Area", "", 14)
    mapdl.nsla("S", 1)
    mapdl.sf("All", "Press", "%MY_PRESS%")
    mapdl.allsel()

    # Configurar y resolver el modelo
    mapdl.finish()
    mapdl.slashsolu()
    mapdl.nlgeom("On")
    mapdl.psf("PRES", "NORM", 3, 0, 1)
    mapdl.view(1, -1, 1, 1)
    ruta_imagen_carga = "static/images/Pressure_Load_plot.png"
    mapdl.eplot(vtk=False, savefig=ruta_imagen_carga)
    mapdl.solve()
    mapdl.finish()
    
    # Procesamiento y visualización de resultados
    mapdl.post1()
    mapdl.set("last")
    mapdl.allsel()

    argumentos_barra = dict(
        title_font_size=20,
        label_font_size=16,
        shadow=True,
        n_labels=9,
        italic=True,
        bold=True,
        fmt="%.1f",
        font_family="arial",
        title="Esfuerzo Principal 1 (psi)",
        color="black",
    )

    ruta_imagen_esfuerzo = "static/images/principal_stress_plot.png"
    mapdl.post_processing.plot_nodal_principal_stress("1", smooth_shading=False,
        edge_color="black",
        background="beige",
        show_edges=True,
        scalar_bar_args=argumentos_barra,
        n_colors=256,
        cmap="jet",
        savefig=ruta_imagen_esfuerzo
        )

    ruta_imagen_esfuerzo_xy = "static/images/XYprincipal_stress_plot.png"
    mapdl.post_processing.plot_nodal_principal_stress(
        "1",
        cpos="xy",
        edge_color="black",
        background="beige",
        show_edges=True,
        scalar_bar_args=argumentos_barra,
        n_colors=256,
        cmap="jet",
        savefig=ruta_imagen_esfuerzo_xy
    )

    mapdl.exit()
    return ruta_imagen_carga, ruta_imagen_esfuerzo, ruta_imagen_esfuerzo_xy

# Ejemplo de uso de la función
#print(analizar_cortador_de_torno(1.0e7, 0.27, 10000))
