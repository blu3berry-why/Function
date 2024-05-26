# Azure Blob Trigger Function with OpenCV

This repository contains an Azure Function that processes images stored in Azure Blob Storage. When an image is uploaded to a specific container, this function is triggered to download the image, add a border using OpenCV, and upload the processed image back to the blob storage with updated metadata.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Overview

This Azure Function listens to a specified Azure Blob Storage container. When a new image is uploaded, the function:
1. Downloads the image.
2. Adds a yellow border to the image using OpenCV.
3. Uploads the processed image back to the storage with a new name and metadata indicating it has been processed.

## Prerequisites

Before you begin, ensure you have the following:
- An Azure account.
- An Azure Storage account and a blob container.
- Python 3.9+ installed locally.
- Azure Functions Core Tools installed.
- Visual Studio Code with the Azure Functions extension (optional but recommended).

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/azure-blob-trigger-opencv.git
cd azure-blob-trigger-opencv
```

### 2. Create a Virtual Environment and Install Dependencies

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of your project and add your Azure Storage connection string:

```
felhohf4storage_STORAGE=your_azure_storage_connection_string
```

### 4. Deploy to Azure

To deploy the function to Azure, you can use the Azure Functions Core Tools or Visual Studio Code.

#### Using Azure Functions Core Tools:

```sh
func azure functionapp publish <your-function-app-name>
```

#### Using Visual Studio Code:

1. Open the project in VS Code.
2. Click on the Azure icon in the Activity Bar.
3. Sign in to your Azure account.
4. Click the "Deploy to Function App" button and follow the prompts.

## Usage

Once deployed, the Azure Function will automatically trigger whenever a new image is uploaded to the specified blob container.


## Dependencies

- **azure-functions**: Azure Functions Python library.
- **azure-storage-blob**: Azure Blob Storage library for Python.
- **opencv-python-headless**: OpenCV library without GUI functionality.
- **numpy**: Fundamental package for scientific computing with Python.

Install the dependencies using the following command:

```sh
pip install -r requirements.txt
```
