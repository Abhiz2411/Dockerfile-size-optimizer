import os
import sys
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax

# Load environment variables from .env file
load_dotenv()

class DockerfileOptimizer:
    def __init__(self):
        """
        Initialize the Dockerfile Optimizer
        Loads API key from environment variables
        """
        self.console = Console()
        
        # API Key configuration from .env
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            self.console.print("[bold red]Error:[/] No OpenAI API key found in .env file.")
            self.console.print("Please add OPENAI_API_KEY=your_api_key to your .env file")
            sys.exit(1)
        
        # Configure OpenAI client with minimal arguments
        try:
            self.client = OpenAI(api_key=self.api_key)
        except TypeError:
            # Fallback for potential library compatibility issues
            self.client = OpenAI(api_key=self.api_key, base_url=None, timeout=None)

    def read_dockerfile(self, filepath=None):
        """
        Read Dockerfile content from file or stdin
        
        Args:
            filepath (str, optional): Path to Dockerfile
        
        Returns:
            str: Dockerfile content
        """
        try:
            if filepath:
                with open(filepath, 'r') as file:
                    return file.read()
            else:
                # Read from stdin
                self.console.print("[yellow]Paste your Dockerfile content (press Ctrl+D when finished):[/]")
                return sys.stdin.read()
        except FileNotFoundError:
            self.console.print(f"[bold red]Error:[/] Dockerfile not found at {filepath}")
            sys.exit(1)
        except Exception as e:
            self.console.print(f"[bold red]Error reading Dockerfile:[/] {e}")
            sys.exit(1)

    def optimize_dockerfile(self, dockerfile_content):
        """
        Analyze and optimize Dockerfile using OpenAI
        
        Args:
            dockerfile_content (str): Dockerfile content
        
        Returns:
            str: Optimization results
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """
                        You are an expert Docker image optimizer. 
                        Analyze Dockerfiles and provide:
                        1. Specific, actionable optimization suggestions
                        2. Explanation of potential performance/size improvements
                        3. Best practices recommendations
                        4. Estimate potential image size reduction
                        Format response in clear, concise markdown with:
                        - Clear headings
                        - Bullet points for each suggestion
                        - Estimated size reduction percentage
                        """
                    },
                    {
                        "role": "user", 
                        "content": f"Analyze this Dockerfile and provide comprehensive optimization suggestions:\n{dockerfile_content}"
                    }
                ],
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            self.console.print(f"[bold red]OpenAI API Error:[/] {e}")
            sys.exit(1)

    def display_results(self, dockerfile_content, optimization_results):
        """
        Display optimization results with rich formatting
        
        Args:
            dockerfile_content (str): Original Dockerfile
            optimization_results (str): Optimization suggestions
        """
        # Original Dockerfile panel
        self.console.print(Panel(
            Syntax(dockerfile_content, "dockerfile", theme="monokai"),
            title="[bold blue]Original Dockerfile[/]",
            border_style="cyan"
        ))

        # Optimization suggestions panel
        self.console.print(Panel(
            Markdown(optimization_results),
            title="[bold green]Optimization Suggestions[/]",
            border_style="green"
        ))

    def run(self, filepath=None):
        """
        Main application runner
        
        Args:
            filepath (str, optional): Path to Dockerfile
        """
        # Read Dockerfile
        dockerfile_content = self.read_dockerfile(filepath)

        # Optimize and get suggestions
        optimization_results = self.optimize_dockerfile(dockerfile_content)

        # Display results
        self.display_results(dockerfile_content, optimization_results)

def main():
    parser = argparse.ArgumentParser(description="Dockerfile Optimization CLI")
    parser.add_argument(
        'dockerfile', 
        nargs='?', 
        help='Path to Dockerfile (optional, will read from stdin if not provided)'
    )
    
    args = parser.parse_args()

    # Initialize and run optimizer
    optimizer = DockerfileOptimizer()
    optimizer.run(args.dockerfile)

if __name__ == "__main__":
    main()