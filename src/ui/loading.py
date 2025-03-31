import streamlit as st
import time

def show_loading_state():
    """
    Cyber-inspired loading animation with circuit-like effects
    """
    try:
        st.html("""
        <div class="loading-container-cyber">
            <div class="rocket-animation-cyber">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="cyber-rocket">
                <path d="M50 10 L30 70 L50 65 L70 70 Z" fill="#00FFD1"/>
                <path d="M40 80 L50 90 L60 80" stroke="#00FFD1" stroke-width="3" fill="none"/>
            </svg>
        </div>
        
        <h1 class="title-cyber">AutoML</h1>
        
        <h2 class="subtitle-cyber">You Ask , We Deliver</h2>
        
        <div class="loading-content-cyber">
            <p class="loading-text-cyber">Initializing neural networks...</p>
            <div class="loading-bar-container-cyber">
                <div class="loading-bar-cyber"></div>
            </div>
        </div>
        
        <style>
            body { background-color: #000000 !important; }
            
            .loading-container-cyber {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 80vh;
                text-align: center;
                padding: 2rem;
                background: radial-gradient(circle, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 100%);
            }
            
            .cyber-rocket {
                width: 100px;
                height: 100px;
                animation: pulse 2s infinite;
            }
            
            .title-cyber {
                font-size: 3rem;
                margin-bottom: 0.5rem;
                color: #00FFD1;
                text-shadow: 0 0 10px #00FFD1;
                font-family: 'Orbitron', sans-serif;
            }
            
            .subtitle-cyber {
                font-size: 1.5rem;
                margin-bottom: 2rem;
                color: #00A86B;
                font-family: 'Chakra Petch', sans-serif;
            }
            
            .loading-content-cyber {
                background: rgba(0, 255, 209, 0.05);
                border: 1px solid rgba(0, 255, 209, 0.2);
                padding: 1.5rem 2rem;
                border-radius: 8px;
                max-width: 600px;
                width: 100%;
            }
            
            .loading-text-cyber {
                margin: 0 0 1rem 0;
                font-size: 1.1rem;
                color: #00FFD1;
                font-family: 'Chakra Petch', sans-serif;
            }
            
            .loading-bar-container-cyber {
                height: 6px;
                background: rgba(0, 255, 209, 0.2);
                border-radius: 3px;
                overflow: hidden;
            }
            
            .loading-bar-cyber {
                height: 100%;
                width: 30%;
                background: linear-gradient(90deg, #00FFD1, #00A86B);
                animation: circuit-load 1.5s cubic-bezier(0.4, 0.0, 0.2, 1) infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            @keyframes circuit-load {
                0% { transform: translateX(-100%); box-shadow: 0 0 10px #00FFD1; }
                50% { box-shadow: 0 0 20px #00FFD1; }
                100% { transform: translateX(400%); box-shadow: 0 0 10px #00FFD1; }
            }
        </style>
    </div> """)
    except Exception as e:
        # Fallback to built-in Streamlit spinner if custom animation fails
        st.warning("Custom loading animation unavailable. Using default spinner...")
        with st.spinner("Loading, please wait..."):
            time.sleep(3)


if __name__ == "__main__":
    show_loading_state()
    time.sleep(3)
    st.empty()
    st.success("App loaded successfully!")


