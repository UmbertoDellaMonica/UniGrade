
# 📚 UniGrade

<div align="center">
  <img src="/docs/unigrade-logo-icon.ico" width="100" alt="UniGrade Logo" />
  <h3>Manage your university transcript effortlessly / Gestisci il tuo libretto universitario senza sforzo</h3>
  <p>
    <!-- Lingua toggle visivo -->
    <a style="text-decoration:none; margin-right:10px;">
      <img src="docs/united-kingdom.png" width="30" />
    </a>
    <a style="text-decoration:none;">
      <img src="docs/italy.png" width="30" />
    </a>
  </p>
</div>

---

### 🌐 Lingua / Language Toggle

<details>
<summary id="english">🇬🇧 English</summary>

### 🚀 Overview

**UniGrade** is a **lightweight and offline desktop app** for university students who want to manage their academic records digitally. With UniGrade you can:

- 📝 Track all exams and grades
- 🎯 Calculate **weighted and arithmetic GPA**
- 📊 Monitor academic performance over time
- 💾 Store all data **locally** using **SQLite**
- 🖼️ Upload and update your personal profile **avatar**

### ✨ Features

- User registration and personal academic profile management
- Add, edit, and remove exams with grades and CFU
- Real-time calculation of **weighted GPA**
- Fully customizable user settings
- Secure offline storage with **SQLite**
- Beautiful charts showing exam progress

### 📸 Screenshots

<div align="center">
<img src="assets/screenshots/dashboard.png" width="500" />
<img src="assets/screenshots/exam_chart.png" width="500" />
</div>

### 🧮 Mathematical Formulas

#### Weighted GPA

\[
\text{Weighted GPA} = \frac{\sum_{i=1}^{n} v_i \cdot c_i}{\sum_{i=1}^{n} c_i}
\]

#### Initial Graduation Grade (without bonuses)

\[
\text{Initial Graduation Grade} = \text{round} \left( \text{Weighted GPA} \times \frac{110}{30} \right)
\]

### 🛠️ Developer Build Instructions

Activate the Python environment:

```sh
.\activate-env.bat
```

Build the program from source:

```sh
pyinstaller --onefile --windowed --icon=assets/unigrade-logo-icon.ico --add-data "assets;assets" app.py --name UniGrade
```

</details>

<details>
<summary id="italiano">🇮🇹 Italiano</summary>

### 🚀 Panoramica

**UniGrade** è un’applicazione desktop **leggera e completamente offline** pensata per studenti universitari che vogliono gestire il proprio libretto digitale. Con UniGrade puoi:

- 📝 Tenere traccia di tutti gli esami e voti
- 🎯 Calcolare **media ponderata e aritmetica**
- 📊 Monitorare le performance accademiche
- 💾 Archiviare tutti i dati **localmente** con **SQLite**
- 🖼️ Caricare e aggiornare l’**avatar** personale

### ✨ Funzionalità

- Registrazione e gestione del profilo accademico
- Aggiunta, modifica e rimozione degli esami con voti e CFU
- Calcolo in tempo reale della **media ponderata**
- Personalizzazione delle impostazioni
- Archiviazione sicura dei dati offline con **SQLite**
- Grafici intuitivi sull’andamento degli esami

### 📸 Screenshot

<div align="center">
<img src="assets/screenshots/dashboard.png" width="500" />
<img src="assets/screenshots/exam_chart.png" width="500" />
</div>

### 🧮 Formule Matematiche

#### Media Ponderata

$$
\text{Media Ponderata} = \frac{\sum_{i=1}^{n} v_i \cdot c_i}{\sum_{i=1}^{n} c_i}
$$

#### Voto di Laurea Iniziale (senza bonus)

$$
\text{Voto di Laurea Iniziale} = \text{round} \left( \text{Media Ponderata} \times \frac{110}{30} \right)
$$

### 🛠️ Istruzioni per sviluppatori

Attiva l’environment Python:

```sh
.\activate-env.bat
```

Builda il programma da sorgente:

```sh
pyinstaller --onefile --windowed --icon=assets/unigrade-logo-icon.ico --add-data "assets;assets" app.py --name UniGrade
```

</details>

---

### ⚡ Notes / Note

- All data is **stored locally** and **securely** in SQLite
- Tutti i dati sono **conservati localmente** in modo sicuro con SQLite

---

### <img src="docs/certificate.png" width="30" /> License / Licenza

<details>
<summary>🇬🇧 English</summary>

This project is licensed under the **AGPLv3 License** – see the [LICENSE](LICENSE) file for details.

</details>

<details>
<summary>🇮🇹 Italiano</summary>

Questo progetto è rilasciato sotto licenza **AGPLv3** – vedi il file [LICENSE](LICENSE) per i dettagli.

</details>
---
