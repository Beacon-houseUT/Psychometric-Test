import streamlit as st
import pandas as pd
import requests
import time

# ─── PAGE CONFIG ──────────────────────────────────
st.set_page_config(page_title="Psychometric Report", layout="centered")

# ─── GOOGLE DOCS STYLE STYLING ─────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main > div {
        max-width: 8.5in;
        margin: 0 auto;
        padding: 1in 1in;
        background-color: white;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        line-height: 1.6;
        color: #202124;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Document container */
    .doc-container {
        background-color: white;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin: 20px auto;
        padding: 0;
    }
    
    /* Title styles */
    .doc-title {
        font-size: 28px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 8px;
        color: #202124;
        border-bottom: none;
    }
    
    .doc-subtitle {
        font-size: 18px;
        font-weight: 400;
        text-align: center;
        margin-bottom: 40px;
        color: #5f6368;
    }
    
    /* Student info header */
    .student-header {
        border-bottom: 1px solid #dadce0;
        padding-bottom: 20px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .student-name {
        font-size: 25px !important;
        font-weight: 600;
        margin-bottom: 5px;
        color: #202124;
    }
    
    .student-details {
        font-size: 17px;
        color: #5f6368;
        margin-bottom: 10px;
    }
    
    .personality-type {
        font-size: 18px;
        font-weight: 500;
        color: #1a73e8;
        margin-top: 10px;
    }
    
    /* Section headers */
    .section-title {
        font-size: 25px !important;
        font-weight: 600;
        margin-top: 40px;
        margin-bottom: 8px;
        color: #202124;
    }
    
    .section-subtitle {
        font-size: 17px;
        color: #5f6368;
        margin-bottom: 20px;
        font-style: normal;
        line-height: 1.5;
    }
    
    /* Table styles */
    .doc-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 17px;
    }
    
    .doc-table th {
        background-color: #f8f9fa;
        border: 1px solid #dadce0;
        padding: 12px;
        text-align: left;
        font-weight: 500;
        color: #202124;
    }
    
    .doc-table td {
        border: 1px solid #dadce0;
        padding: 12px;
        vertical-align: top;
        color: #202124;
    }
    
    .doc-table tr:nth-child(even) {
        background-color: #fafafa;
    }
    
    /* Insight boxes */
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #1a73e8;
        padding: 16px;
        margin: 20px 0;
        font-style: normal;
        color: #5f6368;
        font-size: 17px;
    }
    
    .insight-label {
        font-weight: 500;
        color: #202124;
        font-style: normal;
    }
    
    /* Edit mode styles */
    .edit-notice {
        background-color: #fff3e0;
        border: 1px solid #ffb74d;
        padding: 12px;
        margin-bottom: 20px;
        border-radius: 4px;
        font-size: 17px;
        color: #e65100;
    }
    
    /* Button styles */
    .stButton > button {
        background-color: #1a73e8;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 500;
        font-size: 17px;
    }
    
    .stButton > button:hover {
        background-color: #1557b0;
    }
    
    /* Form styles */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        border: 1px solid #dadce0;
        border-radius: 4px;
        font-family: 'Inter', sans-serif;
        font-size: 17px;
    }
    
    /* Career section */
    .career-section {
        margin-top: 50px;
        border-top: 2px solid #dadce0;
        padding-top: 30px;
    }
    
    .career-title {
        font-size: 25px;
        font-weight: 600;
        margin-bottom: 30px;
        color: #202124;
        text-align: center;
    }
    
    .career-field {
        margin-bottom: 30px;
        padding: 20px;
        border: 1px solid #dadce0;
        border-radius: 4px;
        font-size: 17px;
    }
    
    .career-field-title {
        font-size: 25px;
        font-weight: 600;
        margin-bottom: 8px;
        color: #202124;
    }
    
    .alignment-high { 
        color: #137333; 
        font-weight: 500; 
        font-size: 17px;
    }
    
    .alignment-moderate { 
        color: #ea8600; 
        font-weight: 500; 
        font-size: 17px;
    }
    
    .alignment-low { 
        color: #d93025; 
        font-weight: 500; 
        font-size: 17px;
    }
    
    .career-role {
        margin: 15px 0;
        padding: 12px;
        background-color: #f8f9fa;
        border-radius: 4px;
    }
    
    .career-role-title {
        font-weight: 500;
        color: #202124;
        margin-bottom: 4px;
        font-size: 17px;
    }
    
    .career-role-desc {
        color: #5f6368;
        font-size: 17px;
    }
    
    /* Loading states */
    .stSpinner {
        text-align: center;
    }
    
    /* Summary table styles */
    .summary-table {
        margin: 20px 0;
        background-color: #f8f9fa;
        border-radius: 4px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'report_data' not in st.session_state:
    st.session_state.report_data = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'career_data' not in st.session_state:
    st.session_state.career_data = None
if 'career_analysis_requested' not in st.session_state:
    st.session_state.career_analysis_requested = False

# ─── UPLOAD FORM ──────────────────────────────────
if not st.session_state.form_submitted:
    st.markdown('<h1 class="doc-title">Psychometric Assessment Upload</h1>', unsafe_allow_html=True)
    
    with st.form("upload_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Child's Name", placeholder="Enter full name")
        with col2:
            age = st.number_input("Age", min_value=5, max_value=18, step=1)
        with col3:
            grade = st.text_input("Grade", placeholder="e.g., 5th grade")
        
        uploaded_files = st.file_uploader(
            "Upload Test Screenshots (1-4 images)",
            accept_multiple_files=True,
            type=["jpg", "jpeg", "png"],
            help="Upload screenshots of the test results"
        )
        
        submit = st.form_submit_button("Generate Report", type="primary", use_container_width=True)
    
    if submit:
        if not (name and age and grade and uploaded_files):
            st.error("Please complete all fields and upload at least one image.")
        else:
            # Store form data in session state
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.grade = grade
            st.session_state.uploaded_files = uploaded_files
            st.session_state.form_submitted = True
            st.rerun()

# ─── PROCESS AND DISPLAY REPORT ─────────────────
if st.session_state.form_submitted and not st.session_state.report_data:
    # Show loading animation
    with st.spinner(f"Analyzing test results for {st.session_state.name}..."):
        progress = st.progress(0)
        status = st.empty()
        
        status.text("Uploading images...")
        progress.progress(20)
        
        session = requests.Session()
        session.trust_env = False
        
        form_data = {
            "name": st.session_state.name,
            "age": str(st.session_state.age),
            "grade": st.session_state.grade,
            "fileCount": str(len(st.session_state.uploaded_files)),
        }
        
        files = []
        for i, f in enumerate(st.session_state.uploaded_files):
            f.seek(0)
            files.append((f"data{i}", (f.name, f.read(), f.type)))
        
        try:
            status.text("Processing test data...")
            progress.progress(50)
            
            # Multiple retry attempts with different configurations
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    # Configure session with better connection handling
                    session.headers.update({
                        'User-Agent': 'StreamlitApp/1.0',
                        'Connection': 'close'
                    })
                    
                    resp = session.post(
                        "https://uttarika.app.n8n.cloud/webhook/report-upload",
                        data=form_data,
                        files=files,
                        timeout=(30, 180),  # (connection timeout, read timeout)
                        stream=False
                    )
                    resp.raise_for_status()
                    break  # Success, exit retry loop
                    
                except (requests.exceptions.ConnectionError, 
                        requests.exceptions.ChunkedEncodingError,
                        requests.exceptions.Timeout) as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        status.text(f"Connection issue, retrying... (attempt {retry_count + 1})")
                        time.sleep(2)  # Wait before retry
                        # Reset files for retry
                        files = []
                        for i, f in enumerate(st.session_state.uploaded_files):
                            f.seek(0)
                            files.append((f"data{i}", (f.name, f.read(), f.type)))
                    else:
                        raise e
            
            status.text("Generating insights...")
            progress.progress(80)
            
            # Handle response parsing more safely
            try:
                payload = resp.json()
            except ValueError:
                # If JSON parsing fails, try to get text response
                text_response = resp.text
                st.error(f"Invalid JSON response received. Response: {text_response[:500]}...")
                st.session_state.form_submitted = False
                st.stop()
            
            # Validate response structure
            if not payload:
                st.error("Empty response received from server")
                st.session_state.form_submitted = False
                st.stop()
            
            # Unwrap list response
            if isinstance(payload, list) and payload:
                payload = payload[0]
            
            st.session_state.report_data = payload
            st.session_state.original_data = payload.copy()  # Keep original for reset
            progress.progress(100)
            status.text("Report ready!")
            
        except requests.exceptions.Timeout:
            st.error("Request timed out. The server may be busy. Please try again.")
            st.session_state.form_submitted = False
            st.stop()
            
        except requests.exceptions.ConnectionError:
            st.error("Connection failed. Please check your internet connection and try again.")
            st.session_state.form_submitted = False
            st.stop()
            
        except requests.exceptions.HTTPError as e:
            st.error(f"Server error ({e.response.status_code}): {e.response.text}")
            st.session_state.form_submitted = False
            st.stop()
            
        except Exception as e:
            st.error(f"Could not generate report: {e}")
            st.error("Please try uploading fewer or smaller images, or try again later.")
            st.session_state.form_submitted = False
            st.stop()

# ─── CAREER ANALYSIS REQUEST ─────────────────
if st.session_state.career_analysis_requested and not st.session_state.career_data:
    # Position spinner at the bottom where buttons are
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.spinner("Generating career recommendations..."):
        try:
            # Get student info
            student_info = st.session_state.report_data.get("studentInfo", {
                "name": st.session_state.name,
                "age": st.session_state.age,
                "grade": st.session_state.grade,
            })
            
            # Prepare career analysis request
            career_request_data = {
                "studentInfo": {
                    "name": student_info.get('name', 'Student'),
                    "age": student_info.get('age', 'Unknown'),
                    "grade": student_info.get('grade', 'Unknown')
                },
                "editedTestData": st.session_state.report_data.get("testData", {}),
                "editedInsights": st.session_state.report_data.get("insightLines", [])
            }
            
            # Send request to career analysis webhook
            session = requests.Session()
            session.trust_env = False
            session.headers.update({
                'User-Agent': 'StreamlitApp/1.0',
                'Content-Type': 'application/json'
            })
            
            career_response = session.post(
                "https://uttarika.app.n8n.cloud/webhook/career-analysis",
                json=career_request_data,
                timeout=(30, 120)
            )
            career_response.raise_for_status()
            
            # Parse career response
            career_data = career_response.json()
            if isinstance(career_data, list) and career_data:
                career_data = career_data[0]
            
            # Extract the actual career analysis from your n8n structure
            if career_data.get("reportData") and career_data["reportData"].get("careerAnalysis"):
                actual_career_data = career_data["reportData"]["careerAnalysis"]
            else:
                # Fallback to direct structure
                actual_career_data = career_data
            
            st.session_state.career_data = actual_career_data
            
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to generate career recommendations: {e}")
            st.session_state.career_analysis_requested = False
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.career_analysis_requested = False

# ─── HELPER FUNCTIONS FOR EDITING ──────────────────
def render_editable_table(config, rows, test_index):
    """Render an editable table for a specific test type"""
    
    if config["key"] == "high5Data":
        # HIGH5 has different structure (no score field)
        for j, row in enumerate(rows):
            col1, col2, col3 = st.columns([1, 1, 3])
            
            with col1:
                new_preference = st.text_input(
                    f"Strength {j+1}",
                    value=row.get("preference", ""),
                    key=f"{config['key']}_pref_{j}",
                    label_visibility="collapsed"
                )
            
            with col2:
                new_domain = st.text_input(
                    f"Domain {j+1}",
                    value=row.get("domain", ""),
                    key=f"{config['key']}_domain_{j}",
                    label_visibility="collapsed"
                )
            
            with col3:
                new_meaning = st.text_area(
                    f"Meaning {j+1}",
                    value=row.get("meaning", ""),
                    key=f"{config['key']}_meaning_{j}",
                    height=80,
                    label_visibility="collapsed"
                )
            
            # Update the data in session state
            st.session_state.report_data["testData"][config["key"]][j].update({
                "preference": new_preference,
                "domain": new_domain,
                "meaning": new_meaning
            })
    
    else:
        # Standard structure for other tests
        for j, row in enumerate(rows):
            col1, col2, col3 = st.columns([1, 1, 3])
            
            with col1:
                if config["key"] == "test16PersonalityData":
                    # For 16 personalities, preference is read-only
                    st.text_input(
                        f"Preference {j+1}",
                        value=row.get("preference", ""),
                        key=f"{config['key']}_pref_{j}_readonly",
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    new_preference = row.get("preference", "")
                else:
                    new_preference = st.text_input(
                        f"Preference {j+1}",
                        value=row.get("preference", ""),
                        key=f"{config['key']}_pref_{j}",
                        label_visibility="collapsed"
                    )
            
            with col2:
                new_score = st.text_input(
                    f"Score {j+1}",
                    value=row.get("score", ""),
                    key=f"{config['key']}_score_{j}",
                    label_visibility="collapsed"
                )
            
            with col3:
                new_meaning = st.text_area(
                    f"Meaning {j+1}",
                    value=row.get("meaning", ""),
                    key=f"{config['key']}_meaning_{j}",
                    height=80,
                    label_visibility="collapsed"
                )
            
            # Update the data in session state
            st.session_state.report_data["testData"][config["key"]][j].update({
                "preference": new_preference,
                "score": new_score,
                "meaning": new_meaning
            })

def render_read_only_table(config, rows):
    """Render a read-only table using Google Docs styling"""
    
    if config["key"] == "high5Data":
        # HIGH5 special display - only show preference, domain, meaning
        table_data = []
        for row in rows:
            table_data.append([
                row.get("preference", ""),
                row.get("domain", ""),
                row.get("meaning", "")
            ])
        
        headers = ["Strength", "Domain", "Meaning"]
        df = pd.DataFrame(table_data, columns=headers)
    else:
        # Standard display - show preference, score, meaning
        table_data = []
        for row in rows:
            table_data.append([
                row.get("preference", ""),
                row.get("score", ""),
                row.get("meaning", "")
            ])
        
        df = pd.DataFrame(table_data, columns=config["headers"])
    
    # Convert to HTML for custom styling
    html_table = df.to_html(index=False, escape=False)
    html_table = html_table.replace('<td>', '<td style="padding: 12px; border: 1px solid #dadce0; vertical-align: top; color: #202124; font-size: 17px; font-family: Inter, sans-serif;">')
    html_table = html_table.replace('<th>', '<th style="background-color: #f8f9fa; border: 1px solid #dadce0; padding: 12px; text-align: left; font-weight: 500; color: #202124; font-size: 17px; font-family: Inter, sans-serif;">')
    html_table = html_table.replace('<table border="1" class="dataframe">', '<table class="doc-table" style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 17px; font-family: Inter, sans-serif;">')
    
    st.markdown(html_table, unsafe_allow_html=True)

def render_career_section(career_data):
    """Render the career analysis section with edit functionality"""
    if not career_data:
        return
    
    st.markdown('<div class="career-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="career-title">Career Pathways & Recommendations</h1>', unsafe_allow_html=True)
    
    # Display career success/warning message
    if career_data.get("userMessage"):
        msg = career_data["userMessage"]
        if msg["type"] == "success":
            st.success(f"**{msg['title']}**: {msg['message']}")
        elif msg["type"] == "warning":
            st.warning(f"**{msg['title']}**: {msg['message']}")
        else:
            st.info(f"**{msg['title']}**: {msg['message']}")
    
    # Core Identity Summary Section
    if career_data.get("summary"):
        st.markdown('<h2 style="font-size: 25px; font-weight: 600; margin-top: 40px; margin-bottom: 8px; color: #202124;">Summary</h2>', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 17px; color: #5f6368; margin-bottom: 20px; line-height: 1.5;">Key characteristics based on comprehensive psychometric analysis</div>', unsafe_allow_html=True)
        
        summary_data = career_data["summary"]
        
        if st.session_state.edit_mode:
            # Editable summary section
            st.write("**Edit Summary:**")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write("**Category**")
            with col2:
                st.write("**Key Characteristics**")
            
            # Core Drive
            col1, col2 = st.columns([1, 2])
            with col1:
                st.text_input("Category", value="Core Drive", key="summary_cat_1", disabled=True, label_visibility="collapsed")
            with col2:
                new_core_drive = st.text_area(
                    "Core Drive", 
                    value=summary_data.get("coreDriver", "Analysis pending"),
                    key="summary_core_drive",
                    height=80,
                    label_visibility="collapsed"
                )
                # Update in session state
                if 'career_data' in st.session_state and st.session_state.career_data:
                    st.session_state.career_data["summary"]["coreDriver"] = new_core_drive
            
            # Personality
            col1, col2 = st.columns([1, 2])
            with col1:
                st.text_input("Category", value="Personality", key="summary_cat_2", disabled=True, label_visibility="collapsed")
            with col2:
                new_personality = st.text_area(
                    "Personality", 
                    value=summary_data.get("personality", "Analysis pending"),
                    key="summary_personality",
                    height=80,
                    label_visibility="collapsed"
                )
                if 'career_data' in st.session_state and st.session_state.career_data:
                    st.session_state.career_data["summary"]["personality"] = new_personality
            
            # Work Style
            col1, col2 = st.columns([1, 2])
            with col1:
                st.text_input("Category", value="Work Style", key="summary_cat_3", disabled=True, label_visibility="collapsed")
            with col2:
                new_work_style = st.text_area(
                    "Work Style", 
                    value=summary_data.get("workStyle", "Analysis pending"),
                    key="summary_work_style",
                    height=80,
                    label_visibility="collapsed"
                )
                if 'career_data' in st.session_state and st.session_state.career_data:
                    st.session_state.career_data["summary"]["workStyle"] = new_work_style
            
            # Learning Style
            col1, col2 = st.columns([1, 2])
            with col1:
                st.text_input("Category", value="Learning Style", key="summary_cat_4", disabled=True, label_visibility="collapsed")
            with col2:
                new_learning_style = st.text_area(
                    "Learning Style", 
                    value=summary_data.get("learningStyle", "Analysis pending"),
                    key="summary_learning_style",
                    height=80,
                    label_visibility="collapsed"
                )
                if 'career_data' in st.session_state and st.session_state.career_data:
                    st.session_state.career_data["summary"]["learningStyle"] = new_learning_style
        else:
            # Read-only summary table
            summary_html = '''
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 17px; font-family: Inter, sans-serif; background-color: #f8f9fa; border-radius: 4px;">
                <tr><th style="background-color: #f8f9fa; border: 1px solid #dadce0; padding: 12px; text-align: left; font-weight: 500; color: #202124; font-size: 17px;">Category</th><th style="background-color: #f8f9fa; border: 1px solid #dadce0; padding: 12px; text-align: left; font-weight: 500; color: #202124; font-size: 17px;">Key Characteristics</th></tr>
            '''
            
            summary_items = [
                ("Core Drive", summary_data.get("coreDriver", "Analysis pending")),
                ("Personality", summary_data.get("personality", "Analysis pending")),
                ("Work Style", summary_data.get("workStyle", "Analysis pending")),
                ("Learning Style", summary_data.get("learningStyle", "Analysis pending"))
            ]
            
            for category, characteristic in summary_items:
                summary_html += f'<tr><td style="border: 1px solid #dadce0; padding: 12px; vertical-align: top; color: #202124; font-size: 17px;">{category}</td><td style="border: 1px solid #dadce0; padding: 12px; vertical-align: top; color: #202124; font-size: 17px;">{characteristic}</td></tr>'
            
            summary_html += '</table>'
            st.markdown(summary_html, unsafe_allow_html=True)
    
    # Career Fields Section
    if career_data.get("careerFields"):
        career_fields = career_data["careerFields"]
        
        for field_index, (field_key, field_data) in enumerate(career_fields.items()):
            st.markdown('<div class="career-field">', unsafe_allow_html=True)
            
            if st.session_state.edit_mode:
                # Editable career field
                st.write(f"**Edit Career Field {field_index + 1}:**")
                
                # Title
                new_title = st.text_input(
                    "Field Title",
                    value=field_data.get("title", "Career Field"),
                    key=f"career_title_{field_index}",
                    label_visibility="collapsed"
                )
                if 'career_data' in st.session_state and st.session_state.career_data:
                    st.session_state.career_data["careerFields"][field_key]["title"] = new_title
                
                # Alignment
                alignment_options = ["High", "Moderate", "Low"]
                current_alignment = field_data.get("alignment", "Unknown")
                new_alignment = st.selectbox(
                    "Alignment",
                    alignment_options,
                    index=alignment_options.index(current_alignment) if current_alignment in alignment_options else 0,
                    key=f"career_alignment_{field_index}"
                )
                if 'career_data' in st.session_state and st.session_state.career_data:
                    st.session_state.career_data["careerFields"][field_key]["alignment"] = new_alignment
                
                # Description
                new_description = st.text_area(
                    "Description",
                    value=field_data.get("description", "Analysis in progress"),
                    key=f"career_desc_{field_index}",
                    height=100,
                    label_visibility="collapsed"
                )
                if 'career_data' in st.session_state and st.session_state.career_data:
                    st.session_state.career_data["careerFields"][field_key]["description"] = new_description
                
                # Roles
                roles = field_data.get("roles", [])
                if roles:
                    st.write("**Edit Roles:**")
                    for role_index, role in enumerate(roles):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            new_role_title = st.text_input(
                                f"Role {role_index + 1} Title",
                                value=role.get("title", "Role"),
                                key=f"role_title_{field_index}_{role_index}",
                                label_visibility="collapsed"
                            )
                        with col2:
                            new_role_desc = st.text_area(
                                f"Role {role_index + 1} Description",
                                value=role.get("description", "Description pending"),
                                key=f"role_desc_{field_index}_{role_index}",
                                height=80,
                                label_visibility="collapsed"
                            )
                        
                        # Update in session state
                        if 'career_data' in st.session_state and st.session_state.career_data:
                            st.session_state.career_data["careerFields"][field_key]["roles"][role_index]["title"] = new_role_title
                            st.session_state.career_data["careerFields"][field_key]["roles"][role_index]["description"] = new_role_desc
            else:
                # Read-only career field
                st.markdown(f'<h3 class="career-field-title">{field_data.get("title", "Career Field")}</h3>', unsafe_allow_html=True)
                
                # Alignment indicator with color coding
                alignment = field_data.get("alignment", "Unknown")
                if alignment.lower() == "high":
                    alignment_class = "alignment-high"
                elif "moderate" in alignment.lower():
                    alignment_class = "alignment-moderate"
                else:
                    alignment_class = "alignment-low"
                
                st.markdown(f'<p style="font-size: 17px;"><strong>Alignment:</strong> <span class="{alignment_class}">{alignment}</span></p>', unsafe_allow_html=True)
                
                # Description
                description = field_data.get("description", "Analysis in progress")
                st.markdown(f'<p style="font-size: 17px; color: #202124;">{description}</p>', unsafe_allow_html=True)
                
                # Roles
                roles = field_data.get("roles", [])
                if roles:
                    st.markdown('<h4 style="font-size: 17px; font-weight: 600; color: #202124; margin-bottom: 15px;">Examples of roles to explore:</h4>', unsafe_allow_html=True)
                    for role in roles:
                        role_title = role.get("title", "Role")
                        role_description = role.get("description", "Description pending")
                        st.markdown(f'''
                        <div class="career-role">
                            <div class="career-role-title">{role_title}</div>
                            <div class="career-role-desc">{role_description}</div>
                        </div>
                        ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─── DISPLAY REPORT ──────────────────────────────
if st.session_state.report_data:
    payload = st.session_state.report_data

    # Safely extract student info and personality type
    student_info = payload.get("studentInfo", {
        "name": st.session_state.name,
        "age": st.session_state.age,
        "grade": st.session_state.grade,
    })
    personality_type = payload.get("personalityType", "").strip()

    test_data = payload.get("testData", {})
    insights = payload.get("insightLines", [])

    # Clean up personality type
    if personality_type:
        personality_code = personality_type.split('\n')[-1].strip()
    else:
        personality_code = "N/A"
    
    # Header Section
    st.markdown('<h1 class="doc-title">Psychometric Assessment Report</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="student-header">', unsafe_allow_html=True)
    st.markdown(f'''
        <div>
            <div class="student-name">{student_info.get("name", "N/A")}</div>
            <div class="student-details">Age: {student_info.get("age", "N/A")} | Grade: {student_info.get("grade", "N/A")}</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Show edit mode indicator
    if st.session_state.edit_mode:
        st.markdown(
            '<div class="edit-notice"><strong>EDIT MODE:</strong> You can now modify the report data. Click "Save Changes" to confirm or "Reset Changes" to revert.</div>',
            unsafe_allow_html=True
        )
    
    # Test sections configuration
    test_configs = [
        {
            "key": "test16PersonalityData",
            "title": "MBTI-style Personality Type",
            "subtitle": "The Myers-Briggs Type Indicator (MBTI) is a personality test that categorizes people into 16 types based on four preference pairs: Extraversion vs. Introversion, Sensing vs. Intuition, Thinking vs. Feeling, and Judging vs. Perceiving. The MBTI tries to summarize how people naturally prefer to think, make decisions, and interact with the world around them. It's essentially attempting to capture your core psychological preferences - like whether you're energized by social interaction or solitude, whether you focus on concrete details or big-picture possibilities, and whether you prefer structure or flexibility in your daily life.",
            "headers": ["Preference", "Score", "Meaning"]
        },
        {
            "key": "high5Data",
            "title": "HIGH5 Strengths Themes",
            "subtitle": "The HIGH5 test identifies your top 5 natural strengths from a pool of 20 possible strength themes, such as Strategist, Empathizer, Achiever, or Commander. It focuses on uncovering your inherent talents and what energizes you most in work and life situations. HIGH5 is specifically designed to help you understand your unique combination of natural abilities and how to leverage them. The assessment ranks your top 5 strengths in order, giving you insights into where you have the greatest potential for success and fulfillment when you focus on using these natural talents.",
            "headers": ["Strength", "Domain", "Meaning"]
        },
        {
            "key": "bigFiveData",
            "title": "Big Five Personality Traits (OCEAN)",
            "subtitle": "The Big Five personality test measures five core personality dimensions that psychologists consider fundamental to human personality: Openness (creativity and openness to new experiences), Conscientiousness (organization and self-discipline), Extraversion (sociability and energy), Agreeableness (compassion and cooperation), and Vulnerability to Stress(emotional stability).",
            "headers": ["Trait", "Score", "Meaning"]
        },
        {
            "key": "riasecData",
            "title": "RIASEC Career Interest Themes",
            "subtitle": "The RIASEC test (also called the Holland Code) assesses your career interests and work preferences across six personality types: Realistic (hands-on, practical work), Investigative (analytical, research-oriented), Artistic (creative, expressive), Social (helping, teaching others), Enterprising (leading, persuading), and Conventional (organized, detail-oriented).",
            "headers": ["Theme", "Score", "Meaning"]
        }
    ]
    
    # Display each test section
    for i, config in enumerate(test_configs):
        rows = test_data.get(config["key"], [])
        if not rows:
            continue
        
        st.markdown(f'<h2 class="section-title">{config["title"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-subtitle">{config["subtitle"]}</div>', unsafe_allow_html=True)
        
        # Show editable or read-only table based on mode
        if st.session_state.edit_mode:
            # Show column headers for editing
            if config["key"] == "high5Data":
                col1, col2, col3 = st.columns([1, 1, 3])
                col1.write("**Strength**")
                col2.write("**Domain**")
                col3.write("**Meaning**")
            else:
                col1, col2, col3 = st.columns([1, 1, 3])
                col1.write("**Preference**")
                col2.write("**Score**")
                col3.write("**Meaning**")
            
            render_editable_table(config, rows, i)
        else:
            render_read_only_table(config, rows)
        
        # Add insight if available (editable in edit mode)
        if i < len(insights):
            if st.session_state.edit_mode:
                st.write("**Insight:**")
                new_insight = st.text_area(
                    "Edit insight",
                    value=insights[i].replace("INSIGHT: ", ""),
                    key=f"insight_{i}",
                    height=100,
                    label_visibility="collapsed"
                )
                # Update insight in session state
                st.session_state.report_data["insightLines"][i] = f"INSIGHT: {new_insight}"
            else:
                insight_text = insights[i].replace("INSIGHT: ", "")
                st.markdown(
                    f'<div class="insight-box"><span class="insight-label">Insight:</span> {insight_text}</div>',
                    unsafe_allow_html=True
                )
    
    # ─── CAREER ANALYSIS SECTION ─────────────────
    if st.session_state.career_data:
        render_career_section(st.session_state.career_data)
    
    # Add action buttons at the bottom - ALWAYS SHOW EDIT BUTTON
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Edit Report button centered at top - ALWAYS VISIBLE
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Edit Report" if not st.session_state.edit_mode else "View Report", 
                    use_container_width=True):
            st.session_state.edit_mode = not st.session_state.edit_mode
            st.rerun()
    
    # Edit mode controls (only show when in edit mode)
    if st.session_state.edit_mode:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Reset Changes", use_container_width=True):
                st.session_state.report_data = st.session_state.original_data.copy()
                # Also reset career data if it exists
                if 'original_career_data' in st.session_state:
                    st.session_state.career_data = st.session_state.original_career_data.copy()
                st.rerun()
        
        with col3:
            if st.button("Save Changes", use_container_width=True):
                st.session_state.original_data = st.session_state.report_data.copy()
                # Also save career data if it exists
                if st.session_state.career_data:
                    st.session_state.original_career_data = st.session_state.career_data.copy()
                st.success("Changes saved!")
                st.session_state.edit_mode = False
                st.rerun()
    
    # Only show action buttons if not currently processing career analysis
    if not st.session_state.career_analysis_requested:
        # Main action buttons
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.career_data:
            # CAREER DATA EXISTS: Show Career Reanalysis | New Assessment (side by side)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("Career Reanalysis", use_container_width=True):
                    st.session_state.career_data = None
                    st.session_state.career_analysis_requested = True
                    st.rerun()
            
            with col2:
                if st.button("New Assessment", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
        
        else:
            # NO CAREER DATA: Show Generate Career Pathways + New Assessment
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if not st.session_state.edit_mode:
                    if st.button("Generate Career Pathways", use_container_width=True):
                        st.session_state.career_analysis_requested = True
                        st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("New Assessment", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
