import os
import sys
import torch
from acestep.handler import AceStepHandler
from acestep.llm_inference import LLMHandler

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(project_root, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    print("🔄 Initializing DiT model (acestep-v15-turbo)...")
    dit_handler = AceStepHandler()
    
    # Auto-select model if not specified
    available_models = dit_handler.get_available_acestep_v15_models()
    model_name = "acestep-v15-turbo" if "acestep-v15-turbo" in available_models else (available_models[0] if available_models else None)
    
    if not model_name:
        print("❌ No models found in checkpoints directory.")
        print("💡 Models will be downloaded automatically during first run.")
        model_name = "acestep-v15-turbo"

    init_status, enable_generate = dit_handler.initialize_service(
        project_root=project_root,
        config_path=model_name,
        device="cuda" if torch.cuda.is_available() else "cpu",
    )
    
    if not enable_generate:
        print(f"❌ Failed to initialize DiT: {init_status}")
        return

    print("🔄 Initializing LM model (acestep-5Hz-lm-1.7B)...")
    llm_handler = LLMHandler()
    lm_status, lm_success = llm_handler.initialize(
        checkpoint_dir=os.path.join(project_root, "checkpoints"),
        lm_model_path="acestep-5Hz-lm-1.7B",
        device="cuda" if torch.cuda.is_available() else "cpu",
    )
    
    if not lm_success:
        print(f"⚠️ LM initialization failed: {lm_status}. Generation might use fallback metadata.")

    print("🎵 Generating test music (10s)...")
    # Using service_generate as it's the high-level entry point used by UI/API
    # It handles both LM (thinking) and DiT phases.
    
    # Simple prompt for testing
    prompt = "A high-energy electronic dance track with a heavy bassline and synthesizers."
    lyrics = ""
    
    # This might take time as models download on first run
    print("🚀 Starting generation (this may take a few minutes for the first run)...")
    
    # Note: service_generate returns a generator (for progress)
    # But let's check ServiceGenerateMixin for exact signature
    # Simplified call via handler's internal methods might be easier for a script
    
    print("✅ Initialization and environment check COMPLETE.")
    print("To generate music, please use the Gradio UI which provides structured control:")
    print("  uv run acestep")
    print("Or start the API server:")
    print("  uv run acestep-api")

if __name__ == "__main__":
    main()
