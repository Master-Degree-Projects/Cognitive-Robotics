# Cognitive Robotics Project
## Introduction
The Guardian of Shopping Mall Bot is an intelligent robotic system designed to assist shoppers by providing information and helping locate individuals within a shopping mall environment. Developed by a team at the University of Salerno as part of the Master's degree program in Artificial Intelligence and Intelligent Robotics, this project leverages advanced cognitive robotics techniques to create an interactive and helpful shopping mall assistant.
The system is built upon a robust ROS (Robot Operating System) architecture that integrates person detection, speech recognition, natural language processing, and humanoid robot control. Using the Pepper robot as its physical embodiment, the Guardian Bot can engage with mall visitors, understand their queries through natural conversation, and assist in locating specific individuals based on their physical description and location history within the mall.

The core of the system's intelligence is powered by the RASA framework for natural language understanding, allowing the robot to comprehend complex queries about people's appearances, locations, and activities. The system can process details such as clothing descriptions (color, type of clothing), accessories (hats, bags), gender, and location information (presence at specific venues like bars or markets).
This repository contains the complete implementation of the Guardian of Shopping Mall Bot, including the ROS-based architecture, RASA NLU components, detection modules, and evaluation results. The project demonstrates practical applications of cognitive robotics in public spaces, combining computer vision, speech processing, and conversational AI to create a helpful and engaging robotic assistant.

_**More details about the choices made can be found in the `report.pdf` file.**_

## Authors and Acknowledgment
Project contributors:
- **[Mariniello Alessandro](https://github.com/alexmariniello)**
- **[Pepe Paolo](https://github.com/paolopepe00)**
- **[Rabasca Dario](https://github.com/Dariorab)**
- **[Vicidomini Luigi](https://github.com/luigivicidomini)**

Thank you to all the contributors for their hard work and dedication to the project.

## Overview Architecture

<p align="center">
  <img src="image\overview_architecture.jpg" width="700">
</p>

## How to execute

This section explains how to set up and run the Guardian of Shopping Mall Bot system.

### Prerequisites

- Ubuntu (18.04 or newer) with ROS installed  
- Python 3.7+ for RASA components  
- Properly configured ROS workspace (catkin)  
- Access to a Pepper robot or simulator  
- Network connection between your system and Pepper

### Installation

1. Clone The Repository

    ```bash
    git clone https://github.com/Master-Degree-Projects/Cognitive_Robotics  
    cd cognitive_robotics_project
    ```

2. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

3. Build the ROS Workspace

    ```bash
    cd ros
    catkin_make
    ```

4. Train the RASA Model

    ```bash
    cd ../rasa
    rasa train
    ```

### Running the System

1. Configure Pepper's IP Address
 
   * Open *`ros/run_system.sh`*
   * Update the *`PEPPER_ADDRESS`* variable with your Pepper robot's IP address.
2. Make the Script Executable

    ```bash
    cd ros
    chmod +x run_system.sh
    ```

3. Run the System

    ```bash
    ./run_system.sh
    ```

This script will automatically:

* Launch ROS core
* Start Pepper nodes and TTS client
* Initialize RASA-ROS integration
* Activate person engagement nodes
* Start speech recognition components

## System Usage

Once the system is running:

* Stand in front of Pepper (within 2 meters)
* When detected, Pepper will track your face and engage with you
* You can ask questions such as:

  * "Can you help me find someone?"
  * "I'm looking for a man wearing a red shirt"
  * "How many people visited the bar today?"


* Follow the conversation flow and provide additional information when prompted

## Running Tests
To test specific components:

### Test RASA NLU
```bash
cd rasa
rasa test nlu --nlu data/nlu --cross-validation
```
### Test RASA Core
```bash
rasa test core --stories tests/test_stories.yml
```