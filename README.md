![AI Logo](https://ecoclimsolutions.files.wordpress.com/2023/12/rmcai.png?resize=219%2C219)
# EcoIdentify

EcoIdentify is an AI-powered algorithm that makes recycling convenient and easy! 
Garbage classification involves separating wastes according to how it's handled or processed. It's important as some materials are recyclable and others are not, and cross-contamination can pose serious risks to infrastructure and recycling-ability.

---

## Project Workflow

1. **Model Training**  
   - File: `Classification_for_EcoIdentify.ipynb`  
   - Built in Google Colab  
   - This code was used to train the classification model using a dataset found on Kaggle.  

2. **Web Deployment**  
   - File: `app.py`  
   - Deployed on Hugging Face Spaces.  
   - This is the main file that uses Streamlit to deploy the model created using the previous code. 

3. **Hardware Deployment**  
   - File: `Deployment_on_Raspi.py`  
   - Runs on a Raspberry Pi inside a smart trash bin.  
   - This program enables real-time waste classification using Roboflow's API.  

---

## Repository Structure

| File | Purpose |
|------|---------|
| `Classification_for_EcoIdentify.ipynb` | Used for training and building model |
| `app.py` | Deployed for public usage using web application |
| `Deployment_on_Raspi.py` | Uses GPIO pins within Raspberry Pi to control motors using output from Roboflow's API |
| `README.md` | Contains project overview |
| `LICENSE` | Usage rights and permissions as highlighted by MIT License |

---

## Demonstration
**Web App**: [Public Demonstration](https://huggingface.co/spaces/EcoClim-Solution/EcoIdentify)  

---


## License

All code is licensed under MIT License. To view terms and conditions visit this [information page](https://mit-license.org/).
