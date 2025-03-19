import nbformat

with open('jupyter.ipynb', "r", encoding="utf-8") as f:
    notebook = nbformat.read(f, as_version=4)

notebook.metadata["title"] = "ANALIZAR LA CORRELACIÓN ENTRE EL NIVEL EDUCATIVO PARENTAL Y LA PREPARACIÓN PREVIA PARA EXÁMENES EN ESTUDIANTES DE 5º Y 6º GRADO, CONSIDERANDO EL SEXO DEL ESTUDIANTE COMO FACTOR CLAVE EN ESTUDIANTES CON PADRES DE MENOR FORMACION EDUCATIVA"
notebook.metadata["date"] = "Ricardo Quintero, Diego Aguilar"
notebook.metadata["author"] = "Ricardo Quintero, Diego Aguilar"

with open('jupyter.ipynb', "w", encoding="utf-8") as f:
    nbformat.write(notebook, f)

print("Metadatos actualizados")