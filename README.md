# Project Setup and Installation Guide (Linux)

This guide will help you set up and run the project on a Linux machine. Follow the steps below to install the required dependencies and configure the environment.

### Prerequisites
Before proceeding, make sure your system meets the following requirements:
- **Operating System**: Linux
- **Python Version**: Python 3.x
- **Package Manager**: pip (Python's package manager)

You will also need the following packages and tools installed on your system:

- **FFmpeg**: Required for audio processing.
- **Ollama**: A tool used for pulling Llama models.

### Step-by-Step Installation Instructions

#### 1. Update Package List

To ensure your system is using the latest package versions, run the following command to update the package list:\
```
sudo apt update
```

#### 2. Install Python Package Manager (pip)

Install pip, the package manager used to install Python libraries and dependencies:
```
sudo apt install python3-pip
```

#### 3. Install FFmpeg
FFmpeg is required for handling audio files. Install it by running:
```
sudo apt install ffmpeg
```

#### 4. Install Ollama and Pull Phi3
Ollama is a tool to pull the Phi3 model, which is used in the project. First, install Ollama:
```
sudo curl -fsSL https://ollama.com/install.sh | sh
```

Next, use Ollama to pull the required Phi3 model:
```
ollama pull phi3
```

#### 5. Create a Virtual Environment
It's recommended to create a virtual environment to isolate the project dependencies. You can do this by running:
```
python3 -m venv venv
```
This command will create a directory named venv in your project folder, containing the virtual environment.

#### 6. Activate the Virtual Environment
Once the virtual environment is created, activate it using the following command:
```
source venv/bin/activate
```
You should see the virtual environment name (venv) in your terminal prompt, indicating that it's active.

#### 7. Install Project Dependencies
With the virtual environment activated, install the project dependencies using pip:
```
pip install -r requirements.txt
```
This command will read the requirements.txt file and install the necessary Python packages to run the project.

### Additional Notes

1. **Virtual Environment Management**: If you ever need to deactivate the virtual environment, simply run the following command:
```
deactivate
```
This will return you to the system's default Python environment.

2. **Dependency Installation**: Ensure that you install all dependencies while the virtual environment is active to avoid conflicts with the global Python environment.

3. **Environment Variables**: If your project requires environment variables (e.g., `JWT_SECRET_KEY`), store them in a `.env` file and load them securely.

4. **Git Setup**: Remember to exclude the venv folder from version control by adding it to your `.gitignore` file. This ensures that the virtual environment remains local to your machine and doesn't get uploaded to GitHub.

### Running the Project
After completing the setup steps, you should be ready to run the project. Make sure the virtual environment is activated before running any Python scripts:
```
source venv/bin/activate
```
This guide should help new developers set up and run the project with ease. Let me know if you need further modifications or additional sections!