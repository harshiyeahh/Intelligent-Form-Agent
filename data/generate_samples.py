import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size=14, bold=False):
    """Attempt to load Arial, otherwise load default font."""
    font_names = ["arialbd.ttf" if bold else "arial.ttf", "calibrib.ttf" if bold else "calibri.ttf", "courbd.ttf" if bold else "cour.ttf"]
    font_paths = [os.path.join("C:\\Windows\\Fonts", name) for name in font_names]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_invoice():
    # Dimensions: 800 x 1000
    img = Image.new("RGB", (800, 1000), color="white")
    draw = ImageDraw.Draw(img)
    
    # Fonts
    title_font = get_font(28, bold=True)
    header_font = get_font(16, bold=True)
    body_bold = get_font(13, bold=True)
    body_font = get_font(13, bold=False)
    small_font = get_font(11, bold=False)
    
    # Background accents
    draw.rectangle([0, 0, 800, 15], fill="#1e3d59") # Dark blue bar at top
    draw.rectangle([0, 985, 800, 1000], fill="#17b978") # Green bar at bottom
    
    # Title / Branding
    draw.text((50, 40), "APEX CLOUD SERVICES LLC", fill="#1e3d59", font=title_font)
    draw.text((50, 75), "100 Innovation Way, Tech District\nSan Francisco, CA 94105\nsupport@apexcloud.com", fill="#555555", font=small_font)
    
    # Invoice Title (Right side)
    draw.text((550, 40), "INVOICE", fill="#17b978", font=title_font)
    
    # Invoice Metadata
    draw.text((550, 80), "Invoice #: INV-2026-0891\nDate: May 15, 2026\nDue Date: June 15, 2026", fill="#333333", font=body_font)
    
    # Line divider
    draw.line([50, 150, 750, 150], fill="#cccccc", width=1)
    
    # Bill To / Details
    draw.text((50, 170), "BILL TO:", fill="#1e3d59", font=header_font)
    draw.text((50, 195), "Global Tech Enterprises\nAttn: Accounts Payable\n500 Enterprise Blvd, Suite 10\nAustin, TX 78701", fill="#333333", font=body_font)
    
    # Payment Terms
    draw.text((550, 170), "PAYMENT TERMS:", fill="#1e3d59", font=header_font)
    draw.text((550, 195), "Net 30\nBank Transfer", fill="#333333", font=body_font)
    
    # Table Header
    draw.rectangle([50, 290, 750, 320], fill="#1e3d59")
    draw.text((60, 298), "Description", fill="white", font=body_bold)
    draw.text((450, 298), "Quantity", fill="white", font=body_bold)
    draw.text((550, 298), "Unit Price", fill="white", font=body_bold)
    draw.text((660, 298), "Total", fill="white", font=body_bold)
    
    # Table Content
    items = [
        ("Cloud Hosting - Pro Instance (1 Month)", "1", "$450.00", "$450.00"),
        ("Database Backup Storage (500GB)", "1", "$50.00", "$50.00"),
        ("Managed Security Services", "1", "$150.00", "$150.00"),
    ]
    
    y = 330
    for desc, qty, price, total in items:
        draw.text((60, y), desc, fill="#333333", font=body_font)
        draw.text((450, y), qty, fill="#333333", font=body_font)
        draw.text((550, y), price, fill="#333333", font=body_font)
        draw.text((660, y), total, fill="#333333", font=body_font)
        draw.line([50, y+25, 750, y+25], fill="#eeeeee", width=1)
        y += 35
        
    # Totals
    ty = y + 10
    draw.text((520, ty), "Subtotal:", fill="#555555", font=body_font)
    draw.text((660, ty), "$650.00", fill="#333333", font=body_font)
    
    draw.text((520, ty+25), "Tax (8.5%):", fill="#555555", font=body_font)
    draw.text((660, ty+25), "$55.25", fill="#333333", font=body_font)
    
    # Grand Total line
    draw.rectangle([500, ty+50, 750, ty+52], fill="#1e3d59")
    draw.text((520, ty+60), "Total Amount Due:", fill="#1e3d59", font=body_bold)
    draw.text((660, ty+60), "$705.25", fill="#1e3d59", font=title_font)
    
    # Notes / Footer
    draw.text((50, ty+60), "NOTES & INSTRUCTIONS:", fill="#1e3d59", font=body_bold)
    draw.text((50, ty+80), "Thank you for your business!\nPlease send payments via bank transfer\nto account ending in 9876.\nFor inquiries, contact billing@apexcloud.com", fill="#555555", font=small_font)
    
    os.makedirs("data", exist_ok=True)
    img.save("data/sample_invoice.png")
    print("Created data/sample_invoice.png")

