import os
import json
from processor import DocumentProcessor

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def main():
    processor = DocumentProcessor()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Gather all PDFs
    documents = []
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            documents.append({
                "filename": os.path.join(INPUT_DIR, filename)
            })

    if not documents:
        print("❌ No PDFs found in input directory.")
        return

    # Static persona and job for now
    input_data = {
        "documents": documents,
        "persona": {"role": "Travel Planner"},
        "job_to_be_done": {"task": "Plan a trip to Japan including major destinations and accommodations"}
    }

    try:
        result = processor.process_documents(input_data)

        # Write ONE output file for the batch
        output_path = os.path.join(OUTPUT_DIR, "challenge1b_output.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ Output written to: {output_path}")
    except Exception as e:
        print(f"❌ Error during batch processing: {e}")

if __name__ == "__main__":
    main()
