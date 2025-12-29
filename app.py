from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from generate_rti import generate_filled_rti
import os
import time

app = Flask(__name__)
# Enable CORS for Vercel frontend
CORS(app, resources={r"/*": {"origins": "*"}})

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "RTI Application Generator",
        "version": "1.0.0"
    })


@app.route("/api/generate-rti", methods=["POST"])
def generate_rti():
    """Generate RTI PDF from JSON data"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["applicant_name", "guardian_name", "address", "mobile"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }), 400
        
        # Generate unique filename
        filename = f"rti_application_{int(time.time())}.pdf"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        # Generate the PDF
        generate_filled_rti(data, output_path)
        
        # Send the file
        return send_file(
            output_path,
            as_attachment=True,
            download_name="NyaySetu_RTI_Application.pdf",
            mimetype="application/pdf"
        )
        
    except Exception as e:
        print(f"Error generating RTI PDF: {str(e)}")
        return jsonify({
            "error": "Failed to generate RTI PDF",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    # Use environment port or default to 5001
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
