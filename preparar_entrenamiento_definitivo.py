import deeplabcut
import os

config_path = r"C:\Users\Usuario01\PycharmProjects\PythonProject\proyecto3-Mario-2025-05-27\config.yaml"

print("🔁 Paso 1: Convertimos CSV a HDF5...")
deeplabcut.convertcsv2h5(config_path)

print("🛠️ Paso 2: Creamos conjunto de entrenamiento...")
deeplabcut.create_training_dataset(config_path)

# Verificar que se ha creado el archivo pose_cfg.yaml
train_dir = os.path.join(
    os.path.dirname(config_path),
    "dlc-models", "iteration-0", "proyecto3May27-trainset95shuffle1", "train"
)
pose_cfg_path = os.path.join(train_dir, "pose_cfg.yaml")

if os.path.isfile(pose_cfg_path):
    print(f"✅ Éxito: pose_cfg.yaml encontrado en:\n{pose_cfg_path}")
else:
    print("❌ ERROR: No se generó el archivo pose_cfg.yaml.")
    print("Revisa si el config.yaml está bien definido y si hay imágenes + CSV válidos.")
