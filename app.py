import streamlit as st
import pandas as pd
from datetime import datetime

# Custom layers ko import karna
from database import load_data, save_data
from my_algorithm import merge_sort, binary_search
import policy_engine as pe

if 'student_list' not in st.session_state:
    st.session_state.student_list = load_data()

# --- STREAMLIT PAGE INITIAL SETUP ---
st.set_page_config(page_title="Fees System", layout="centered")

# --- UI STYLE ENGINE: GLASSMORPHISM & THEME OPTIMIZATION ---
# Injecting custom transparent blur styles to achieve a modern premium aesthetic
st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    
    /* Light mode override based on user system preferences */
    @media (prefers-color-scheme: light) {
        .stApp {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            color: #0f172a;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            color: #0f172a !important;
        }
    }

    /* Glassmorphic card structure */
    .glass-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Standard interactive widget enhancements */
    .stButton>button {
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- APP SYSTEM TITLE ---
st.markdown('<div class="glass-card"><h1 style="text-align: center; margin:0;">💳 Fees Management System</h1><p style="text-align: center; margin:5px 0 0 0; opacity:0.8;">Simple & Secure University Ledger</p></div>', unsafe_allow_html=True)

# --- USER ROUTING BLOCK (AUTHENTICATION) ---
if 'role' not in st.session_state:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Login Portal")
    role_choice = st.radio("Choose Your Role", ["Student Dashboard", "University Admin"])
    
    if role_choice == "University Admin":
        username = st.text_input("Enter Username")
        password = st.text_input("Enter Password", type="password")
        if st.button("Login as Admin", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.role = "admin"
                st.rerun()
            else: 
                st.error("Wrong Username or Password")
                
    elif role_choice == "Student Dashboard":
        student_roll_input = st.text_input("Enter Your Roll Number (e.g., BSE-23F-101)").strip().upper()
        if st.button("Open Dashboard", use_container_width=True):
            sorted_list = sorted(st.session_state.student_list, key=lambda x: x['roll_no'])
            idx = binary_search(sorted_list, student_roll_input)
            if idx != -1:
                st.session_state.role = "student"
                st.session_state.student_roll = student_roll_input
                st.rerun()
            else: 
                st.error("Roll Number Not Found in Records")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Header Layout with Logout Trigger
    col_title, col_logout = st.columns([4, 1])
    with col_logout:
        if st.button("🔒 Logout", use_container_width=True):
            del st.session_state.role
            if 'student_roll' in st.session_state: del st.session_state.student_roll
            st.rerun()

    # --- MODULE 1: STUDENT VIEW LAYOUT ---
    if st.session_state.role == "student":
        with col_title: st.subheader("Student Personal Dashboard")
        
        student = next(x for x in st.session_state.student_list if x['roll_no'] == st.session_state.student_roll)
        remaining_balance = student['total_fees'] - student['fees_paid']
        
        st.success(f"Welcome back, {student['name']}!")
        
        # Transparent UI metrics cards
        st.markdown(f"""
        <div class="glass-card">
            <table style="width:100%; border:none; border-collapse: collapse;">
                <tr>
                    <td style="padding:10px; font-weight:bold;">Roll Number:</td><td>{student['roll_no']}</td>
                    <td style="padding:10px; font-weight:bold;">Total Fees:</td><td>Rs. {student['total_fees']}</td>
                </tr>
                <tr>
                    <td style="padding:10px; font-weight:bold;">Current Semester:</td><td>Semester {student['semester']}</td>
                    <td style="padding:10px; font-weight:bold;">Fees Paid:</td><td>Rs. {student['fees_paid']}</td>
                </tr>
                <tr>
                    <td style="padding:10px; font-weight:bold;">Registered Credits:</td><td>{student['credit_hours']} Hrs</td>
                    <td style="padding:10px; font-weight:bold; color:#f43f5e;">Pending Dues:</td><td style="font-weight:bold; color:#f43f5e;">Rs. {remaining_balance}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🖨️ Official Fee Voucher")
        with st.container(border=True):
            st.markdown("### **SMART UNIVERSITY OFFICIAL CHALLAN**")
            st.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')} | **Status:** {'PAID' if remaining_balance <= 0 else 'UNPAID'}")
            st.markdown("---")
            v_col1, v_col2 = st.columns(2)
            with v_col1:
                st.write(f"**Name:** {student['name']}")
                st.write(f"**Roll No:** {student['roll_no']}")
                st.write(f"**Program Name:** {student['course']}")
                st.write(f"**Challan ID:** `{student['receipt']}`")
            with v_col2:
                st.write(f"**Tuition Fee Math:** {student['credit_hours']} Hrs × Rs. {pe.FEES_PER_CREDIT_HOUR}")
                if int(student['semester']) == 1:
                    st.write(f"**Admission Charges:** Rs. {pe.ADMISSION_FEE_RATE}")
                    st.write(f"**Security Deposit:** Rs. {pe.SECURITY_DEPOSIT_RATE}")
                else:
                    st.write(f"**Activity Charges:** Rs. {pe.ACTIVITY_CHARGES_RATE}")
                st.markdown(f"### **Net Payable Amount: Rs. {remaining_balance}**")
        
        if st.button("Print Voucher Leaf", use_container_width=True):
            st.markdown("<script>window.print();</script>", unsafe_allow_html=True)

    # --- MODULE 2: ADMINISTRATIVE VIEW LAYOUT ---
    elif st.session_state.role == "admin":
        with col_title: st.subheader("Admin Control Panel")
        
        # Plain simple clean text menu tabs
        menu = st.tabs(["📋 View All Students", "➕ Add New Student", "💵 Receive Fees Payment", "❌ Remove Student"])
        
        # TAB 1: DISPLAY, SORT, SEARCH
        with menu[0]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            if not st.session_state.student_list: 
                st.info("No records present in the database file.")
            else:
                col_s1, col_s2 = st.columns([1, 2])
                with col_s1:
                    if st.button("⚡ Sort List (Merge Sort)", use_container_width=True):
                        st.session_state.student_list = merge_sort(st.session_state.student_list)
                        save_data(st.session_state.student_list)
                        st.success("List Sorted Successfully!")
                with col_s2:
                    search_roll = st.text_input("Type Roll Number to Search", key="search").strip().upper()
                    if st.button("Run Binary Search Lookup", use_container_width=True):
                        idx = binary_search(st.session_state.student_list, search_roll)
                        if idx != -1: 
                            st.json(st.session_state.student_list[idx])
                        else: 
                            st.error("No Match Found! (Ensure database is sorted first)")
                
                df = pd.DataFrame(st.session_state.student_list)
                df['Remaining Dues'] = df['total_fees'] - df['fees_paid']
                st.dataframe(df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # TAB 2: AUTOMATED POLICY ADMISSION INGESTION
        with menu[1]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### Register New Student Profile")
            with st.form("add_form", clear_on_submit=True):
                name = st.text_input("Student Full Name")
                col_spec1, col_spec2 = st.columns(2)
                with col_spec1: dept = st.selectbox("Select Department", ["BSE", "BSCS", "BBA", "A&F"])
                with col_spec2: batch = st.selectbox("Select Admission Batch (Fall Only)", ["23F", "24F", "25F", "26F"])
                
                course = st.text_input("Active Semester Term Name (e.g., Spring 2026)")
                credit_hours = st.number_input("Registered Credit Hours", min_value=1, max_value=21, value=15, step=1)
                initial_paid = st.number_input("Initial Fee Amount Deposited (Rs.)", min_value=0.0, value=0.0)
                
                if st.form_submit_button("Calculate Fees & Create Profile", use_container_width=True):
                    if not name or not course: 
                        st.error("Input Warning: Fields cannot be left empty.")
                    else:
                        # Auto runtime calculation logic matching the current year calendar
                        semester_calculated = 1
                        if batch == "23F": semester_calculated = 6
                        elif batch == "24F": semester_calculated = 4
                        elif batch == "25F": semester_calculated = 2
                        elif batch == "26F": semester_calculated = 1

                        total_computed = pe.calculate_fees(semester_calculated, credit_hours)
                        
                        if initial_paid > total_computed: 
                            st.error("Calculation Error: Paid amount cannot exceed total structural bill.")
                        else:
                            generated_roll = pe.generate_roll_number(dept, batch, st.session_state.student_list)
                            generated_receipt = pe.generate_bank_receipt(dept, batch)
                            
                            new_student = {
                                "roll_no": generated_roll, "name": name, "course": course,
                                "semester": int(semester_calculated), "credit_hours": int(credit_hours),
                                "fees_paid": float(initial_paid), "total_fees": total_computed, "receipt": generated_receipt
                            }
                            st.session_state.student_list.append(new_student)
                            save_data(st.session_state.student_list)
                            st.success(f"Profile Created! Assigned Roll No: {generated_roll} | Auto-Semester: {semester_calculated}")
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # TAB 3: LEDGER UPDATE RECONCILIATION
        with menu[2]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            up_roll = st.text_input("Enter Student Roll Number to Update Balance", key="up").strip().upper()
            student_found = next((x for x in st.session_state.student_list if x['roll_no'] == up_roll), None)
            if student_found:
                st.write(f"Account Active: **{student_found['name']}** | Total Fee Bill: Rs. {student_found['total_fees']}")
                new_paid = st.number_input(f"Enter New Total Paid Amount (Current Total: Rs. {student_found['fees_paid']})", min_value=0.0, max_value=student_found['total_fees'])
                if st.button("Update Fees Ledger", use_container_width=True):
                    student_found['fees_paid'] = new_paid
                    save_data(st.session_state.student_list)
                    st.success("Payment Logged Successfully!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # TAB 4: DELETION NODE WIPE
        with menu[3]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            del_roll = st.text_input("Enter Student Roll Number to Delete", key="del").strip().upper()
            if st.button("Permanently Delete Record", type="primary", use_container_width=True):
                st.session_state.student_list = [x for x in st.session_state.student_list if x['roll_no'] != del_roll]
                save_data(st.session_state.student_list)
                st.success("Record Deleted and Pruned Successfully.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)