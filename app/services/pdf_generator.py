import os
import time
import tempfile
import httpx
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

class PDFGenerator:
    @staticmethod
    def _download_temp_image(url: str, max_retries: int = 5) -> str:
        """Download an image URL to a temp file with retries for lazy-generated images."""
        if not url:
            return None
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/*,*/*',
        }
        
        for attempt in range(max_retries):
            try:
                print(f"PDF image download attempt {attempt + 1}/{max_retries}: {url[:80]}...")
                with httpx.Client(timeout=90.0, headers=headers, follow_redirects=True) as client:
                    response = client.get(url)
                
                # If server returned an error, retry after delay
                if response.status_code >= 400:
                    print(f"  Got HTTP {response.status_code}, retrying in {3 * (attempt + 1)}s...")
                    time.sleep(3 * (attempt + 1))
                    continue
                
                content = response.content
                
                # Check content type - make sure we got an actual image
                content_type = response.headers.get('content-type', '')
                if 'image' not in content_type or len(content) < 5000:
                    print(f"  Not an image (type={content_type}, size={len(content)}), retrying...")
                    time.sleep(3 * (attempt + 1))
                    continue
                
                # Verify minimum image size (valid JPG/PNG is typically > 5KB)
                if len(content) < 5000:
                    print(f"  Image too small ({len(content)} bytes), retrying...")
                    time.sleep(3 * (attempt + 1))
                    continue
                
                # Save to temp file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                temp_path = temp_file.name
                temp_file.close()
                with open(temp_path, 'wb') as f:
                    f.write(content)
                
                print(f"  Successfully downloaded {len(content)} bytes to {temp_path}")
                return temp_path
                
            except Exception as e:
                print(f"  Download error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(3 * (attempt + 1))
                continue
        
        print(f"  Failed to download image after {max_retries} attempts")
        return None

    @staticmethod
    def generate_report(project_id: str, data: dict, output_path: str):
        # Save PDF to /tmp which is writable and reliable on Render containers
        if not output_path.startswith("/"):
            output_path = os.path.join("/tmp", output_path)
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        print("=== Starting PDF Image Downloads (Sequential) ===")
        # Download images sequentially with a tiny spacing to prevent rate limiting
        ext_path = PDFGenerator._download_temp_image(data.get("exterior_image"))
        time.sleep(0.5)
        int_path = PDFGenerator._download_temp_image(data.get("interior_image"))
        time.sleep(0.5)
        fp_path = PDFGenerator._download_temp_image(data.get("floorplan_image"))
        
        print(f"Download results: ext={ext_path is not None}, int={int_path is not None}, fp={fp_path is not None}")

        # ================= PAGE 1: OVERVIEW & SPECS =================
        c.setFillColor(HexColor('#0B0B0B'))
        c.rect(0, height - 120, width, 120, fill=1)
        c.setFillColor(HexColor('#D4AF37'))
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 70, "AI HOME DESIGNER")
        c.setFillColor(HexColor('#F5F5F5'))
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 95, "Bespoke Architectural Project Portfolio & Cost Estimation")

        c.setFillColor(HexColor('#0B0B0B'))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 160, "Project Specifications")
        c.setStrokeColor(HexColor('#D4AF37'))
        c.setLineWidth(1)
        c.line(50, height - 170, width - 50, height - 170)

        c.setFont("Helvetica", 11)
        y = height - 200
        c.drawString(50, y, f"Project Identifier: {project_id}")
        y -= 20
        c.drawString(50, y, f"Selected Style: {data.get('style', 'N/A')}")
        y -= 20
        c.drawString(50, y, f"Plot Size: {data.get('plot_size', 'N/A')} sq ft")
        y -= 20
        c.drawString(50, y, f"Project Budget: ${data.get('budget', '0.00')}")
        y -= 20
        c.drawString(50, y, f"Estimated Cost: {data.get('estimated_cost', '$0.00')}")
        y -= 20
        c.drawString(50, y, f"Sustainability Score: {data.get('sustainability_score', '85')}/100")

        y -= 30
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Financial & Material Analysis")
        c.line(50, y - 10, width - 50, y - 10)
        
        y -= 35
        c.setFont("Helvetica", 11)
        breakdown = data.get("cost_breakdown", "Base construction cost analysis.")
        words = str(breakdown).split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if len(" ".join(current_line)) > 90:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        
        for line in lines[:4]:
            c.drawString(50, y, line)
            y -= 18

        y -= 15
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Recommended Materials:")
        y -= 20
        c.setFont("Helvetica", 11)
        for mat in data.get('materials', [])[:4]:
            c.drawString(70, y, f"* {mat}")
            y -= 18

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Eco-Friendly Optimization Tips:")
        y -= 20
        c.setFont("Helvetica", 11)
        for tip in data.get('sustainability_tips', [])[:3]:
            c.drawString(70, y, f"* {tip}")
            y -= 18

        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 40, "Page 1 of 3 - Confidential Proposal generated by AI Architect Engine.")
        c.showPage()

        # ================= PAGE 2: CONCEPT PREVIEWS =================
        c.setFillColor(HexColor('#0B0B0B'))
        c.rect(0, height - 100, width, 100, fill=1)
        c.setFillColor(HexColor('#D4AF37'))
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 60, "VISUAL CONCEPT RENDERINGS")
        
        y = height - 150
        
        if ext_path and os.path.exists(ext_path):
            c.setFillColor(HexColor('#0B0B0B'))
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Exterior Architecture Concept Preview")
            y -= 10
            c.drawImage(ext_path, 50, y - 230, width=500, height=230, preserveAspectRatio=True)
            y -= 260
        else:
            c.setFillColor(HexColor('#999999'))
            c.setFont("Helvetica", 11)
            c.drawString(50, y, "[Exterior image could not be embedded - view online in the app]")
            y -= 30

        if int_path and os.path.exists(int_path):
            c.setFillColor(HexColor('#0B0B0B'))
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Interior Design & Ambient Preview")
            y -= 10
            c.drawImage(int_path, 50, y - 230, width=500, height=230, preserveAspectRatio=True)
        else:
            c.setFillColor(HexColor('#999999'))
            c.setFont("Helvetica", 11)
            c.drawString(50, y, "[Interior image could not be embedded - view online in the app]")

        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 40, "Page 2 of 3 - Confidential Proposal generated by AI Architect Engine.")
        c.showPage()

        # ================= PAGE 3: TECHNICAL BLUEPRINT =================
        c.setFillColor(HexColor('#0B0B0B'))
        c.rect(0, height - 100, width, 100, fill=1)
        c.setFillColor(HexColor('#D4AF37'))
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 60, "PHOTOREALISTIC 3D LAYOUT")

        y = height - 150

        if fp_path and os.path.exists(fp_path):
            c.setFillColor(HexColor('#0B0B0B'))
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Luxury Architectural 3D Cutaway Visualization")
            y -= 10
            c.drawImage(fp_path, 50, y - 450, width=500, height=450, preserveAspectRatio=True)
        else:
            c.setFillColor(HexColor('#999999'))
            c.setFont("Helvetica", 11)
            c.drawString(50, y, "[Floorplan image could not be embedded - view online in the app]")

        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 40, "Page 3 of 3 - Confidential Proposal generated by AI Architect Engine.")
        
        c.save()
        print(f"=== PDF saved to {output_path} ===")

        # Cleanup temp image files
        for path in [ext_path, int_path, fp_path]:
            if path and os.path.exists(path):
                try:
                    os.unlink(path)
                except Exception:
                    pass

        return output_path
