from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with a secure key in production

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        dataset = request.form.get('dataset')
        variable = request.form.get('variable')
        extraction_type = request.form.get('extraction_type')
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        uploaded_file = request.files.get('shapefile')

        # For demonstration, flash the received inputs
        flash(f"Dataset: {dataset}, Variable: {variable}, Extraction: {extraction_type}")
        if extraction_type == "site_specific" and lat and lon:
            flash(f"Site-specific extraction at Latitude: {lat}, Longitude: {lon}")
        if extraction_type == "location_based":
            flash("Location-based extraction selected.")
            if uploaded_file:
                flash("A shapefile/GeoJSON was uploaded.")
            # (Optionally, you can capture drawn polygon data via JavaScript and pass it to the backend)

        # Process the data as needed...
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
