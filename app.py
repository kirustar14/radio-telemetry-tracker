from flask import Flask, render_template, request, redirect, url_for
import folium
import rasterio
import os
import geopandas as gpd

app = Flask(__name__)

# Ensure the uploads folder exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Route for the main index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the GeoTIFF upload page
@app.route('/uploadGeoTiff')
def upload_geo_tiff_page():
    return render_template('uploadGeoTiff.html')

@app.route('/uploadGeoTiff', methods=['POST'])
def upload_geo_tiff():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and (file.filename.endswith('.tif') or file.filename.endswith('.tiff')):
        # Save the uploaded GeoTIFF file
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        # Load the GeoTIFF image
        with rasterio.open(file_path) as src:
            band1 = src.read(1)  # Read the first band
            bounds = src.bounds

        # Calculate the map center and zoom level
        map_center = [(bounds.top + bounds.bottom) / 2, (bounds.left + bounds.right) / 2]
        zoom_level = 10  # You may need to adjust this based on your data's extent

        # Create a map centered around the GeoTIFF bounds
        map = folium.Map(location=map_center, zoom_start=zoom_level)

        # Add the GeoTIFF as an overlay
        folium.raster_layers.ImageOverlay(
            image=band1,  # Ensure this is in a format suitable for web display
            bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
            opacity=0.6,
        ).add_to(map)

        # Optionally, fit the map to the bounds of the GeoTIFF
        folium.LayerControl().add_to(map)  # Add layer controls if needed

        return render_template('map_display.html', map=map._repr_html_())

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
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Here you would typically extract the zip file and use the tiles
        # For now, we'll redirect to a placeholder
        return redirect(url_for('map_display', basemap_type='webmap'))

    return redirect(url_for('index'))

# Route to display the map with overlay options
@app.route('/mapDisplay')
def map_display():
    return render_template('map_display.html')

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
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Load the shapefile and add as overlay
        gdf = gpd.read_file(file_path)
        map = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=10)
        folium.GeoJson(gdf).add_to(map)

        return render_template('map_display.html', map=map._repr_html_())

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
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Load the GeoJSON data and add as overlay
        gdf = gpd.read_file(file_path)
        map = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=10)
        folium.GeoJson(gdf).add_to(map)

        return render_template('map_display.html', map=map._repr_html_())

    return redirect(url_for('index'))

# Route to serve the Upload Overlays page
@app.route('/uploadOverlays')
def upload_overlays_page():
    return render_template('uploadOverlays.html')


if __name__ == '__main__':
    app.run(debug=True)
