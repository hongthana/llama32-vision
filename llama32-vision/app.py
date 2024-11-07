from PIL import Image
import base64
import io
import ollama
import gradio as gr
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime

console = Console()

def image_to_base64(image):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Converting image to base64...", total=None)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return img_base64

def analyze_image(image, prompt):
    # Log timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"\n[bold cyan]New Analysis Request at {timestamp}[/bold cyan]")
    
    # Log image details
    console.print(Panel.fit(
        f"Image Size: {image.size}\n"
        f"Image Mode: {image.mode}",
        title="Image Details"
    ))
    
    # Convert the image to base64
    base64_image = image_to_base64(image)
    
    # Use Ollama to analyze the image
    response = ollama.chat(
        model="x/llama3.2-vision:latest",
        messages=[{
          "role": "user",
          "content": prompt,
          "images": [base64_image]
        }],
    )
    
    # Extract the model's response
    result = response['message']['content'].strip()
    
    # Format the response as markdown
    formatted_result = f"""
# Analysis Result

{result}
"""
    
    # Print to CLI
    print("\n[bold blue]Prompt:[/bold blue]", prompt)
    print("[bold green]Response:[/bold green]", result)
    print("-" * 50)
    
    return formatted_result

# Create Gradio interface
demo = gr.Interface(
    fn=analyze_image,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Textbox(
            lines=2, 
            placeholder="Enter your prompt here...", 
            label="Prompt",
            value="Describe this image?"
        )
    ],
    outputs=gr.Markdown(label="Model Response"),
    title="Image Analysis with Llama 3.2-Vision",
    description="Upload an image and enter a prompt to analyze it."
)

# Launch the interface
if __name__ == "__main__":
    print("[bold purple]Starting Llama 3.2 Vision Interface[/bold purple]")
    print("[yellow]Access the web interface at the URL shown below[/yellow]")
    demo.launch()