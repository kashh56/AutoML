# src/css.py
import streamlit as st

def load_css():
    css = """
        <style>

        /* --- EXPLICIT COLOR DEFINITIONS --- */
        :root {
            --dark-bg: #0E1117;
            --light-text: #FAFAFA;
            
            --neon-green: #00FFA3;
            --neon-font: Arial, Helvetica, sans-serif;
            --tab-font-size: 18px;
            --tab-bottom-border-height: 4px;
            /* Component Styling Variables */
            --card-bg: rgba(30, 30, 40, 0.5);
            --card-border: rgba(0, 255, 163, 0.25);
            --expander-header-bg: rgba(40, 40, 55, 0.6);
            --expander-hover-bg: rgba(0, 255, 163, 0.1);
        }

        /* --- Base Styles --- */
        body {
            background-color: var(--dark-bg) !important;
            color: var(--light-text) !important;
        }
        .stApp {
             background-color: var(--dark-bg) !important;
        }

        /* --- App Header Styling --- */
        .app-title {
            color: var(--neon-green) !important;
            font-family: var(--neon-font);
            font-size: 80px !important;
            font-weight: 700;
            text-shadow:
                0 0 1px var(--neon-green),
                0 0 2px var(--neon-green),
                0 0 5px var(--neon-green),
                0 0 45px var(--neon-green);
            margin-bottom: 25px !important;
            line-height: 1.0 !important;
            text-align: center !important;
        }
        .app-tagline {
            color: var(--neon-green) !important;
            font-family: var(--neon-font);
            font-size: 27px !important;
            font-style: normal !important;
            font-weight: 400 !important;
            text-shadow:
                0 0 5px var(--neon-green),
                0 0 10px var(--neon-green);
            margin-top: 10px !important;
            text-align: center !important;
        }
        .app-header {
             padding: 1rem 0 !important;
             margin-bottom: 2rem !important;
             text-align: center !important;
        }
        /* --- End App Header Styling --- */

        
        /* --- Tab Styling --- */
        div[data-baseweb="tab-list"] button[data-baseweb="tab"],
        div[data-baseweb="tab-list"] button[data-baseweb="tab"] > div,
        div[data-baseweb="tab-list"] button[data-baseweb="tab"] > div > span {
            font-size: var(--tab-font-size) !important;
            font-family: var(--neon-font) !important;
            font-weight: 600 !important;
        }
        div[data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"],
        div[data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"] > div,
        div[data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"] > div > span {
            font-size: var(--tab-font-size) !important;
        }
        div[data-baseweb="tab-list"] {
            border: none !important; border-top: none !important; border-right: none !important; border-left: none !important; border-bottom: none !important;
            border-color: transparent !important; outline: none !important; box-shadow: none !important;
            margin-bottom: 25px !important; padding: 0 !important;
            display: flex !important; justify-content: space-around !important;
        }
        button[data-baseweb="tab"] {
            color: var(--light-text) !important; padding: 1rem 1.5rem !important;
            transition: color 0.3s ease, text-shadow 0.3s ease, border-bottom-color 0.3s ease !important;
            border-style: solid !important; border-width: 0 0 var(--tab-bottom-border-height) 0 !important;
            border-color: transparent transparent transparent transparent !important;
            outline: none !important; box-shadow: none !important; background-color: transparent !important;
            margin: 0 !important; line-height: normal !important; flex-shrink: 0 !important;
        }
        button[data-baseweb="tab"]::before, button[data-baseweb="tab"]::after { display: none !important; content: none !important; }
        button[data-baseweb="tab"]:hover:not([aria-selected="true"]) {
            color: var(--neon-green) !important; background-color: transparent !important;
            border-color: transparent transparent transparent transparent !important; outline: none !important; box-shadow: none !important;
            text-shadow: 0 0 3px var(--neon-green), 0 0 6px var(--neon-green);
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            border: none !important; border-top: none !important; border-right: none !important; border-left: none !important; border-bottom: none !important;
            border-color: transparent !important; outline: none !important; box-shadow: none !important; background-color: transparent !important;
            color: var(--neon-green) !important; border-bottom-style: solid !important;
            border-bottom-width: var(--tab-bottom-border-height) !important; border-bottom-color: var(--neon-green) !important;
            text-shadow: 0 0 3px var(--neon-green), 0 0 6px var(--neon-green);
        }
        /* --- End Tab Styling --- */


        
        /* --- Welcome Page Specific Styling --- */

        /* Main Welcome Header (H1) - *** UPDATED COLOR *** */
        .welcome-header h1 {
            font-size: 2.8rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
            color: var(--neon-green) !important; /* Use neon green */
            text-align: left !important;
            border-bottom: none !important;
            /* Optional: Add a subtle glow like the main title */
            text-shadow: 0 0 4px rgba(0, 255, 163, 0.7);
        }
        /* Main Welcome Subtitle (P) */
         .welcome-header p.subtitle {
            font-size: 1.15rem !important;
            color: var(--subtitle-text) !important; /* Keep subtitle gray */
            margin-bottom: 0 !important;
            text-align: left !important;
         }

        /* Section Headers (H2 generated by st.markdown("## ...")) */
        .stApp h2 {
            font-size: 1.9rem !important;
            font-weight: 600 !important;
            color: var(--neon-green) !important;
            border-bottom: 1px solid rgba(0, 255, 163, 0.3);
            padding-bottom: 8px !important;
            margin-top: 40px !important;
            margin-bottom: 25px !important;
        }
        /* Override for Sidebar Title H2 */
        section[data-testid="stSidebar"] h2 {
             border-bottom: none !important;
             color: #E6E6FA !important;
             font-size: 1.8rem !important;
             font-weight: 600 !important;
             margin: 0 !important;
             padding-bottom: 0 !important;
        }

        /* Feature Card Styling */
        .feature-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 1.5rem 1.75rem;
            height: 100%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            margin-bottom: 1rem;
        }
        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 255, 163, 0.15);
        }
         /* Titles within cards (H3) */
         .feature-card h3 {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            color: var(--light-text) !important;
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
            border-bottom: none !important;
            padding-bottom: 0 !important;
         }
         /* Lists within cards */
         .feature-card ul {
            padding-left: 0 !important; margin-left: 5px; margin-bottom: 0 !important;
            list-style-type: none;
         }
         .feature-card ul li {
              margin-bottom: 0.6rem !important; line-height: 1.5;
              color: var(--subtitle-text) !important; position: relative; padding-left: 1.2em;
         }
         .feature-card ul li::before {
              content: '▪'; color: var(--neon-green); font-weight: bold;
              display: inline-block; position: absolute; left: 0; top: 0;
         }

        /* Getting Started List (Ordered List - OL) */
        .stApp ol {
             padding-left: 0 !important; margin-left: 5px; margin-bottom: 30px !important;
             list-style-type: none; counter-reset: getting-started-counter;
        }
         .stApp ol li {
             margin-bottom: 12px !important; line-height: 1.6 !important;
             color: var(--light-text) !important; counter-increment: getting-started-counter;
             position: relative; padding-left: 2.5em;
         }
         .stApp ol li::before {
              content: counter(getting-started-counter); color: var(--dark-bg); background-color: var(--neon-green);
              font-weight: bold; border-radius: 50%; width: 1.6em; height: 1.6em; display: inline-block;
              text-align: center; line-height: 1.6em; position: absolute; left: 0; top: 0;
         }
         .stApp ol li strong { color: var(--neon-green) !important; font-weight: 600; }

        /* Expander Styling */
        div[data-testid="stExpander"] {
             border: none !important; border-radius: 8px !important; margin-bottom: 1rem !important;
             box-shadow: 0 2px 4px rgba(0,0,0,0.2); background-color: transparent !important; overflow: hidden;
        }
        div[data-testid="stExpander"] summary {
            padding: 0.8rem 1.2rem !important; font-size: 1.1rem !important; font-weight: 600 !important;
            color: var(--light-text) !important; background-color: var(--expander-header-bg) !important;
            border: none !important; border-radius: 0 !important;
            transition: background-color 0.2s ease, color 0.2s ease; cursor: pointer;
        }
         div[data-testid="stExpander"] summary:hover {
             background-color: var(--expander-hover-bg) !important; color: var(--neon-green) !important;
         }
         div[data-testid="stExpander"] summary svg { fill: var(--light-text) !important; }
         div[data-testid="stExpander"] summary:hover svg { fill: var(--neon-green) !important; }
         div[data-testid="stExpander"] div[role="button"] + div { /* Content area */
             padding: 1.2rem 1.5rem !important; background-color: var(--card-bg); border: none !important;
         }
         div[data-testid="stExpander"] div[role="button"] + div ul,
         div[data-testid="stExpander"] div[role="button"] + div ol { margin-bottom: 0 !important; padding-left: 20px !important; list-style-type: disc; }
         div[data-testid="stExpander"] div[role="button"] + div li {
             color: var(--subtitle-text) !important; margin-bottom: 0.5rem !important; list-style-type: disc; padding-left: 0;
         }
         div[data-testid="stExpander"] div[role="button"] + div li::before { content: none !important; }
         div[data-testid="stExpander"] a { color: var(--neon-green) !important; text-decoration: underline; }
         div[data-testid="stExpander"] a:hover { text-shadow: 0 0 3px var(--neon-green); }

         /* Footer Styling */
         .footer {
             margin-top: 4rem !important; padding: 1rem !important; font-size: 0.9rem !important;
             color: var(--subtitle-text) !important; text-align: center; width: 100%;
             position: relative; bottom: auto; left: auto;
             border-top: 1px solid rgba(255, 255, 255, 0.1);
         }
        /* --- End Welcome Page Specific Styling --- */

        
        /* --- Overview Tab Styling --- */

        /* Style for st.metric containers */
        div[data-testid="stMetric"] {
            background-color: var(--card-bg); /* Use card background */
            border: 1px solid var(--card-border); /* Use card border */
            border-radius: 8px;
            padding: 1rem 1.25rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            height: 100%; /* Ensure metrics in a row are same height */
        }
        div[data-testid="stMetric"]:hover {
             transform: translateY(-2px); /* Lift effect */
             box-shadow: 0 4px 8px rgba(0, 255, 163, 0.1); /* Neon glow */
        }

        /* Style for st.metric Label */
        div[data-testid="stMetric"] label[data-testid="stMetricLabel"] {
             color: var(--subtitle-text) !important; /* Dimmer label */
             font-weight: 500 !important;
             font-size: 0.95rem !important;
        }

        /* Style for st.metric Value */
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
             color: var(--neon-green) !important; /* Neon value */
             font-size: 2.5rem !important; /* Larger value */
             font-weight: 700 !important;
             padding-top: 5px;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
             /* Style delta if you use it */
             font-weight: 500 !important;
        }

        /* Section Headers in Overview Tab (Reuse H3 style) */
        /* The general .stApp h3 rule should cover this if specific enough */
        /* If not, target more specifically: */
        div[data-testid="stVerticalBlock"] h3 { /* Assuming Overview content is in a vertical block */
             font-size: 1.75rem !important;
             font-weight: 600 !important;
             color: var(--neon-green) !important;
             border-bottom: 1px solid rgba(0, 255, 163, 0.3);
             padding-bottom: 8px !important;
             margin-top: 30px !important; /* Adjust spacing */
             margin-bottom: 20px !important;
        }
        /* Reset for feature card H3 if needed */
         .feature-card h3 {
            font-size: 1.3rem !important;
            border-bottom: none !important;
            padding-bottom: 0 !important;
         }


        /* DataFrame Styling */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--card-border) !important; /* Neon border */
            border-radius: 8px;
            overflow: hidden; /* Ensures border radius applies to table */
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        /* DataFrame Header */
        div[data-testid="stDataFrame"] .col_heading {
            background-color: var(--expander-header-bg) !important; /* Darker header */
            color: var(--light-text) !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            text-align: left !important;
            border-bottom: 1px solid var(--neon-green) !important; /* Neon underline */
        }
        div[data-testid="stDataFrame"] .col_heading:first-of-type {
            border-top-left-radius: 7px; /* Match container radius */
        }
        div[data-testid="stDataFrame"] .col_heading:last-of-type {
            border-top-right-radius: 7px; /* Match container radius */
        }


        /* DataFrame Cells */
        div[data-testid="stDataFrame"] .dataframe td,
        div[data-testid="stDataFrame"] .dataframe th { /* Also style index header */
             color: var(--subtitle-text) !important;
             border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important; /* Faint row separators */
             border-right: none !important; /* Remove vertical separators */
             padding: 0.5rem 0.75rem !important;
             font-size: 0.9rem !important;
        }
        div[data-testid="stDataFrame"] .dataframe th { /* Index header specifically */
            background-color: rgba(30, 30, 40, 0.3); /* Slightly different background for index */
            color: var(--light-text) !important;
            font-weight: 500 !important;
        }

        /* DataFrame Rows Hover */
        div[data-testid="stDataFrame"] .dataframe tr:hover td,
        div[data-testid="stDataFrame"] .dataframe tr:hover th {
             background-color: rgba(0, 255, 163, 0.05) !important; /* Faint neon hover */
             color: var(--light-text) !important;
        }

        /* --- End Overview Tab Styling --- */





        /* --- Hide Streamlit elements --- */
        #MainMenu {visibility: hidden !important;}
        header {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        div[data-testid="stStatusWidget"] {display: none !important;}
        /* --- End Hide Streamlit elements --- */

        /* --- Sidebar styling --- */
        section[data-testid="stSidebar"] > div:first-child {
             background-color: var(--dark-bg) !important;
        }
        
        div[data-testid="stMetric"] { color: var(--light-text) !important; }
        div[data-testid="stMetric"] > div { color: var(--light-text) !important; }
        div[data-testid="stMetric"] label { color: var(--light-text) !important; }
        /* --- End Remaining Styles --- */

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)