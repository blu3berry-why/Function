import azure.functions as func
import logging
from PIL import Image
from azure.storage.blob import BlobServiceClient
import io
import os
import cv2
import numpy as np

# app = func.FunctionApp()

# @app.blob_trigger(arg_name="myblob", path="felho-hf-container2/images/{name}",
#                                connection="felhohf4storage_STORAGE") 
# def blob_trigger(myblob: func.InputStream):
#     logging.info(f"Python blob trigger function processed blob"
#                 f"Name: {myblob.name}"
#                 f"Blob Size: {myblob.length} bytes")
#     try:
#         conn_string=os.environ['felhohf4storage_STORAGE']
#         blob_service_client = BlobServiceClient.from_connection_string(conn_string)
#         print("Blob name:")
#         print(myblob.name)
#         blob_name = myblob.name.split("/")[-1]
#         container_name = "felho-hf-container2"
#         blob_client = blob_service_client.get_blob_client(container=container_name, blob="images/" + blob_name)
        
#         blob_properties = blob_client.get_blob_properties()
#         metadata = blob_properties.metadata
#         if 'processed' in metadata and metadata['processed'] == 'true':
#             logging.info("Blob has been processed already. Skipping.")
#             return

        
#         # Download the blob data
#         data = blob_client.download_blob().readall()

#         # Convert the blob data to a NumPy array
#         image_array = np.frombuffer(data, np.uint8)
#         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
#         borderoutput = cv2.copyMakeBorder( 
#         image, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 0])


#         # Encode the resized image back to a byte array
#         success, buffer = cv2.imencode('.png', borderoutput)
#         if not success:
#             raise ValueError("Image encoding failed")

#         # Convert the byte array to a BytesIO object
#         image_bytes = io.BytesIO(buffer)

#         new_name = "bordered-" + blob_name

#         print(new_name)
#         new_blob_client = blob_service_client.get_blob_client(container=container_name, blob=new_name)
#         print(new_blob_client.blob_name)
#         new_blob_client.upload_blob(image_bytes.getvalue(), overwrite=True, metadata={'processed': 'true'})

#         logging.info(f"Python blob trigger function executed successfully."
#                     f"Name: {myblob.name}")
#     except Exception as e:
#         logging.error(f"Error: {e}")


app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="felho-hf-container2/images/{name}",
                  connection="felhohf4storage_STORAGE")
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob "
                 f"Name: {myblob.name} "
                 f"Blob Size: {myblob.length} bytes")
    try:
        # Retrieve the connection string from environment variables
        conn_string = os.environ['felhohf4storage_STORAGE']
        blob_service_client = BlobServiceClient.from_connection_string(conn_string)
        
        # Get the blob name and container name
        blob_name = myblob.name.split("/")[-1]
        container_name = "felho-hf-container2"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob="images/" + blob_name)
        
        # Check metadata to see if the blob has already been processed
        blob_properties = blob_client.get_blob_properties()
        metadata = blob_properties.metadata
        if 'processed' in metadata and metadata['processed'] == 'true':
            logging.info("Blob has been processed already. Skipping.")
            return
        
        # Download the blob data
        data = blob_client.download_blob().readall()

        # Convert the blob data to a NumPy array
        image_array = np.frombuffer(data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        thresh = 127
        im_bw = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
        
        # Add a border to the image
        borderoutput = cv2.copyMakeBorder(
            im_bw, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 0])

        # Encode the image with the border back to a byte array
        success, buffer = cv2.imencode('.png', borderoutput)
        if not success:
            raise ValueError("Image encoding failed")

        # Convert the byte array to a BytesIO object
        image_bytes = io.BytesIO(buffer.tobytes())

        # Define the new blob name
        new_name = "bordered-" + blob_name

        # Upload the new image blob with the processed metadata
        new_blob_client = blob_service_client.get_blob_client(container=container_name, blob="images/" + new_name)
        new_blob_client.upload_blob(image_bytes.getvalue(), overwrite=True, metadata={'processed': 'true'})

        logging.info(f"Python blob trigger function executed successfully. Name: {myblob.name}")
    except Exception as e:
        logging.error(f"Error: {e}")