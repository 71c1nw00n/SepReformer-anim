# **Separate and Reconstruct: Asymmetric Encoder-Decoder for Speech Separation**  
Team project repository for **CS472: Introduction to AI**  

## **1. Data Pre-Processing**
### **1) Human Datasets**  
There are 4 files for generalization and normalization to use human voices as a dataset.  
We used 4 types of datasets: **LibriSpeech, TIMIT, VCTK, WSJ0**.

### **2) Animal Datasets**  
We used the `data_pre-processing.ipynb` file to process the animal data needed for training and testing the model.

---

## **2. Data Mixing**  
The **animal+animal, animal+human, human+human** mixed audio files were created using the `data_mixing.ipynb` file.  
More specifically, please refer to the three specific mixing files:  

- `animal_animal_mixing.ipynb`
- `human_animal_mixing.ipynb`
- `human_human_mixing.ipynb`

Our datasets used in the model are accessible at the links below:  

- **Final dataset** (n=32,000)  
- **Actual used dataset** (n=1,800)  

---

## **3. Model Training**  
In the latest update of the baseline model, a few bugs were identified, so we made some code adjustments.  
Additionally, we modified the parameters in the config file as well as the file and folder paths to fit our environment.  
For convenience, the modified model was uploaded to GitHub for use.  

🔗 **GitHub URL of our modified model:**  
[https://github.com/dohunny/cs470-github.git](https://github.com/dohunny/cs470-github.git)  

### **Training Process**  
The `train.ipynb` file is used to set up the environment for training the model. The steps are as follows:  

1. Load the model from GitHub and install the necessary Python libraries for execution.  
2. Modify the paths of the files and folders where the dataset is located.  
3. Create the SCP files based on the dataset paths.  

When all preparations are complete, train the model with the following command:  

```bash
$ !python run.py --model SepReformer_Base_WSJ0 --engine-mode train

---

## **4. Testing with Other Pretrained Models**  
We tested our dataset with various pretrained speech separation models.  
To check the output of each model, run the corresponding `.ipynb` file:  

- `ConvTasNet.ipynb`
- `DPTNet.ipynb`
- `DPRNN.ipynb`

Each file contains the necessary configurations to evaluate the respective model on our dataset.
