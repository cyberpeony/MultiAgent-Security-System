# MultiAgent-Security-System  

Sistema multiagente para patrullaje autónomo en zonas de riesgo. Integra 1 dron con cámara dinámica, 7 cámaras estáticas y personal de seguridad, todos con visión computacional para detectar y responder a riesgos o actividades sospechosas. Incluye código de los agentes, simulación en Unity y documentación.  

Desarrollado durante la etapa de Enfoque del Tecnológico de Monterrey, este proyecto simula un sistema de patrullaje autónomo basado en agentes con visión computacional, diseñado para detectar amenazas en tiempo real dentro de zonas de riesgo. Fue construido integrando múltiples tecnologías como Unity, Python, Flask y OpenAI Vision.

---
## Contenido del repositorio

### 1. Código
- **Carpeta:** `Codigo/`
  - `DroneAgents.py`: Implementación de los agentes en Python (DroneAgent, GuardAgent, CameraAgent, WindAgent), la Ontología de Agentes y su lógica de interacción.
  - `ontology.owl`: Script de manejo de la ontología.

### 2. Unity
- **Carpeta:** `Unity/`
  - `Unity (links).pdf`: Documento que contiene el link al ZIP del proyecto de Unity en OneDrive.
  - O también, podrás consultarlo desde [https://tecmx-my.sharepoint.com/:f:/g/personal/a01642991_tec_mx/EuwS9JaEPfZDibjqxOMPIswBWsZmSHfhwzty90_sGyTbEw?e=ZdFC5W](https://tecmx-my.sharepoint.com/:f:/g/personal/a01642991_tec_mx/EuwS9JaEPfZDibjqxOMPIswBc0Uv16r1om98RFH-yL52tA?e=3QXNKg)
    
 ### 3. Documentación
- **Carpeta:** `Documentacion/`
  - `Entrega Intermedia.pdf`: Propuesta formal del reto en la fase intermedia, que incluye:
    - Descripción del problema.
    - Propiedades de agentes y del ambiente.
    - Diagramas de clases y secuencia.
    - Plan de trabajo y métricas de evaluación.
  - `Presentación_Pitch.pdf`: Presentación final (pitch) de nuestra propuesta.
  - `Documentación_Final.pdf`: Propuesta formal del reto en la fase final, que incluye:
    - Descripción del problema.
    - Propiedades de agentes y del ambiente (Actualizadas dado las mejoras).
    - Diagramas de clases y secuencia de protocolos de interacción (Actualizados, finales).
    - Diagrama de la ontología (Nuevo).
    - Utilidad o éxito de los agentes finales y sus gráficos (Actualizado y nuevo, respectivamente).
    - Plan de trabajo y métricas de evaluación (Actualizado).
---

## Cómo usar este repositorio

### 1. Prepara el proyecto
1. **Descomprime el archivo ZIP** encontrado a forma de link en la carpeta "Unity" en una carpeta, por ejemplo: `C:\Proyectos\MultiAgent-Security-System`.  

2. **Abre Unity Hub**, haz clic en **"Add"** y selecciona la carpeta raíz del proyecto.  

3. **Selecciona la última versión de Unity**. Si no la tienes instalada, descárgala directamente desde Unity Hub.  

4. **Abre el proyecto** desde Unity Hub. Unity procesará los archivos automáticamente.  

### 2. Ejecutar el código de visión computacional y socket
1. En los archivos del proyecto de unity, navega a `Assets/Script/openai_vision`.

2. Ejecuta el archivo llamado `demo3.py`. Esto inicializará el servidor y esperará las imágenes que Unity proporciona en la simulación.
   ```bash
     python demo3.py
     ```

### 3. Ejecutar el código de agentes en Python
- **Requisitos:**
  - Python 3.x.
  - Bibliotecas necesarias: `agentpy`, `owlready2`.
- **Instrucciones:**
  1. Ve a la carpeta `Codigo/`.
  2. Ejecuta el script `DroneAgents.py`:
     ```bash
     python DroneAgents.py
     ```
### 3. Iniciliza Unity
  1. Una vez abierto el proyecto de unity, da click en iniciar la simulación.


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
