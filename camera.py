import requests

def capture_photo_from_ip_camera(url, filename='photo.jpg'):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        raise Exception(f"Failed to capture photo, status code: {response.status_code}")
