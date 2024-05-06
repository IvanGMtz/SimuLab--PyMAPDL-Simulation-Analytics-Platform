from ansys.mapdl.core import launch_mapdl

def analizar_soporte(box1, box2, radio_perno, tamaño_elemento, carga_presion):
    nombre_trabajo = "analisis_soporte"
    mapdl = launch_mapdl(jobname=nombre_trabajo)

    mapdl.clear()
    mapdl.prep7()
    
    # Creación de la geometría
    mapdl.rectng(*box1)
    mapdl.rectng(*box2)
    
    # Crear y restar agujeros para los pernos
    radio = 1
    centro1_X = box1[0]
    centro1_Y = (box1[2] + box1[3]) / 2
    mapdl.cyl4(centro1_X, centro1_Y, radio)
    centro2_X = (box2[0] + box2[1]) / 2
    centro2_Y = box2[3]
    mapdl.cyl4(centro2_X, centro2_Y, radio)
    mapdl.aadd("all")

    # Crear el primer agujero de perno
    perno1_X = box1[0]
    perno1_Y = (box1[2] + box1[3]) / 2

    perno1 = mapdl.cyl4(perno1_X, perno1_Y, radio_perno)
    perno2_X = (box2[0] + box2[1]) / 2
    perno2_Y = box2[3]
    perno2 = mapdl.cyl4(perno2_X, perno2_Y, radio_perno)

    # Eliminar áreas de agujeros de los pernos del soporte
    mapdl.asba("all", perno1)
    soporte = mapdl.asba("all", perno2)

    # Definir propiedades del material
    modulo_young = 30e6  # Módulo de Young
    coef_poisson = 0.27  # Coeficiente de Poisson
    mapdl.mp("EX", 1, modulo_young)
    mapdl.mp("PRXY", 1, coef_poisson)

    # Establecer el grosor del elemento
    grosor = 0.5
    mapdl.r(1, grosor)  # grosor de 0.5 unidades de longitud

    # Tipo de elemento y malla
    mapdl.et(1, "PLANE183", kop3=3)
    mapdl.esize(tamaño_elemento)
    mapdl.amesh(soporte)
    
    mapdl.allsel()
    mapdl.solution()

    mapdl.antype("STATIC")

    bc1 = mapdl.lsel(
        "S", "LOC", "X", perno1_X - radio_perno, perno1_X + radio_perno
    )

    fixNodes = mapdl.nsll(type_="S")

    # Condiciones de frontera
    mapdl.d("ALL", "ALL", 0)  # Se asume cero por defecto

    # Aplicar carga de presión
    mapdl.lsel("S", "LOC", "Y", perno2_Y - radio_perno, perno2_Y)
    mapdl.lsel("R", "LOC", "X", 0, perno2_X)
    mapdl.sf("ALL", "PRES", carga_presion[0], carga_presion[1])
    mapdl.allsel()

    mapdl.lsel("S", "LOC", "Y", perno2_Y - radio_perno, perno2_Y)
    mapdl.lsel("R", "LOC", "X", perno2_X, perno2_X + radio_perno)
    mapdl.sf("ALL", "PRES", carga_presion[1], carga_presion[0])
    mapdl.allsel()

    mapdl.solve()
    mapdl.post1()
    result = mapdl.result

    # Guardar la imagen de desplazamiento
    ruta_imagen_deformacion = "static/images/deformation_plot.png"
    argumentos_barra = dict(
        title_font_size=20,
        label_font_size=16,
        shadow=True,
        n_labels=9,
        italic=True,
        bold=True,
        font_family="arial",
        title="Desplazamiento Normalizado (in)",
        color="black",
    )

    mapdl.post_processing.plot_nodal_displacement(
        'NORM',
        cpos="xy",
        edge_color="black",
        background="beige",
        show_edges=True,
        scalar_bar_args=argumentos_barra,
        n_colors=256,
        cmap="jet",
        savefig=ruta_imagen_deformacion
    )

    result.plot_principal_nodal_stress(
    0,
    "SEQV",
    cpos="xy",
    background="w",
    text_color="k",
    add_text=True,
    show_edges=True,
    )

    mapdl.exit()

    return ruta_imagen_deformacion
