from flask import Flask, render_template, request, redirect, url_for
import folium
import rasterio
import os

app = Flask(__name__)

# Route for the upload page
@app.route('/')
def index():
    return render_template('upload.html')  # Assuming your HTML is saved as upload.html

# Route to handle the uploaded file
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and (file.filename.endswith('.tif') or file.filename.endswith('.tiff')):
        # Save the uploaded file
        file_path = os.path.join('uploads', file.filename)  # Save to an 'uploads' folder
        file.save(file_path)
        
        # Load the GeoTIFF image
        with rasterio.open(file_path) as src:
            band1 = src.read(1)
            bounds = src.bounds

        # Create a map centered around the GeoTIFF bounds
        map_center = [(bounds.top + bounds.bottom) / 2, (bounds.left + bounds.right) / 2]
        map = folium.Map(location=map_center, zoom_start=10)

        # Add the GeoTIFF as an overlay
        folium.raster_layers.ImageOverlay(
            image=band1,  # You may need to convert this to a proper format for the overlay
            bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
            opacity=0.6,
        ).add_to(map)

        return map._repr_html_()  # Render the map

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
