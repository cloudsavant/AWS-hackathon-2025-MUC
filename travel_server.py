#!/usr/bin/env python3
"""
Simple web server to serve the travel planner UI and handle agentcore commands
"""

import subprocess
import json
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TravelPlannerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/travel_planner_ui.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/generate-plan':
            self.handle_generate_plan()
        else:
            self.send_error(404)
    
    def handle_generate_plan(self):
        try:
            # Get content length and read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse the JSON data
            request_data = json.loads(post_data)
            prompt = request_data.get('prompt', '')
            
            if not prompt:
                self.send_json_error('No prompt provided', 400)
                return
            
            logger.info("Executing agentcore with prompt: %s", prompt)
            
            # Execute the agentcore command
            cmd = ['agentcore', 'invoke', json.dumps({"prompt": prompt})]
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,  # 2 minute timeout
                    cwd=os.getcwd()
                )
                
                if result.returncode != 0:
                    logger.error(f"agentcore command failed: {result.stderr}")
                    self.send_json_error(f"Agent execution failed: {result.stderr}", 500)
                    return
                
                # Parse the output as JSON
                try:
                    logger.info("agentcore raw output: %s", result.stdout)
                    
                    # First try to parse as direct JSON
                    try:
                        response_data = json.loads(result.stdout)
                        logger.info("Parsed response as direct JSON successfully")
                        self.send_json_response(response_data)
                        return
                    except json.JSONDecodeError:
                        pass
                    
                    # Extract JSON from agentcore decorated output
                    # Look for "Response:" followed by JSON
                    import re
                    
                    # Try to find JSON after "Response:" marker
                    response_match = re.search(r'Response:\s*(\{.*\})', result.stdout, re.DOTALL)
                    if response_match:
                        json_str = response_match.group(1).strip()
                        try:
                            response_data = json.loads(json_str)
                            logger.info("Successfully extracted JSON from agentcore response")
                            self.send_json_response(response_data)
                            return
                        except json.JSONDecodeError:
                            pass
                    
                    # Fallback: Look for any JSON-like structure
                    json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result.stdout, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        try:
                            response_data = json.loads(json_str)
                            logger.info("Successfully extracted JSON from mixed output")
                            self.send_json_response(response_data)
                            return
                        except json.JSONDecodeError:
                            pass
                    
                    # If all else fails, return error
                    logger.error("Could not extract valid JSON from agentcore output")
                    self.send_json_error("Could not parse JSON from agent response", 500)
                    
                except Exception as e:
                    logger.error("Unexpected error parsing agentcore output: %s", e)
                    self.send_json_error("Error parsing agent response: " + str(e), 500)
                
            except subprocess.TimeoutExpired:
                logger.error("agentcore command timed out")
                self.send_json_error("Request timed out", 504)
            except FileNotFoundError:
                logger.error("agentcore command not found")
                self.send_json_error("agentcore command not found. Please ensure it's installed and in PATH.", 500)
            except subprocess.SubprocessError as e:
                logger.error("Subprocess error executing agentcore: %s", e)
                self.send_json_error("Error executing agentcore: " + str(e), 500)
                
        except json.JSONDecodeError:
            self.send_json_error('Invalid JSON in request', 400)
        except (IOError, OSError) as e:
            logger.error("I/O error handling request: %s", e)
            self.send_json_error('Server error: ' + str(e), 500)
    
    def send_json_response(self, data):
        response = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response)
    
    def send_json_error(self, message, status_code):
        error_data = {'error': message}
        response = json.dumps(error_data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8080):
    """Run the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TravelPlannerHandler)
    
    print(f"🌍 Travel Planner Server running at http://localhost:{port}")
    print("📂 Serving files from current directory")
    print("🚀 Open your browser and navigate to the URL above")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)