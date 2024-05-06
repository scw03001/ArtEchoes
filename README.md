<!-- 디렉토리 정리 한번 싹 하고 Path 다시 수정할 것 -->
# ArtEchoes

To professor: Since we met every Thursday to conduct progress reports and pair programming, there are not many code reviews in the GitHub repository.

## Project Overview

This project aims to create a web application to enhance users' understanding of the artworks while also providing entertainment. This application includes three major functionalities:

### 1. Chatbot System

The core feature of this project is the chatbot system. It allows users to ask various questions about artwork after taking photos of it. For example, if a user captures a self-portrait by Van Gogh, they can inquire about the background of its creation, the techniques he employed, and more. The chatbot provides detailed answers.

### 2. Find Artist

This feature identifies the artist whose style most closely matches a given image. We use a ResNet 18-based model for this artist classification.

### 3. Make Animation

Artworks are static, and sometimes we want to see them in motion. Inspired by the idea of imagining paintings as animated, this feature generates random animations about 4-second videos.

## Technologies \& Codes

### Programming Languages

- Model Training \& Implementation: PyTorch
- Web Application: NextJS, React, TypeScript, Flask & Python

### Model

#### ResNet18

Due to the limited diversity of our training dataset, we implemented transfer learning for our model. We used a pre-trained **ResNet 18** from PyTorch, modifying the final layer to accommodate the 50 artists in our dataset.

#### GPT-3.5

Our chatbot is based on GPT-3.5 to respond to the questions.

#### Stable Video Diffusion

The video generation from the given image is based on **Stable Video Diffusion**. For more details, see the [Stable Video Diffusion paper](https://static1.squarespace.com/static/6213c340453c3f502425776e/t/655ce779b9d47d342a93c890/1700587395994/stable_video_diffusion.pdf).

#### Grad-CAM

We use Grad-CAM to visualise the reasoning of the classificaiton. Since our base model is ResNet18, our target layer for Grad-CAM is fourth-to-last layer. If you want to see how this works, see the [pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam). 

### Datasets

#### Train Dataset

The base dataset is [**Best Artworks of All Time**](https://www.kaggle.com/datasets/ikarus777/best-artworks-of-all-time). However, some artists' datasets contain only a few images. To address this imbalance and the lack of training data, we created a [augmentData.py](./dataset/augmentData.py) to augment and increase images.

#### Test Dataset

We collected our test dataset using [Google Custom Search](./GoogleImageSearch/image_crawler.py), gathering up to 10 images for each artist.

### APIs

#### GoogleVision AI

We use GoogleVision AI API to find the label of the artworks by using [**Detect Web entities and pages**](https://cloud.google.com/vision/docs/detecting-web). We extract the `best_guess_labels` and return the one with the highest score. We then ask users to verify if this label is correct. If not, users can manually enter the artwork name before starting the chatbot.

#### OpenAI

We use OpenAI API to respond to the questions. The detail of the API is [here](https://platform.openai.com/docs/api-reference/introduction).

#### Stability AI

Stability.AI provides video generation from a given image. We planned to make an animation with the input image and the user prompt. Unfortunately, creating the model for this requires significant work and is out of our ability. Additionally, we do not have enough datasets to train the model. Therefore, we decided to use the API to provide videos from the given image. We use a high value of motion_bucket_id to provide the motion. The detail of the API is [here: Image-to-Video](https://platform.stability.ai/docs/api-reference#tag/Edit/paths/~1v2beta~1stable-image~1edit~1remove-background/post).

## Files

The folders below contain files organized according to their respective roles:

- [GoogleImageSearch](./GoogleImageSearch): Contains our dataset information, and the image crawler.
- [Wikipedia](./Wikipedia/): Contains the Wikipedia PDF files and script for 50 artists.
- [dataset](./dataset/): Contains our model trining code and saved models.
- [frontend](./frontend/): Contains frontend code.
- [website](./website/): Contains backend code.

## Instructions

Create virtual env

```bash
conda create -n env
conda activate env
```

Install requirements.txt

```bash
pip install -r requirements.txt
```

Create a GCP account (googleVision API), OpenAI account, Stability.AI account

Create .env file, and add API keys on it

```bash
google_search_api_key = "key"
google_custom_search_api = "key"
stability_api = "key"
chatbot_api= "key"
```

### Instructions for Web Application

To get our amazing application up and running, we need to set up and start 2 things:

1. Our frontend application that will be the point of interaction for the user.
2. Backend server that will respond to the HTTP requests sent by the web application.

#### Quick Start (Frontend)

Run in the terminal this command to install the dependencies:

```bash
npm install
```

Then run this command to start your local server

```bash
npm run dev
```
The local server will run in `localhost:3000`

#### Quick Start (Backend)
Run in the terminal this command to install the dependencies:

```bash
pip3 install -r requirements.txt
```

Then run this command to start your backend server

```bash
python3 app.py
```
The backend server will run in `localhost:8000`


#### After these two steps, our application will be ready to rock!

## Sample Output

### Find Artist

![ACV demo finartist10](https://github.com/scw03001/ArtEchoes/assets/20364366/0800fc4a-2d6a-4baf-a2ba-4ddf95f7dec9)


### Animation

![ACV demo animation10](https://github.com/scw03001/ArtEchoes/assets/20364366/6aee789d-6a6b-4948-a653-58dce6e7fd25)


### Chatbot

![ACV demo chat](https://github.com/scw03001/ArtEchoes/assets/20364366/b4b56938-b608-40d7-8842-941763d9f0dd)

