# AI-Powered Cancer Care: From Detection to Recovery
This project is a Clinical Decision Support System (CDSS) I built to help doctors make sense of complex cancer data. Instead of just making another AI model that sits in a notebook, I wanted to build something interactive. I combined a Java desktop interface with a Python-based AI engine to make it feel like a real medical tool.

## Why I Built This
Cancer screening is usually a slow, manual process. Doctors have to sift through lifestyle data, tumor morphology, and staging all at once. My goal was to automate the data analysis part so medical professionals can focus more on patient care.

---

## Technical Architecture
I chose a distributed architecture to get the best of both worlds:

* The Interface (Java Swing): I used Java for the frontend because it is reliable for building multi-tabbed desktop apps. It handles all user inputs and data display.
* The Brain (Flask & Scikit-Learn): Python is the industry standard for AI, so my backend runs a Flask server that processes data using Random Forest models. I picked Random Forest because it is excellent at handling the noisy data often found in medical records.
* The Safety First Logic: One thing I am proud of is my Hybrid Logic. I realized AI isn't perfect, so if a patient is at Stage IV, my code is designed to prioritize clinical safety and flag them as High Risk automatically—ensuring the AI doesn't miss critical cases.

---

## Project Structure
* /frontend: The Java source code (MedicalDSS.java).
* /backend: The Python API (app.py) and the script to train the AI (train_models.py).
* /data: The datasets I used for training and testing.
* requirements.txt: The libraries you need to run the Python side.

---

## Getting it Running
To keep this repository lightweight, I did not upload the bulky .pkl model files. You will need to generate them on your machine first.

### 1. The Backend
1. Go into the backend/ folder.
2. Install the dependencies: pip install -r requirements.txt
3. Train the AI: Run python train_models.py. This creates the models locally so the app can use them.
4. Start the bridge: python app.py (It should start running on localhost:5000).

### 2. The Frontend
1. Open the frontend/ folder in your IDE.
2. Run MedicalDSS.java.
3. Note: Make sure the Python server is running before you try to get a prediction.

---

## Challenges I Faced
* Git Syncing: I learned the hard way that GitHub has limits for large files. I had to clean my history and switch to a train-on-demand setup to keep the repository fast and accessible.
* The Bridge: Getting Java to talk to Python via JSON took a few tries to get the data types exactly right, but it now works seamlessly.