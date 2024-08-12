'''
30/07/2024
C. Fdez

Script para la impresión de las etiquetas tanto la FCT como la del EOL
Para generar la etiqueta se lanza generate_label.sh y se pasan como parámetros
    - El contenido del datamatrix
    - El contenido del texto
    - El formato de etiqueta que queremos crear
        - serial --> Formato de etiqueta del FCT (12mm x 26mm)
        - eol --> Formato de etiqueta del EOL (12mm x 15mm)

Para la impresión usaremos el comando lpr -P y le pasamos dos parámetros
    - El primer parámetro indica el hostname de la impresora
    - El segundo parámetro indica el nombre de la etiqueta a imprimir
    Ejemplo: lpr -P Brother_QL_820NWB 1223AB1_eol.png

'''