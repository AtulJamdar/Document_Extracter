"""
Streamlit UI for Intelligent Document Extraction Platform.

Features:
- Document upload
- Real-time extraction
- Results visualization
- Extraction history
- Error handling

This is a FRONTEND ONLY module.
All business logic stays in FastAPI backend.
"""

import streamlit as st
import pandas as pd
from io import BytesIO
import json
from datetime import datetime

from api_client import api_client

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="Document Extraction Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 Intelligent Document Extraction Platform")
st.markdown(
    "Extract structured data from documents using OCR and AI"
)

# ==============================================================================
# SIDEBAR CONFIGURATION
# ==============================================================================

st.sidebar.title("⚙️ Settings")

# Backend connection check
backend_url = st.sidebar.text_input(
    "Backend URL",
    value="http://127.0.0.1:8000",
    help="FastAPI server URL"
)

show_debug = st.sidebar.checkbox(
    "Show Debug Information",
    value=False,
    help="Display raw OCR text and extraction details"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown(
    """
    **Document Types Supported:**
    - Aadhaar
    - Passport
    - Driving License
    - Invoice
    
    **Features:**
    - Advanced preprocessing
    - OCR text extraction
    - Document classification
    - Structured data extraction
    """
)

# ==============================================================================
# SESSION STATE MANAGEMENT
# ==============================================================================

if "extraction_history" not in st.session_state:
    st.session_state.extraction_history = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "uploaded_file_bytes" not in st.session_state:
    st.session_state.uploaded_file_bytes = None

# ==============================================================================
# MAIN CONTENT AREA
# ==============================================================================

# File upload section
st.markdown("### 📤 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a document image",
    type=["png", "jpg", "jpeg"],
    help="Supported formats: PNG, JPG, JPEG"
)

if uploaded_file:
    # Store file bytes for API call
    file_bytes = uploaded_file.read()
    st.session_state.uploaded_file_bytes = file_bytes

    # Create two columns: preview and extract button
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### 👁️ Preview")
        st.image(
            file_bytes,
            caption=f"Uploaded: {uploaded_file.name}",
            use_column_width=True
        )

    with col2:
        st.markdown("#### ⚡ Action")
        st.markdown("")  # Spacing
        
        extract_button = st.button(
            "🔍 Extract Information",
            use_container_width=True,
            key="extract_button",
            type="primary"
        )

        if extract_button:
            with st.spinner("🔄 Processing document..."):
                result = api_client.upload_document(
                    file_bytes,
                    uploaded_file.name
                )

                st.session_state.current_result = result

                # Add to history
                if "error" not in result:
                    st.session_state.extraction_history.insert(
                        0,
                        {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "filename": uploaded_file.name,
                            "type": result.get("document_type", "Unknown"),
                            "confidence": result.get("confidence", 0),
                            "status": "✅ Success"
                        }
                    )

    # Display results
    if st.session_state.current_result:
        result = st.session_state.current_result

        st.markdown("---")

        # Error handling
        if "error" in result:
            st.error(f"❌ Extraction Failed")
            st.error(f"**Error:** {result['error']['message']}")
            st.session_state.extraction_history.insert(
                0,
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "filename": uploaded_file.name,
                    "type": "Error",
                    "confidence": 0,
                    "status": "❌ Failed"
                }
            )

        else:
            # Success! Display results in tabs
            st.success("✅ Extraction Completed Successfully")

            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "📊 Extracted Data",
                    "📝 OCR Text",
                    "📈 Metadata",
                    "🔍 Debug Info"
                ]
            )

            # Tab 1: Extracted Data
            with tab1:
                st.markdown("### Extracted Fields")

                document_type = result.get("document_type", "Unknown").upper()
                confidence = result.get("confidence", 0)

                # Show document type and confidence
                col_type, col_conf = st.columns(2)

                with col_type:
                    st.metric(
                        "Document Type",
                        document_type,
                        delta=None
                    )

                with col_conf:
                    st.metric(
                        "Confidence Score",
                        f"{confidence:.1%}",
                        delta=None,
                        delta_color="off"
                    )

                # Show extracted data
                extracted_data = result.get("extracted_data", {})

                if extracted_data:
                    st.markdown("**Extracted Information:**")

                    # Create nice display for each field
                    for field_name, field_value in extracted_data.items():
                        # Format field name nicely
                        display_name = field_name.replace("_", " ").title()

                        if field_value:
                            st.text_input(
                                display_name,
                                value=str(field_value),
                                disabled=True,
                                key=f"field_{field_name}"
                            )
                        else:
                            st.warning(f"{display_name}: Not extracted")

                    # Download JSON button
                    st.markdown("---")
                    json_str = json.dumps(extracted_data, indent=2)

                    st.download_button(
                        label="⬇️ Download as JSON",
                        data=json_str,
                        file_name=f"{document_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                else:
                    st.warning(
                        "No structured data extracted. "
                        "Check OCR text for raw content."
                    )

            # Tab 2: OCR Text
            with tab2:
                st.markdown("### Raw OCR Text")
                st.markdown(
                    "**Note:** This is the raw text extracted by OCR. "
                    "Use this to verify OCR quality and debug extraction issues."
                )

                raw_text = result.get("raw_text", "")

                st.text_area(
                    "OCR Output",
                    value=raw_text,
                    height=300,
                    disabled=True,
                    label_visibility="collapsed"
                )

                # Copy button simulation
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(
                        f"📊 Total characters: {len(raw_text)}"
                    )
                with col2:
                    st.caption(
                        f"📝 Lines: {len(raw_text.split(chr(10)))}"
                    )

            # Tab 3: Metadata
            with tab3:
                st.markdown("### Extraction Metadata")

                metadata = {
                    "Document ID": result.get("document_id", "N/A"),
                    "Document Type": result.get("document_type", "Unknown"),
                    "Confidence Score": f"{result.get('confidence', 0):.1%}",
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Filename": uploaded_file.name,
                }

                # Display as key-value pairs
                for key, value in metadata.items():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"**{key}**")
                    with col2:
                        st.code(str(value))

            # Tab 4: Debug Info
            with tab4:
                if show_debug:
                    st.markdown("### Debug Information")

                    st.markdown("**Full API Response:**")
                    st.json(result)

                    st.markdown("---")

                    st.markdown("**Processing Notes:**")
                    st.info(
                        "✅ Document uploaded successfully\n"
                        "✅ Image preprocessing applied\n"
                        "✅ OCR extraction completed\n"
                        "✅ Document classification performed\n"
                        "✅ Field extraction completed"
                    )
                else:
                    st.info(
                        "Enable 'Show Debug Information' in sidebar "
                        "to view detailed debug data"
                    )

# ==============================================================================
# EXTRACTION HISTORY
# ==============================================================================

st.markdown("---")
st.markdown("### 📋 Extraction History")

if st.session_state.extraction_history:
    # Convert to DataFrame for nice display
    history_df = pd.DataFrame(st.session_state.extraction_history)

    # Display as table
    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "timestamp": st.column_config.TextColumn("Time"),
            "filename": st.column_config.TextColumn("File"),
            "type": st.column_config.TextColumn("Type"),
            "confidence": st.column_config.NumberColumn(
                "Confidence",
                format="%.1%"
            ),
            "status": st.column_config.TextColumn("Status"),
        }
    )

    # Clear history button
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.extraction_history = []
        st.rerun()

else:
    st.info("📭 No extraction history yet. Upload a document to get started!")

# ==============================================================================
# FOOTER
# ==============================================================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    <p>🚀 Document Extraction Platform v1.0</p>
    <p style='font-size: 0.8em; color: gray;'>
    Powered by FastAPI, Streamlit, Tesseract OCR, and Groq LLM
    </p>
    </div>
    """,
    unsafe_allow_html=True
)
