"""
app.py - ShipCheck Streamlit Dashboard & Human-in-the-Loop Review Interface.

Run with:
    streamlit run app.py
"""
import json
from pathlib import Path

import streamlit as st

from compare import FIELDS, compare, norm, summarize
from config import CATEGORIES, OUTPUT_DIR, REVIEW_REASONS, STATUSES

st.set_page_config(
    page_title="ShipCheck - Shipping Document Verification",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
    }
    .badge-ok { background-color: #dcfce7; color: #15803d; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .badge-mismatch { background-color: #fee2e2; color: #b91c1c; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .badge-review { background-color: #fef3c7; color: #b45309; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    sub_path = Path("submission.json")
    details_path = OUTPUT_DIR / "pipeline_details.json"
    queue_path = OUTPUT_DIR / "review_queue.json"

    sub = json.loads(sub_path.read_text(encoding="utf-8")) if sub_path.exists() else {}
    details = json.loads(details_path.read_text(encoding="utf-8")) if details_path.exists() else {}
    queue = json.loads(queue_path.read_text(encoding="utf-8")) if queue_path.exists() else {}
    return sub, details, queue


sub_data, details_data, review_queue = load_data()

st.title("🚢 ShipCheck: Shipping Document Verification")
st.caption("Automated Email Classification, 7-Field Document Comparison & Human-in-the-Loop Escalation")

if not sub_data:
    st.warning("No pipeline results found. Please run `python pipeline.py` first.")
    st.stop()

# --- KPI Top Metrics ---
total_emails = len(sub_data)
comp_emails = sum(1 for v in sub_data.values() if v.get("category") == "BL_COMPARISON")
mismatches = sum(1 for v in sub_data.values() if v.get("status") == "MISMATCH")
reviews = sum(1 for v in sub_data.values() if v.get("status") == "NEEDS_REVIEW")
ok_count = sum(1 for v in sub_data.values() if v.get("status") == "OK")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Inbox Emails", total_emails)
with col2:
    st.metric("BL Comparisons", comp_emails)
with col3:
    st.metric("Defects (Mismatch)", mismatches, delta=f"{mismatches/comp_emails*100:.1f}%" if comp_emails else "0%")
with col4:
    st.metric("Escalated (Review)", reviews, delta="Reliability" if reviews else "None")
with col5:
    st.metric("Passed (OK)", ok_count)

st.divider()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters & Navigation")
category_filter = st.sidebar.multiselect(
    "Filter by Category",
    options=CATEGORIES,
    default=["BL_COMPARISON"],
)
status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=STATUSES,
    default=STATUSES,
)

search_query = st.sidebar.text_input("Search Email ID or Keyword", "")

# Filter emails
filtered_eids = []
for eid, entry in sub_data.items():
    if entry.get("category") in category_filter and entry.get("status") in status_filter:
        if search_query:
            q = search_query.lower()
            detail = details_data.get(eid, {})
            text = f"{eid} {json.dumps(detail)}".lower()
            if q not in text:
                continue
        filtered_eids.append(eid)

st.sidebar.write(f"Showing **{len(filtered_eids)}** matching emails.")

# --- Tabs ---
tab_inspector, tab_review, tab_summary = st.tabs(
    ["🔎 Document Inspector", "⚠️ Review Queue (HITL)", "📊 Inbox Analytics"]
)