def create_medical():
    img = Image.new("RGB", (800, 1000), color="white")
    draw = ImageDraw.Draw(img)
    
    # Fonts
    title_font = get_font(24, bold=True)
    header_font = get_font(15, bold=True)
    body_bold = get_font(13, bold=True)
    body_font = get_font(13, bold=False)
    small_font = get_font(11, bold=False)
    
    # Branding Header
    draw.rectangle([0, 0, 800, 80], fill="#e8f4f8")
    draw.text((40, 25), "VALLEY FAMILY MEDICAL CENTER", fill="#005f73", font=title_font)
    
    # Form Title
    draw.text((40, 100), "PATIENT MEDICAL INTAKE FORM", fill="#333333", font=header_font)
    draw.text((40, 120), "Please complete all sections accurately to assist our clinical team.", fill="#666666", font=small_font)
    
    # Section 1: Patient Information
    draw.rectangle([40, 150, 760, 175], fill="#005f73")
    draw.text((50, 155), "1. Patient Personal Details", fill="white", font=body_bold)
    
    # Personal Info Fields
    draw.text((50, 190), "Full Name: Jane Doe", fill="#333333", font=body_font)
    draw.text((400, 190), "Date of Birth: October 12, 1988", fill="#333333", font=body_font)
    
    draw.text((50, 225), "Phone: 555-019-2834", fill="#333333", font=body_font)
    draw.text((400, 225), "Email: jane.doe@email.com", fill="#333333", font=body_font)
    
    draw.text((50, 260), "Home Address: 123 Maple Street, Springfield, IL 62704", fill="#333333", font=body_font)
    
    # Section 2: Medical History
    draw.rectangle([40, 310, 760, 335], fill="#005f73")
    draw.text((50, 315), "2. Medical History Checklist", fill="white", font=body_bold)
    
    # Checkboxes (drawn)
    def draw_checkbox(x, y, label, checked):
        draw.rectangle([x, y, x+15, y+15], outline="#333333", width=1)
        if checked:
            draw.line([x+2, y+7, x+6, y+12], fill="#005f73", width=2)
            draw.line([x+6, y+12, x+13, y+3], fill="#005f73", width=2)
        draw.text((x+25, y-1), label, fill="#333333", font=body_font)
        
    draw_checkbox(50, 360, "Hypertension (High Blood Pressure)", True)
    draw_checkbox(400, 360, "Diabetes Type I/II", False)
    
    draw_checkbox(50, 395, "Asthma / Respiratory Conditions", True)
    draw_checkbox(400, 395, "Heart Disease", False)
    
    draw_checkbox(50, 430, "Thyroid Disorder", False)
    draw_checkbox(400, 430, "Kidney / Liver Disease", False)
    
    # Section 3: Allergies & Medications
    draw.rectangle([40, 480, 760, 505], fill="#005f73")
    draw.text((50, 485), "3. Allergies & Current Medications", fill="white", font=body_bold)
    
    draw.text((50, 525), "Known Drug or Food Allergies:", fill="#005f73", font=body_bold)
    draw.text((50, 545), "Penicillin, Peanuts (Causes mild hives and swelling)", fill="#333333", font=body_font)
    
    draw.text((50, 590), "Current Daily Medications & Dosages:", fill="#005f73", font=body_bold)
    draw.text((50, 615), "1. Albuterol inhaler (90 mcg) - used as needed for asthma symptoms.\n2. Multivitamin - 1 tablet daily.", fill="#333333", font=body_font)
    
    # Section 4: Emergency Contact & Consent
    draw.rectangle([40, 680, 760, 705], fill="#005f73")
    draw.text((50, 685), "4. Emergency Contact & Signature", fill="white", font=body_bold)
    
    draw.text((50, 725), "Emergency Contact: John Doe (Spouse)", fill="#333333", font=body_font)
    draw.text((400, 725), "Relationship Phone: 555-019-2835", fill="#333333", font=body_font)
    
    # Signature box
    draw.rectangle([40, 780, 760, 930], outline="#cccccc", width=1)
    draw.text((60, 800), "I certify that the medical history information provided here is true and correct to the\nbest of my knowledge. I consent to medical examination and treatment.", fill="#555555", font=small_font)
    
    # Signature line
    draw.line([60, 890, 400, 890], fill="#333333", width=1)
    draw.text((60, 895), "Patient Signature", fill="#666666", font=small_font)
    # Simulated handwritten signature
    signature_font = get_font(20, bold=False)
    draw.text((80, 860), "Jane Doe", fill="#1e3d59", font=signature_font)
    
    draw.line([450, 890, 740, 890], fill="#333333", width=1)
    draw.text((450, 895), "Date", fill="#666666", font=small_font)
    draw.text((450, 865), "May 18, 2026", fill="#333333", font=body_font)
    
    os.makedirs("data", exist_ok=True)
    img.save("data/sample_medical.png")
    print("Created data/sample_medical.png")

