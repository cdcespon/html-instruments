# 🎹 Acordes al Teclado & Reproductor MIDI

Una aplicación web interactiva, moderna y ligera construida con **HTML5, Vanilla JavaScript y Web Audio API puro**. Diseñada para músicos, estudiantes y pianistas que desean visualizar digitaciones de acordes a dos manos, aprender teoría de voicings y estudiar piezas MIDI compás por compás con síntesis de sonido en tiempo real.

![Demo de la aplicación](demo.gif)

---

## 🚀 Enlaces Rápidos

* 🌐 **[Probar Online en vivo (Preview)](https://htmlpreview.github.io/?https://github.com/cdcespon/html-instruments/blob/main/keyboard-chords.html)**
* 📥 **[Descargar Proyecto Completo (.ZIP)](https://github.com/cdcespon/html-instruments/archive/refs/heads/main.zip)**
* 📄 **[Descargar solo `keyboard-chords.html`](https://raw.githubusercontent.com/cdcespon/html-instruments/main/keyboard-chords.html)**
* 🎥 **[Ver Video de Demostración con Audio (`demo.mp4`)](demo.mp4)**

---

## ✨ Características Principales

### 1. 🎼 Visualizador de Acordes Inteligente
* **Ortografía armónica exacta**: Aritmética de letras musicales (sin reemplazos arbitrarios de sostenidos/bemoles; la 7ª de Do siempre se analiza sobre Si).
* **Distribución a dos manos (Voicings)**:
  * 🟠 **Mano izquierda (Ámbar)**: Fundamentales, quintas y bajos.
  * 🟢 **Mano derecha (Teal)**: Estructura, extensiones (3ª, 7ª, 9ª, 11ª) y tensiones.
* **Digitación sugerida**: Números de dedo exactos (1 = pulgar, 5 = meñique) y cálculo de amplitud en semitonos.
* **Modos de reproducción**: Tocar acorde completo, arpegio ascendente ($\uparrow$), arpegio descendente ($\downarrow$), solo mano izquierda o solo mano derecha.

<p align="center">
  <img src="screenshot.png" alt="Visualizador de Acordes" width="700">
</p>

---

### 2. 🎛️ 5 Motores de Síntesis en Tiempo Real (Web Audio API)
Generación de sonido por síntesis pura en el navegador (sin samples pregrabados ni librerías externas):

* 🎹 **Piano de cola**: Síntesis aditiva con parciales inarmónicos, rigidez de cuerda, cuerdas desafinadas al unísono y ruido de martillo en el ataque.
* ⚡ **DX7 E.Piano**: Síntesis FM basada en el clásico patch *E.PIANO 1* (algoritmo 5, seis operadores con 3 pares portadora/modulador).
* 🎼 **Rhodes**: Síntesis FM con ataque metálico de modulación rápida y cuerpo cálido de sostenido.
* 🎷 **Hammond**: Síntesis aditiva de 9 barras armónicas (*drawbars*) con ratios senoidales y *key click*.
* 🎛️ **Moog**: Síntesis sustractiva analógica con osciladores dobles en diente de sierra y filtro pasabajos resonante con barrido de envolvente.

---

### 3. 📂 Reproductor MIDI Integrado
* **Carga tus propios archivos**: Soporta cualquier archivo `.mid` o `.midi`.
* **Visualización en teclado**: Muestra las notas activas en tiempo real diferenciadas por mano.
* **Control de tempo preciso**: Ajuste de velocidad porcentual (30% a 120%) con botones de paso fino.
* **Práctica por compases (Loop)**: Permite seleccionar un rango específico de compases para repetir y estudiar pasajes difíciles.
* **Aislamiento de manos**: Posibilidad de mutear la mano izquierda o derecha para practicar encima.

<p align="center">
  <img src="screenshot-midi.png" alt="Reproductor MIDI" width="700">
</p>

---

## 📁 Biblioteca de Riffs MIDI Incluida

El repositorio incluye más de 40 archivos MIDI listos para cargar y practicar en la carpeta [`riffs-midi/`](riffs-midi/):

| Género / Estilo | Tonalidades disponibles | BPM Referencia |
| :--- | :--- | :--- |
| **Blues Lento** | A, Bb, C, Eb, F, G | 60 BPM |
| **Blues Shuffle** | A, Bb, C, Eb, F, G | 100 BPM |
| **Bossa Nova** | A, Bb, C, Eb, F, G | 132 BPM |
| **Chacarera** | A, Bb, C, Eb, F, G | 100 BPM |
| **Montuno** | A, Bb, C, Eb, F, G | 160 BPM |
| **Rock Octavas** | A, Bb, C, Eb, F, G | 132 BPM |
| **Rock Órgano** | A, Bb, C, Eb, F, G | 116 BPM |

> Incluye también el script [`generar.py`](riffs-midi/generar.py) para crear o modificar patrones MIDI algorítmicamente con Python.

---

## 💻 ¿Cómo ejecutarlo?

No requiere Node.js, servidores, ni instalación de paquetes:

1. Clona o descarga este repositorio:
   ```bash
   git clone https://github.com/cdcespon/html-instruments.git
   ```
2. Abre `keyboard-chords.html` en cualquier navegador web moderno (Chrome, Edge, Firefox, Safari).
3. ¡Listo! Puedes hacer clic en las notas, elegir timbres y arrastrar tus archivos MIDI.

---

## 👤 Autor

Desarrollado por **Claudio Cespon**
* 💼 [Perfil en LinkedIn](https://www.linkedin.com/in/claudio-cespon/)
* 🐙 [GitHub: @cdcespon](https://github.com/cdcespon)

---
*Licencia MIT · Desarrollado con HTML5, CSS3, JavaScript & Web Audio API.*
