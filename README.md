# MultiAgent-Security-System  

Sistema multiagente para patrullaje autónomo en zonas de riesgo. Integra 1 dron con cámara dinámica, 7 cámaras estáticas y personal de seguridad, todos con visión computacional para detectar y responder a riesgos o actividades sospechosas. Incluye código de los agentes, simulación en Unity y documentación.  

---
## Contenido del repositorio

### 1. Código
- **Carpeta:** `Codigo/`
  - `DronAgentes.py`: Implementación de los agentes en Python (DroneAgent, GuardAgent, CameraAgent) y su lógica de interacción.
  - `ontology.owl`: Script de manejo de la ontología.
  - `ontology.py`: Ontología desarrollada para modelar las relaciones y atributos de los agentes.

### 2. Unity
- **Carpeta:** `Unity/`
  - `Unity.pdf`: Documento que contiene el link al ZIP del proyecto de Unity en OneDrive.
  - O también, podrás consultarlo desde https://tecmx-my.sharepoint.com/:f:/g/personal/a01642991_tec_mx/EuwS9JaEPfZDibjqxOMPIswBWsZmSHfhwzty90_sGyTbEw?e=ZdFC5W
    
 ### 3. Documentación
- **Carpeta:** `Documentacion/`
  - `Documentación - Documentación - Evidencia 2 - Entrega Intermedia.pdf`: Propuesta formal del reto, que incluye:
    - Descripción del problema.
    - Propiedades de agentes y del ambiente.
    - Diagramas de clases y secuencia.
    - Plan de trabajo y métricas de evaluación.

---

## Cómo usar este repositorio

### 1. Ejecutar el código Python
- **Requisitos:**
  - Python 3.x.
  - Bibliotecas necesarias: `agentpy`, `owlready2`.
- **Instrucciones:**
  1. Ve a la carpeta `Codigo/`.
  2. Ejecuta el script `DronAgentes.py`:
     ```bash
     python DronAgentes.py
     ```
### 2. Acceso a Unity

1. **Descomprime el archivo ZIP** encontrado a forma de link en la carpeta "Unity" en una carpeta, por ejemplo: `C:\Proyectos\MultiAgent-Security-System`.  

2. **Abre Unity Hub**, haz clic en **"Add"** y selecciona la carpeta raíz del proyecto.  

3. **Selecciona la última versión de Unity**. Si no la tienes instalada, descárgala directamente desde Unity Hub.  

4. **Abre el proyecto** desde Unity Hub. Unity procesará los archivos automáticamente.  

Con estos pasos, deberías poder ejecutar el proyecto correctamente.

### 3. Consultar la documentación
- El archivo principal está en `Documentacion/`. Contiene información detallada sobre el diseño del sistema y los planes de trabajo.

---

# Scripts de vision computacional y  Scripts de Unity:
Los scripts de Computer Vision utilizando OpenAI, se encuentran en el ZIP de Unity

---
## Colaboradores

Proyecto desarrollado por el equipo **Wizards**:
- Fernanda Díaz Gutiérrez
- Miguel Ángel Barrientos Ballesteros
- Carlos Iván Armenta Naranjo
- Jorge Javier Blázquez González
- Gabriel Álvarez Arzate

---
