import argparse
import sys
import os
import json

# Add project root to sys.path to allow running from any directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.core import extract_structured_data, ask_question, summarize_form, analyze_multiple_forms

def main():
    parser = argparse.ArgumentParser(
        description="Intelligent Form Agent - CLI Tool to process and analyze forms using Gemini API."
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Agent commands")
    
    # Subcommand: extract
    parser_extract = subparsers.add_parser("extract", help="Extract structured key-value data in JSON format from a form.")
    parser_extract.add_argument("file_path", type=str, help="Path to the form file (Image or PDF)")
    parser_extract.add_argument("--key", type=str, default=None, help="Gemini API Key (optional, defaults to GEMINI_API_KEY env var)")
    
    # Subcommand: ask
    parser_ask = subparsers.add_parser("ask", help="Ask a question about a specific form.")
    parser_ask.add_argument("file_path", type=str, help="Path to the form file (Image or PDF)")
    parser_ask.add_argument("question", type=str, help="The question to ask")
    parser_ask.add_argument("--key", type=str, default=None, help="Gemini API Key (optional)")
    
    # Subcommand: summarize
    parser_summarize = subparsers.add_parser("summarize", help="Generate a markdown summary of a form.")
    parser_summarize.add_argument("file_path", type=str, help="Path to the form file (Image or PDF)")
    parser_summarize.add_argument("--key", type=str, default=None, help="Gemini API Key (optional)")
    
    # Subcommand: analyze-multi
    parser_multi = subparsers.add_parser("analyze-multi", help="Analyze multiple forms together with a holistic query.")
    parser_multi.add_argument("files", type=str, nargs="+", help="Paths to the form files (Images or PDFs)")
    parser_multi.add_argument("--query", type=str, required=True, help="The comparative or holistic question/query")
    parser_multi.add_argument("--key", type=str, default=None, help="Gemini API Key (optional)")
    
    args = parser.parse_args()
    
    # Verify file paths exist
    if hasattr(args, "file_path"):
        if not os.path.exists(args.file_path):
            print(f"Error: File not found: {args.file_path}", file=sys.stderr)
            sys.exit(1)
            
    if hasattr(args, "files"):
        for f in args.files:
            if not os.path.exists(f):
                print(f"Error: File not found: {f}", file=sys.stderr)
                sys.exit(1)
                
    try:
        if args.command == "extract":
            data = extract_structured_data(args.file_path, api_key=args.key)
            print(json.dumps(data, indent=2))
            
        elif args.command == "ask":
            answer = ask_question(args.file_path, args.question, api_key=args.key)
            print(answer)
            
        elif args.command == "summarize":
            summary = summarize_form(args.file_path, api_key=args.key)
            print(summary)
            
        elif args.command == "analyze-multi":
            analysis = analyze_multiple_forms(args.files, args.query, api_key=args.key)
            print(analysis)
            
    except Exception as e:
        print(f"Error executing command '{args.command}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