def create_rental():
    img = Image.new("RGB", (800, 1000), color="white")
    draw = ImageDraw.Draw(img)
    
    # Fonts
    title_font = get_font(22, bold=True)
    header_font = get_font(14, bold=True)
    body_bold = get_font(12, bold=True)
    body_font = get_font(12, bold=False)
    small_font = get_font(10, bold=False)
    
    # Header
    draw.rectangle([0, 0, 800, 10], fill="#8b5a2b") # Brown border
    draw.text((50, 40), "RESIDENTIAL LEASE AGREEMENT", fill="#8b5a2b", font=title_font)
    draw.line([50, 75, 750, 75], fill="#cccccc", width=1)
    
    # Intro
    intro_text = (
        "This Lease Agreement (the 'Agreement') is entered into and made effective as of May 1, 2026,\n"
        "by and between the Landlord and the Tenant named below. The parties agree to the following terms:"
    )
    draw.text((50, 95), intro_text, fill="#333333", font=body_font)
    
    # Part 1: Parties and Property
    draw.text((50, 150), "1. PARTIES AND PROPERTY", fill="#8b5a2b", font=header_font)
    draw.line([50, 168, 750, 168], fill="#8b5a2b", width=1)
    
    draw.text((50, 185), "Landlord:", fill="#333333", font=body_bold)
    draw.text((150, 185), "Robert Vance (Vance Properties LLC)", fill="#333333", font=body_font)
    
    draw.text((50, 210), "Tenant:", fill="#333333", font=body_bold)
    draw.text((150, 210), "Alice Cooper", fill="#333333", font=body_font)
    
    draw.text((50, 235), "Property Address:", fill="#333333", font=body_bold)
    draw.text((170, 235), "742 Evergreen Terrace, Springfield, IL 62704", fill="#333333", font=body_font)
    
    # Part 2: Terms and Payments
    draw.text((50, 280), "2. TERM AND PAYMENTS", fill="#8b5a2b", font=header_font)
    draw.line([50, 298, 750, 298], fill="#8b5a2b", width=1)
    
    draw.text((50, 315), "Lease Term:", fill="#333333", font=body_bold)
    draw.text((160, 315), "12 Months (Commencing June 1, 2026, and ending May 31, 2027)", fill="#333333", font=body_font)
    
    draw.text((50, 340), "Monthly Rent:", fill="#333333", font=body_bold)
    draw.text((160, 340), "$1,800.00 (Due on the 1st day of each calendar month)", fill="#333333", font=body_font)
    
    draw.text((50, 365), "Security Deposit:", fill="#333333", font=body_bold)
    draw.text((160, 365), "$2,000.00 (Refundable at lease end minus damages)", fill="#333333", font=body_font)
    
    draw.text((50, 390), "Late Fee:", fill="#333333", font=body_bold)
    draw.text((160, 390), "$50.00 for rent payments received after the 5th day of the month", fill="#333333", font=body_font)
    
    # Part 3: Utilities and Rules
    draw.text((50, 440), "3. UTILITIES AND MAINTENANCE", fill="#8b5a2b", font=header_font)
    draw.line([50, 458, 750, 458], fill="#8b5a2b", width=1)
    
    utility_text = (
        "- Tenant is responsible for electricity, gas, and water services.\n"
        "- Landlord is responsible for trash collection, high-speed fiber internet, and lawn care.\n"
        "- Tenant agrees to maintain the property in a clean and sanitary condition.\n"
        "- No pets are allowed on the premises without written consent from the Landlord.\n"
        "- Subletting the property is strictly prohibited."
    )
    draw.text((50, 475), utility_text, fill="#333333", font=body_font)
    
    # Part 4: Signatures
    draw.text((50, 600), "4. SIGNATURES AND ACKNOWLEDGMENT", fill="#8b5a2b", font=header_font)
    draw.line([50, 618, 750, 618], fill="#8b5a2b", width=1)
    
    signature_disclaimer = (
        "By signing below, both Landlord and Tenant acknowledge that they have read, understood,\n"
        "and agreed to comply with all terms and conditions of this lease agreement."
    )
    draw.text((50, 635), signature_disclaimer, fill="#555555", font=small_font)
    
    # Landlord Signature
    draw.line([50, 750, 350, 750], fill="#333333", width=1)
    draw.text((50, 755), "Landlord Signature", fill="#666666", font=small_font)
    draw.text((50, 730), "Robert Vance (Vance Properties LLC)", fill="#333333", font=body_font)
    # Simulated script signature
    sig_font = get_font(18, bold=False)
    draw.text((80, 705), "Robert Vance", fill="#4b2e1e", font=sig_font)
    draw.text((280, 730), "Date: May 2, 2026", fill="#666666", font=small_font)
    
    # Tenant Signature
    draw.line([400, 750, 700, 750], fill="#333333", width=1)
    draw.text((400, 755), "Tenant Signature", fill="#666666", font=small_font)
    draw.text((400, 730), "Alice Cooper", fill="#333333", font=body_font)
    # Simulated script signature
    draw.text((430, 705), "Alice Cooper", fill="#4b2e1e", font=sig_font)
    draw.text((630, 730), "Date: May 1, 2026", fill="#666666", font=small_font)
    
    # Bottom accent
    draw.rectangle([0, 990, 800, 1000], fill="#8b5a2b")
    
    os.makedirs("data", exist_ok=True)
    img.save("data/sample_rental.png")
    print("Created data/sample_rental.png")

if __name__ == "__main__":
    create_invoice()
    create_medical()
    create_rental()
