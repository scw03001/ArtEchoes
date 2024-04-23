<!-- 디렉토리 정리 한번 싹 하고 Path 다시 수정할 것 -->
# ArtEchoes

## Project Overview

This project aims to create a web application to enhance users' understanding of the artworks while also providing entertainment. This application includes three major functionalities:

### 1. Chatbot System

The core feature of this project is the chatbot system. It allows users to ask various questions about artwork after taking photos of it. For example, if a user captures a self-portrait by Van Gogh, they can inquire about the background of its creation, the techniques he employed, and more. The chatbot provides detailed answers.

### 2. Find Artist

This feature identifies the artist whose style most closely matches a given image. We use a ResNet 18-based model for this artist classification.

### 3. Make Animation

Artworks are static, and sometimes we want to see them in motion. Inspired by the idea of imagining paintings as animated, this feature generates random animations about 4 seconds videos.

## Technolgoies \& Codes

### Programming Languages

- Model Training \& Implementaion: PyTorch
- Web Application: Flask

### Model

#### ResNet18

Due to the limited diversity of our training dataset, we implemented transfer leaerning for our model. We used a pretrained **ResNet 18** from PyTorch, modifyinh the final layer to accomodate the 50 artists in our dataset.

#### GPT-3.5

Our chatbout is based on GPT-3.5 to respond to the questions.

#### Stable Video Diffusion

The video generation from the given image is based on **Stable Video Diffusion**. For more details, see the [Stable Video Diffusion paper](https://static1.squarespace.com/static/6213c340453c3f502425776e/t/655ce779b9d47d342a93c890/1700587395994/stable_video_diffusion.pdf).

#### Grad-CAM

TBC

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

Stability.AI provides video generation from given image. We planned to make animation with the input image and the user prompt. Unforutanetly, creating the model for this requires significant work and out of our ability. Additionally, we do not hav enough dataset to train the model. Therefore, we decided to use the API to provide videos from the given image. We use high value of motion_bucket_id to provide the motion. The detail of the API is [here: Image-to-Video](https://platform.stability.ai/docs/api-reference#tag/Edit/paths/~1v2beta~1stable-image~1edit~1remove-background/post).

## Files

#### dataset

This directory contains the model generation and the dataset-related codes.

- [augmentData.py](./dataset/augmentData.py): Augument images.
- [TrainRes18.py](./dataset/TrainRes18.py): Train the model.



dataset - dataset-related code.
augmentData.py -> create augmented image to increase the data size
TrainReset18 -> Transfer Learning code for Resne 18

## Instructions

Create virtual env

Install requirements.txt

Create env file

Create GCP server to run googleVision API + get .json file

export it to the server

## Sample Output

### Find Artist

![ACV demo finartist10](https://github.com/scw03001/ArtEchoes/assets/20364366/fa06b0ea-f9c3-4d6e-9034-4140af0fc1dc)


### Animation

![ACV demo animation10](https://github.com/scw03001/ArtEchoes/assets/20364366/91080330-7a45-4cbb-8daf-fd34a4344aa1)


### Chatbot

![ACV demo chat](https://github.com/scw03001/ArtEchoes/assets/20364366/79dee518-e4b2-475c-9d22-b82a525128e2)
