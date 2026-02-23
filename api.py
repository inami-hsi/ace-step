import os
import sys
import uvicorn

def main():
    # Set environment variables for the API server
    os.environ["ACESTEP_ENABLE_API"] = "true"
    
    # Project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 Starting ACE-Step 1.5 API Server...")
    print("Access the API docs at http://localhost:8000/docs")
    
    # Launch the official API server directly using uv run
    # This ensures it uses the project dependencies correctly.
    # We can also call the main function from acestep.api_server if preferred.
    
    from acestep.api_server import main as api_main
    
    # Pass arguments via sys.argv if needed, or let it load from env/.env
    sys.argv = [sys.argv[0], "--port", "8000", "--host", "0.0.0.0"]
    api_main()

if __name__ == "__main__":
    main()
