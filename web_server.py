#!/usr/bin/env python3
"""Simple web server for the ADK Web interface."""

import http.server
import socketserver
import os
from pathlib import Path

# Configuration
PORT = 8080
WEB_DIR = Path(__file__).parent / "web"


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with CORS support."""

    def end_headers(self):
        """Add CORS headers to allow API requests."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests."""
        self.send_response(200)
        self.end_headers()


def main():
    """Start the web server."""
    # Change to web directory
    os.chdir(WEB_DIR)

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("🌐 ADK Web Interface Server")
        print("=" * 60)
        print(f"\n✅ Server running at: http://localhost:{PORT}")
        print(f"📁 Serving files from: {WEB_DIR}")
        print("\n🚀 Open your browser and visit:")
        print(f"   http://localhost:{PORT}")
        print("\n⚠️  Make sure your agents are running on ports 8000-8003")
        print("   Run: ./scripts/start_all_agents.sh")
        print("\n🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down server...")
            httpd.shutdown()


if __name__ == "__main__":
    main()


