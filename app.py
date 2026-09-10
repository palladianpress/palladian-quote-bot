import streamlit as st
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Palladian Print Studio | Instant Quote",
    page_icon="👕",
    layout="centered"
)

# --- CUSTOM BRAND STYLING ---
st.markdown("""
    <style>
    /* Global Background & Typography */
    .stApp {
        background-color: #cc443e;
        color: #181717;
        font-family: "acumin-pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    
    /* Headers & Labels */
    h1, h2, h3, h4, p, span, label, .stMarkdown {
        color: #181717 !important;
        font-family: "acumin-pro", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    }

    /* Input Fields & Text Areas (Cream Background + Dark Text) */
    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #efebd9 !important;
        color: #181717 !important;
        border-radius: 6px !important;
        border: 1px solid #181717 !important;
        font-family: "acumin-pro", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    }

    /* Typing text color inside input boxes */
    input[type="text"], input[type="number"] {
        color: #181717 !important;
        background-color: #efebd9 !important;
    }

    /* Radio buttons and Select boxes background */
    div[role="radiogroup"] {
        background-color: transparent;
    }

    /* Quote Output Box (Cream Card) */
    .quote-box {
        background-color: #efebd9;
        border: 2px solid #181717;
        border-radius: 8px;
        padding: 24px;
        margin-top: 20px;
        color: #181717;
    }

    .quote-box p, .quote-box h3 {
        color: #181717 !important;
    }

    /* Email Button */
    .email-btn {
        display: block;
        width: 100%;
        background-color: #181717;
        color: #efebd9 !important;
        text-align: center;
        padding: 16px 20px;
        border-radius: 6px;
        font-weight: bold;
        text-decoration: none;
        margin-top: 20px;
        font-size: 16px;
        letter-spacing: 0.5px;
    }
    .email-btn:hover {
        background-color: #333333;
        color: #efebd9 !important;
    }

    /* Email Info Box Below Button */
    .email-info-box {
        text-align: center;
        margin-top: 15px;
        padding: 12px;
        background-color: rgba(239, 235, 217, 0.3);
        border-radius: 6px;
        border: 1px dashed #181717;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("PALLADIAN PRINT STUDIO")
st.caption("Instant Quote Generator — Single-Color Screen Printed T-Shirts")

st.divider()

# --- INPUT FORM ---
st.subheader("1. Select Garments")

color_option = st.radio(
    "What garment color(s) do you need?",
    ["All White Tees", "All Color Tees", "Mix of White & Color Tees"]
)

qty_white = 0
qty_color = 0

if color_option == "All White Tees":
    qty_white = st.number_input("How many White t-shirts?", min_value=1, value=10, step=1)
elif color_option == "All Color Tees":
    qty_color = st.number_input("How many Color t-shirts?", min_value=1, value=10, step=1)
else:
    col1, col2 = st.columns(2)
    with col1:
        qty_white = st.number_input("White t-shirts", min_value=0, value=5, step=1)
    with col2:
        qty_color = st.number_input("Color t-shirts", min_value=0, value=5, step=1)

total_qty = qty_white + qty_color

st.subheader("2. Artwork & File Preparation")
art_option = st.selectbox(
    "How is your design/artwork set up?",
    [
        "Print-Ready Vector Provided (£0.00)",
        "Artwork Vectorizing & File Prep (£15.00)",
        "In-House Custom Graphic Design (£25.00)"
    ]
)

# --- PRICING LOGIC ---
if total_qty > 0:
    if "Vectorizing" in art_option:
        art_fee = 15.00
        art_label = "Artwork Vectorizing & File Prep (£15.00)"
    elif "Custom Graphic" in art_option:
        art_fee = 25.00
        art_label = "In-House Custom Graphic Design (£25.00)"
    else:
        art_fee = 0.00
        art_label = "Print-Ready Vector Provided (£0.00)"

    if total_qty < 25:
        rate_white, rate_color = 6.50, 7.00
        tier_name = "Standard Rate (1–24 units total)"
    elif total_qty < 50:
        rate_white, rate_color = 6.00, 6.50
        tier_name = "Volume Discount Tier 1 (25–49 units total)"
    elif total_qty < 100:
        rate_white, rate_color = 5.50, 6.00
        tier_name = "Volume Discount Tier 2 (50–99 units total)"
    else:
        rate_white, rate_color = 5.00, 5.50
        tier_name = "Bulk Discount Rate (100+ units total)"

    subtotal_white = qty_white * rate_white
    subtotal_color = qty_color * rate_color
    garment_subtotal = subtotal_white + subtotal_color

    setup_fee = 10.00 if total_qty < 10 else 0.00
    grand_total = garment_subtotal + setup_fee + art_fee
    average_unit_price = grand_total / total_qty

    # --- BREAKDOWN OUTPUT ---
    st.divider()
    st.subheader("Your Estimated Quote")

    garment_summary = ""
    if qty_white > 0 and qty_color > 0:
        garment_summary = f"{qty_white} x White, {qty_color} x Color"
    elif qty_white > 0:
        garment_summary = f"{qty_white} x White"
    else:
        garment_summary = f"{qty_color} x Color"

    st.markdown(f"""
    <div class="quote-box">
        <p><strong>Item Spec:</strong> Gildan Heavyweight Cotton T-Shirt</p>
        <p><strong>Print Style:</strong> 1-Color Hand-Pulled Screen Print</p>
        <p><strong>Total Order Size:</strong> {total_qty} t-shirts ({garment_summary})</p>
        <p><strong>Applied Tier:</strong> {tier_name}</p>
        <p><strong>Artwork Service:</strong> {art_label}</p>
        <p><strong>Estimated Turnaround:</strong> 1 Week (5–7 Working Days)</p>
        <hr style="border: 1px solid #181717;">
        <p><strong>Garment & Print Subtotal:</strong> £{garment_subtotal:.2f}</p>
        <p><strong>Small-Order Setup Fee:</strong> £{setup_fee:.2f}</p>
        <p><strong>Design/Artwork Fee:</strong> £{art_fee:.2f}</p>
        <hr style="border: 1px solid #181717;">
        <h3 style="margin-bottom:0px; text-align:left;">TOTAL ESTIMATED PRICE: £{grand_total:.2f}</h3>
        <p><em>Average All-In Unit Price: £{average_unit_price:.2f} / tee</em></p>
    </div>
    """, unsafe_allow_html=True)

    # --- EMAIL TRIGGER SETUP ---
    email_body = (
        f"Hi Palladian Studio,\n\n"
        f"I calculated a quote on your website and would like to proceed with my order:\n\n"
        f"- Total Quantity: {total_qty} ({garment_summary})\n"
        f"- Artwork Setup: {art_label}\n"
        f"- Estimated Total: £{grand_total:.2f}\n\n"
        f"Please let me know the next steps for payment and sending over artwork files!"
    )
    
    encoded_body = urllib.parse.quote(email_body)
    mailto_url = f"mailto:palladianpressncl@gmail.com?subject=New%20Quote%20Request%20(£{grand_total:.2f})&body={encoded_body}"

    # Email Action Area
    st.markdown(f'<a href="{mailto_url}" class="email-btn">📩 Click Here to Send Quote via Email</a>', unsafe_allow_html=True)

    st.markdown("""
    <div class="email-info-box">
        <p style="margin: 0; font-size: 14px;">
            Click the button above to proceed via e-mail, or send this quote to 
            <strong>palladianpressncl@gmail.com</strong> to proceed or if you have any other questions or enquiries! :-)
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.warning("Please enter a total quantity greater than 0.")

# --- FOOTER ---
st.markdown("---")
st.caption("📍 Palladian Studio | ✉️ palladianpressncl@gmail.com")