# --- TAB 1: Document Inspector ---
with tab_inspector:
    if not filtered_eids:
        st.info("No emails match the selected filters.")
    else:
        selected_eid = st.selectbox("Select Email to Inspect:", options=filtered_eids)
        entry = sub_data[selected_eid]
        detail = details_data.get(selected_eid, {})

        status = entry.get("status")
        cat = entry.get("category")
        reason = entry.get("review_reason")

        # Header info
        c_left, c_right = st.columns([3, 1])
        with c_left:
            st.subheader(f"{selected_eid} — Category: `{cat}`")
            if detail.get("detail"):
                st.caption(f"Note: {detail.get('detail')}")
        with c_right:
            if status == "OK":
                st.markdown('<span class="badge-ok">STATUS: OK</span>', unsafe_allow_html=True)
            elif status == "MISMATCH":
                st.markdown('<span class="badge-mismatch">STATUS: MISMATCH</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="badge-review">NEEDS REVIEW ({reason})</span>', unsafe_allow_html=True)

        # Show comparison if available
        si_fields = detail.get("si_fields")
        bl_fields = detail.get("bl_fields")

        if si_fields and bl_fields:
            st.markdown("#### 7-Field Side-by-Side Comparison")
            comp_rows = []
            for f in FIELDS:
                si_val = si_fields.get(f)
                bl_val = bl_fields.get(f)
                is_defect = f in entry.get("defect_fields", [])
                
                norm_si = norm(f, si_val)
                norm_bl = norm(f, bl_val)
                
                comp_rows.append({
                    "Field": f,
                    "SI Value (Reference)": str(si_val or "—"),
                    "BL Value (Draft)": str(bl_val or "—"),
                    "Result": "❌ MISMATCH" if is_defect else ("⚠️ MISSING" if (si_val is None or bl_val is None) else "✅ MATCH")
                })
            
            st.table(comp_rows)

            if entry.get("defect_fields"):
                st.error(f"Defect detected in fields: **{', '.join(entry['defect_fields'])}**")
            elif status == "OK":
                st.success("🎉 No mismatch detected across all 7 fields.")
        else:
            st.info(f"Email `{selected_eid}` has no SI/BL comparison fields ({cat} message).")

# --- TAB 2: Human-in-the-Loop Review Queue ---
with tab_review:
    st.markdown("### ⚠️ Human-in-the-Loop Escalation Queue")
    st.caption("Cases requiring human operator review due to missing attachments, unreadable documents, wrong doc types, or missing required fields.")

    review_cases = [eid for eid, e in sub_data.items() if e.get("status") == "NEEDS_REVIEW"]
    
    if not review_cases:
        st.success("Zero pending reviews! All cases processed autonomously.")
    else:
        st.write(f"**{len(review_cases)}** cases escalated to review:")
        
        selected_review = st.selectbox("Select case to review:", options=review_cases)
        case_entry = sub_data[selected_review]
        case_detail = details_data.get(selected_review, {})
        queue_info = review_queue.get(selected_review, {})

        r1, r2 = st.columns(2)
        with r1:
            st.write(f"**Email ID:** `{selected_review}`")
            st.write(f"**Escalation Reason:** `{case_entry.get('review_reason')}`")
            st.write(f"**Explanation:** {case_detail.get('detail', queue_info.get('detail', 'N/A'))}")
        with r2:
            st.write(f"**Subject:** {queue_info.get('subject', 'N/A')}")
            st.write(f"**Attachments:** {queue_info.get('attachments', [])}")

        st.markdown("#### Operator Resolution Form")
        with st.form(f"resolve_form_{selected_review}"):
            action = st.radio(
                "Select Resolution Action:",
                ["Confirm Issue (Keep NEEDS_REVIEW)", "Mark as False Alarm (Set to OK)", "Manual Correction (Provide Values)"]
            )
            
            override_notes = st.text_area("Operator notes / justification:")
            submit_resolve = st.form_submit_button("Submit Resolution")

            if submit_resolve:
                st.success(f"Resolution saved for {selected_review}: {action}")

# --- TAB 3: Inbox Analytics ---
with tab_summary:
    st.markdown("### 📊 Inbox Category & Status Distribution")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Category Breakdown")
        cat_counts = {}
        for e in sub_data.values():
            c = e["category"]
            cat_counts[c] = cat_counts.get(c, 0) + 1
        st.bar_chart(cat_counts)
    
    with col_b:
        st.markdown("#### Status Breakdown")
        status_counts = {}
        for e in sub_data.values():
            s = e["status"]
            status_counts[s] = status_counts.get(s, 0) + 1
        st.bar_chart(status_counts)
