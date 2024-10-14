from flask import Flask, render_template, request, redirect, url_for
import folium
import rasterio
import os
import geopandas as gpd

app = Flask(__name__)

# Route for the main index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the GeoTIFF upload page
@app.route('/uploadGeoTiff')
def upload_geo_tiff_page():
    return render_template('uploadGeoTiff.html')

# Route to handle the uploaded GeoTIFF file
@app.route('/uploadGeoTiff', methods=['POST'])
def upload_geo_tiff():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and (file.filename.endswith('.tif') or file.filename.endswith('.tiff')):
        # Save the uploaded GeoTIFF file
        file_path = os.path.join('uploads', file.filename)  # Ensure 'uploads' folder exists
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

# Route to serve the Webmap upload page
@app.route('/uploadWebmap')
def upload_webmap_page():
    return render_template('uploadWebMap.html')

# Route to handle the uploaded webmap tiles
@app.route('/upload_tiles', methods=['POST'])
def upload_tiles():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and file.filename.endswith('.zip'):
        # Save the uploaded webmap tiles
        file_path = os.path.join('uploads', file.filename)  # Ensure 'uploads' folder exists
        file.save(file_path)

        # Here, you would typically extract the zip file and use the tiles
        return redirect(url_for('index'))

    return redirect(url_for('index'))

# Route to serve the Shapefile upload page
@app.route('/uploadShapefile')
def upload_shapefile_page():
    return render_template('uploadShapefile.html')

# Route to handle the uploaded Shapefile
@app.route('/uploadShapefile', methods=['POST'])
def upload_shapefile():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and file.filename.endswith('.zip'):
        # Save the uploaded shapefile (in zip format)
        file_path = os.path.join('uploads', file.filename)  # Ensure 'uploads' folder exists
        file.save(file_path)

        # Here, you would typically extract the zip file and read the shapefile
        # For demonstration, we just redirect to index
        return redirect(url_for('index'))

    return redirect(url_for('index'))

# Route to serve the GeoJSON upload page
@app.route('/uploadGeoJSON')
def upload_geojson_page():
    return render_template('uploadGeoJSON.html')

# Route to handle the uploaded GeoJSON file
@app.route('/uploadGeoJSON', methods=['POST'])
def upload_geojson():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and (file.filename.endswith('.geojson') or file.filename.endswith('.json')):
        # Save the uploaded GeoJSON file
        file_path = os.path.join('uploads', file.filename)  # Ensure 'uploads' folder exists
        file.save(file_path)

        # Load the GeoJSON data using GeoPandas
        gdf = gpd.read_file(file_path)

        # Create a map centered around the GeoJSON bounds
        map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
        map = folium.Map(location=map_center, zoom_start=10)

        # Add the GeoJSON to the map
        folium.GeoJson(gdf).add_to(map)

        return map._repr_html_()  # Render the map

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
