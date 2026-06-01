"""
Theme management for FitDuel
Light and Dark themes
"""

LIGHT_THEME = {
    "name": "light",
    "bg": "#F4F7F6",
    "bg_secondary": "#FFFFFF",
    "card_bg": "#FFFFFF",
    "card_gradient": "linear-gradient(135deg, #FFFFFF 0%, #F4F7F6 100%)",
    "text_primary": "#1F2937",
    "text_secondary": "#6B7280",
    "primary": "#10B981",
    "primary_dark": "#059669",
    "button_bg": None,
    "button_hover": None,
    "action": "#F59E0B",
    "warning": "#FF6B6B",
    "border": "#E5E7EB",
    "input_bg": "#F4F7F6",
    "shadow": "0 4px 24px rgba(16, 185, 129, 0.08), 0 2px 8px rgba(31, 41, 55, 0.06)",
    "plotly_template": "plotly_white",
}

DARK_THEME = {
    "name": "dark",
    "bg": "#0F172A",
    "bg_secondary": "#1E293B",
    "card_bg": "#1E293B",
    "card_gradient": "linear-gradient(135deg, #1E293B 0%, #334155 100%)",
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "primary": "#10B981",
    "primary_dark": "#059669",
    "button_bg": "#065F46",
    "button_hover": "#047857",
    "action": "#FBBF24",
    "warning": "#F87171",
    "border": "#334155",
    "input_bg": "#0F172A",
    "shadow": "0 4px 24px rgba(0, 0, 0, 0.5), 0 2px 8px rgba(16, 185, 129, 0.15)",
    "plotly_template": "plotly_dark",
}


def get_theme(mode: str = "light") -> dict:
    """Get theme based on mode"""
    return DARK_THEME if mode == "dark" else LIGHT_THEME


def get_css(mode: str = "light") -> str:
    """Generate CSS for the selected theme"""
    t = get_theme(mode)

    return f"""
    <style>
        /* Apply theme to app */
        .stApp {{
            background-color: {t["bg"]} !important;
            color: {t["text_primary"]} !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {t["bg_secondary"]} !important;
        }}

        [data-testid="stSidebar"] * {{
            color: {t["text_primary"]} !important;
        }}

        /* Text colors */
        h1, h2, h3, h4, h5, h6, p, span, label, div {{
            color: {t["text_primary"]};
        }}

        /* Cards (user_card, graph_card, stats_card) */
        div[class*="st-key-user_card"],
        div[class*="st-key-graph_card"],
        div[class*="st-key-stats_card"] {{
            background: {t["card_gradient"]} !important;
            box-shadow: {t["shadow"]} !important;
            border-radius: 16px !important;
            border: 1px solid {t["border"]} !important;
        }}

        /* ─────────────────────────────────────────────── */
        /* ALL INPUTS - Force text color and background */
        /* ─────────────────────────────────────────────── */

        /* Text inputs */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stDateInput input,
        .stTimeInput input {{
            background-color: {t["input_bg"]} !important;
            color: {t["text_primary"]} !important;
            border-color: {t["border"]} !important;
        }}

        /* Input placeholders */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder,
        .stNumberInput input::placeholder {{
            color: {t["text_secondary"]} !important;
            opacity: 0.7 !important;
        }}

        /* Selectbox - the visible value */
        [data-baseweb="select"] {{
            background-color: {t["input_bg"]} !important;
        }}

        [data-baseweb="select"] > div {{
            background-color: {t["input_bg"]} !important;
            color: {t["text_primary"]} !important;
        }}

        [data-baseweb="select"] span,
        [data-baseweb="select"] div {{
            color: {t["text_primary"]} !important;
        }}

        /* Selectbox dropdown options */
        [data-baseweb="popover"] {{
            background-color: {t["bg_secondary"]} !important;
        }}

        [data-baseweb="popover"] li {{
            background-color: {t["bg_secondary"]} !important;
            color: {t["text_primary"]} !important;
        }}

        [data-baseweb="popover"] li:hover {{
            background-color: {t["bg"]} !important;
        }}

        /* Number input wrapper */
        .stNumberInput > div > div {{
            background-color: {t["input_bg"]} !important;
            color: {t["text_primary"]} !important;
        }}

        /* Number input +/- buttons */
        .stNumberInput button {{
            background-color: {t["bg_secondary"]} !important;
            color: {t["text_primary"]} !important;
        }}

        /* Date input picker */
        [data-baseweb="input"] {{
            background-color: {t["input_bg"]} !important;
        }}

        [data-baseweb="input"] input {{
            background-color: {t["input_bg"]} !important;
            color: {t["text_primary"]} !important;
        }}

        /* Checkbox label */
        .stCheckbox label,
        .stCheckbox label span {{
            color: {t["text_primary"]} !important;
        }}

        /* Buttons - base style */
        .stButton button {{
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
        }}

        .stButton button:hover {{
            transform: translateY(-1px);
        }}

        {f'''
        /* Dark mode: all buttons get sober green */
        .stButton button {{
            background-color: {t["button_bg"]} !important;
            color: #F1F5F9 !important;
            border: 1px solid {t["button_hover"]} !important;
        }}

        .stButton button:hover {{
            background-color: {t["button_hover"]} !important;
            border-color: {t["primary"]} !important;
        }}
        ''' if t["name"] == "dark" else ""}

        /* Primary buttons (form_submit_button with type=primary) - always brand color */
        .stButton button[kind="primary"],
        button[kind="primaryFormSubmit"] {{
            background-color: {t["primary"]} !important;
            color: white !important;
            border: none !important;
        }}

        .stButton button[kind="primary"]:hover,
        button[kind="primaryFormSubmit"]:hover {{
            background-color: {t["primary_dark"]} !important;
        }}

        /* Metric labels */
        [data-testid="stMetricLabel"] {{
            color: {t["text_secondary"]} !important;
        }}

        [data-testid="stMetricValue"] {{
            color: {t["text_primary"]} !important;
        }}

        /* Expanders */
        [data-testid="stExpander"] {{
            background-color: {t["bg_secondary"]} !important;
            border: 1px solid {t["border"]} !important;
            border-radius: 12px !important;
        }}

        [data-testid="stExpander"] summary {{
            color: {t["text_primary"]} !important;
        }}

        /* DataFrame */
        [data-testid="stDataFrame"] {{
            background-color: {t["bg_secondary"]} !important;
        }}

        /* Captions */
        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {t["text_secondary"]} !important;
        }}
    </style>
    """
