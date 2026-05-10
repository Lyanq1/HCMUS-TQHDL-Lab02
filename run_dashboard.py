import sys
from pathlib import Path

# Add dashboard to path
sys.path.insert(0, str(Path(__file__).parent / 'dashboard'))

from dashboard.app import app

if __name__ == '__main__':
    print("Starting TIKI Fashion Analytics Dashboard...")
    print("Open browser at: http://localhost:8050")
    app.run(debug=True, port=8050)
