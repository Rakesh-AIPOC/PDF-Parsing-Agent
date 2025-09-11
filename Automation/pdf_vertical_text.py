import fitz

def check_vertical_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_dict = page.get_text("dict")

        print(f"Page {page_num + 1} vertical text blocks:")
        for block in text_dict["blocks"]:
            if block['type'] != 0:
                continue

            bbox = block["bbox"]
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]

            if height > width * 3:
                
                block_text = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        block_text += span.get("text", "")
                print(f"BBox: {bbox} Text: {block_text.strip()}")
                return True
    return False

if __name__ == "__main__":
    pdf_file = r"D:\Rakesh\Study materials\PDF Parsing Agent\Utils\Sample PDF.pdf"
    check_vertical_text_blocks(pdf_file)