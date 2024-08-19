 
# Sports Gear Recommender System
 
## Overview
 
The Sports Gear Recommender System is an application designed to help users find the most suitable sports gear based on their preferences and requirements. It leverages LLM from Gemini to analyze user input and recommend personalized gear options by searching from the real-time updated database.
 
## Features

- **ALL-IN-ONE**
  - All components are packaged within a docker container, easy to build and run on your local with no dependencies concern
  - One Remind, Gemini API needs VPN to use, so _make sure you use VPN before using the app_
 
- **Personalized Recommendations:** Get tailored sports gear suggestions based on user preferences.

- **Diverse Gear Selection:** Covers a wide range of sports and gear types.

- **User-Friendly Interface:** Easy to navigate and use.
  
- Vertex AI Google Collab Notebook
  - Embedding and vector search for our scraped data but Not integrated with the current web app yet)
  - https://colab.research.google.com/drive/1Z6aZU1giTCXVpI5UtDyGbRjeWtACaaq4?usp=sharing

## File Structure

- Consumer, Producer (Docker-related)
- Docker-compose.yml (Dependency for all the components to run the app)
- Gemini-chatbot (WebAPP)
- Web-scrapper, analysis_dacathlon_data.ipynb (Data scrapping from decathlon)
 
## Prerequisites
 
- **Docker:**
 - Ensure that Docker is installed and run on your system.
 - You can download Docker from [here](https://www.docker.com/products/docker-desktop).
- All API-key are stored in docker-compose.yml and will expire within three days after this project for security concern

## Getting Started
 
### Step 1: Clone the Repository
 
First, clone the repository to your local machine using the following command:
 
```bash

git clone https://github.com/tommyNg0530/kafka.git

cd kafka

```
 
### Step 2: Build the Docker Image
 
Navigate to the project directory and build the Docker image:
 
```bash

docker-compose build

```
 
### Step 3: Run the Application
 
Once the image is built, you can start the application using:
 
```bash

docker-compose up

```
 
This command will start the application and all its dependencies in Docker containers.
 
### Step 4: Access the Application
 
After running the Docker containers, you can access the Sports Gear Recommender System by navigating to `http://localhost:3000` in your web browser. Replace `your-port` with the port specified in the `docker-compose.yml` file.
 
## Stopping the Application
 
To stop the application and remove the containers, use:
 
```bash

docker-compose down

```
 
## Configuration
 
The application settings and environment variables can be configured in the `docker-compose.yml` file. Modify this file according to your deployment requirements.
 
## Contributing
 
We welcome contributions to improve the Sports Gear Recommender System. Feel free to submit pull requests or open issues in the repository.
 
## License
 
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
 

 
