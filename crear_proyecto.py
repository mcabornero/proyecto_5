import deeplabcut

# Parámetros
project_name = "proyecto5"
your_name = "Mario"
video_path = r"C:\Users\Usuario01\PycharmProjects\PythonProject\video1.mp4"
working_directory = r"C:\Users\Usuario01\PycharmProjects\PythonProject"

# Crear nuevo proyecto
config_path = deeplabcut.create_new_project(
    project_name,
    your_name,
    [video_path],
    working_directory,
    copy_videos=True
)

print(f"✅ Proyecto creado en: {config_path}")
