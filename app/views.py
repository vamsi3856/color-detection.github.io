from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ImageSerializer
import cv2
import numpy as np
from sklearn.cluster import KMeans
from django.shortcuts import render


@api_view(['GET', 'POST'])
def detect_colors(request, num_colors=10):
    if request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image_file = serializer.validated_data['image']
            image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
            image, pixels = preprocess_image(image)
            colors = quantize_colors(pixels, num_colors)
            color_names = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']
            color_values = get_color_values(colors)
            response = {name: list(value) for name, value in zip(color_names, color_values)}
            return Response(response)
        else:
            return Response(serializer.errors, status=400)
    else:
        return render(request, 'upload_image.html')
def preprocess_image(image):
    # Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Reshape the image to a 2D array of pixels
    pixels = image.reshape(-1, 3)
    # Convert the pixels to float type
    pixels = pixels.astype(float)
    # Normalize the pixel values
    pixels /= 255.0
    return image, pixels

def quantize_colors(pixels, num_colors):
    # Apply K-means clustering to identify the dominant colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    # Get the RGB values of the cluster centers
    colors = kmeans.cluster_centers_
    # Scale the RGB values back to the range of 0-255
    colors *= 255.0
    colors = colors.round().astype(int)
    return colors

def get_color_values(colors):
    # Convert the colors to a list of tuples
    color_values = colors.tolist()
    # Convert the color values to integers
    color_values = [[int(value) for value in color] for color in color_values]
    return color_values



