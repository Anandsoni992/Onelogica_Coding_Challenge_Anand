import streamlit as st
import pandas as pd

# Set the title of the app
st.title("HR Management System")

# Create a dropdown menu with the specified options
menu = st.selectbox(
    "Select an option:",
    ["Employee Information", "Time and Attendance", "Payroll Processing", "Performance Management",
     "Benefits Administration"]
)

# Sample data for the employee information table
# Using session state to keep the data persistent across user interactions
if "employee_data" not in st.session_state:
    st.session_state.employee_data = pd.DataFrame({
        "Name": ["Anand", "Abhishek", "Anshul"],
        "Contact Details": ["123-456-7890", "987-654-3210", "456-789-0123"],
        "Job Role": ["Manager", "Developer", "Analyst"],
        "Salary": [50000, 70000, 60000],
        "Performance History": ["Excellent", "Good", "Average"]
    })
    st.session_state.overtime_data = pd.DataFrame({
        "Name": ["Anand", "Abhishek", "Anshul"],
        "Contact Details": ["123-456-7890", "987-654-3210", "456-789-0123"],
        "Overtime Hours": [5, 10, 2]
    })
    st.session_state.leave_data = pd.DataFrame({
        "Name": ["Anand", "Abhishek", "Anshul"],
        "Contact Details": ["123-456-7890", "987-654-3210", "456-789-0123"],
        "Vacation Leave": [10, 5, 8],
        "Sick Leave": [2, 1, 3],
        "Personal Leave": [1, 2, 1]
    })

# Store password validation state in session state
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False


# Function to display the Employee Information section
def show_employee_information():
    # Display the employee data as a table
    st.subheader("Employee Information")
    st.table(st.session_state.employee_data)

    # Show password input field if access is not yet granted
    if not st.session_state.access_granted:
        password = st.text_input("Enter Admin Password to Edit Database(password is in ptt)", type="password")
        if st.button("Submit Password"):
            if password == "Anand":
                st.session_state.access_granted = True
                st.success("Access Granted! You can now add, remove, or edit employee data.")
            else:
                st.error("Password is incorrect!")

    # If access is granted, show options to add, remove, or edit data
    if st.session_state.access_granted:
        action = st.selectbox("Select Action:", ["Add Employee", "Remove Employee", "Edit Employee"])

        if action == "Add Employee":
            new_name = st.text_input("Name")
            new_contact = st.text_input("Contact Details")
            new_role = st.text_input("Job Role")
            new_salary = st.number_input("Salary", min_value=0)
            new_performance = st.selectbox("Performance History", ["Excellent", "Good", "Average", "Poor"])

            if st.button("Add"):
                # Add the new employee data to the table
                new_data = pd.DataFrame({
                    "Name": [new_name],
                    "Contact Details": [new_contact],
                    "Job Role": [new_role],
                    "Salary": [new_salary],
                    "Performance History": [new_performance]
                })
                st.session_state.employee_data = pd.concat([st.session_state.employee_data, new_data],
                                                           ignore_index=True)
                st.success("Employee added successfully!")
                st.table(st.session_state.employee_data)

        elif action == "Remove Employee":
            remove_name = st.selectbox("Select Employee to Remove", st.session_state.employee_data["Name"])
            if st.button("Remove"):
                st.session_state.employee_data = st.session_state.employee_data[
                    st.session_state.employee_data["Name"] != remove_name]
                st.success(f"Employee {remove_name} removed successfully!")
                st.table(st.session_state.employee_data)

        elif action == "Edit Employee":
            edit_name = st.selectbox("Select Employee to Edit", st.session_state.employee_data["Name"])
            edited_contact = st.text_input("New Contact Details", st.session_state.employee_data.loc[
                st.session_state.employee_data["Name"] == edit_name, "Contact Details"].values[0])
            edited_role = st.text_input("New Job Role", st.session_state.employee_data.loc[
                st.session_state.employee_data["Name"] == edit_name, "Job Role"].values[0])
            edited_salary = st.number_input("New Salary", min_value=0, value=int(st.session_state.employee_data.loc[
                                                                                     st.session_state.employee_data[
                                                                                         "Name"] == edit_name, "Salary"].values[
                                                                                     0]))
            edited_performance = st.selectbox("New Performance History", ["Excellent", "Good", "Average", "Poor"],
                                              index=["Excellent", "Good", "Average", "Poor"].index(
                                                  st.session_state.employee_data.loc[st.session_state.employee_data[
                                                                                         "Name"] == edit_name, "Performance History"].values[
                                                      0]))

            if st.button("Save Changes"):
                st.session_state.employee_data.loc[
                    st.session_state.employee_data["Name"] == edit_name, "Contact Details"] = edited_contact
                st.session_state.employee_data.loc[
                    st.session_state.employee_data["Name"] == edit_name, "Job Role"] = edited_role
                st.session_state.employee_data.loc[
                    st.session_state.employee_data["Name"] == edit_name, "Salary"] = edited_salary
                st.session_state.employee_data.loc[
                    st.session_state.employee_data["Name"] == edit_name, "Performance History"] = edited_performance
                st.success(f"Employee {edit_name} updated successfully!")
                st.table(st.session_state.employee_data)


def show_time_and_attendance():
    st.subheader("Time and Attendance")
    option = st.radio(
        "Select a Time and Attendance option:",
        ["Overtime Calculation and Management", "Leave Management", "Geofencing-Based Tracking"]
    )

    if option == "Overtime Calculation and Management":
        st.subheader("Overtime Calculation and Management")
        st.table(st.session_state.overtime_data)
        if not st.session_state.access_granted:
            password = st.text_input("Enter Admin Password to Edit Database(password is in ptt)", type="password")
            if st.button("Submit Password"):
                if password == "Anand":
                    st.session_state.access_granted = True
                    st.success("Access Granted! You can now add, remove, or edit employee data.")
                else:
                    st.error("Password is incorrect!")

        # If access is granted, show options to add, remove, or edit data
        if st.session_state.access_granted:
            action = st.selectbox("Select Action:", ["Add Employee", "Edit Overtime hours"])

            if action == "Add Employee":
                new_name = st.text_input("Name")
                new_contact = st.text_input("Contact Details")
                new_hours = st.text_input("Overtime Hours")

                if st.button("Add"):
                    # Add the new employee data to the table
                    new_data = pd.DataFrame({
                        "Name": [new_name],
                        "Contact Details": [new_contact],
                        "Overtime Hours": [new_hours]
                    })
                    st.session_state.overtime_data = pd.concat([st.session_state.overtime_data, new_data],
                                                               ignore_index=True)
                    st.success("Employee added successfully!")
                    st.table(st.session_state.overtime_data)

            elif action == "Edit Overtime hours":
                edit_name = st.selectbox("Select Employee to Edit", st.session_state.overtime_data["Name"])
                edited_contact = st.text_input("New Contact Details", st.session_state.overtime_data.loc[
                    st.session_state.overtime_data["Name"] == edit_name, "Contact Details"].values[0])
                edited_hours = st.text_input("New Overtime Hours", st.session_state.overtime_data.loc[
                    st.session_state.overtime_data["Name"] == edit_name, "Overtime Hours"].values[0])

                if st.button("Save Changes"):
                    st.session_state.overtime_data.loc[
                        st.session_state.overtime_data["Name"] == edit_name, "Contact Details"] = edited_contact
                    st.session_state.overtime_data.loc[
                        st.session_state.overtime_data["Name"] == edit_name, "Overtime Hours"] = edited_hours
                    st.success(f"Employee {edit_name} updated successfully!")
                    st.table(st.session_state.overtime_data)


    elif option == "Leave Management":
        st.subheader("Leave Management")
        st.table(st.session_state.leave_data)
        if not st.session_state.access_granted:
            password = st.text_input("Enter Admin Password to Edit Database(password is in ptt)", type="password")
            if st.button("Submit Password"):
                if password == "Anand":
                    st.session_state.access_granted = True
                    st.success("Access Granted! You can now add, remove, or edit employee data.")
                else:
                    st.error("Password is incorrect!")

        # If access is granted, show options to add, remove, or edit data
        if st.session_state.access_granted:
            action = st.selectbox("Select Action:", ["Add Employee", "Edit Leaves Taken"])

            if action == "Add Employee":
                new_name = st.text_input("Name")
                new_contact = st.text_input("Contact Details")
                new_vleave = st.text_input("Vacation Leave")
                new_sleave = st.text_input("Sick Leave")
                new_pleave = st.text_input("Personal Leave")

                if st.button("Add"):
                    # Add the new employee data to the table
                    new_data = pd.DataFrame({
                        "Name": [new_name],
                        "Contact Details": [new_contact],
                        "Vacation Leave": [new_vleave],
                        "Sick Leave": [new_sleave],
                        "Personal Leave": [new_pleave]

                    })
                    st.session_state.leave_data = pd.concat([st.session_state.leave_data, new_data],
                                                            ignore_index=True)
                    st.success("Employee added successfully!")
                    st.table(st.session_state.leave_data)

            elif action == "Edit Leaves Taken":
                edit_name = st.selectbox("Select Employee to Edit", st.session_state.leave_data["Name"])
                edited_contact = st.text_input("New Contact Details", st.session_state.leave_data.loc[
                    st.session_state.leave_data["Name"] == edit_name, "Contact Details"].values[0])
                edited_vleave = st.text_input("New Vacation Leave", st.session_state.leave_data.loc[
                    st.session_state.leave_data["Name"] == edit_name, "Vacation Leave"].values[0])
                edited_sleave = st.text_input("New Sick Leave", st.session_state.leave_data.loc[
                    st.session_state.leave_data["Name"] == edit_name, "Sick Leave"].values[0])
                edited_pleave = st.text_input("New Personal Leave", st.session_state.leave_data.loc[
                    st.session_state.leave_data["Name"] == edit_name, "Personal Leave"].values[0])

                if st.button("Save Changes"):
                    st.session_state.leave_data.loc[
                        st.session_state.leave_data["Name"] == edit_name, "Contact Details"] = edited_contact
                    st.session_state.leave_data.loc[
                        st.session_state.leave_data["Name"] == edit_name, "Vacation Leave"] = edited_vleave
                    st.session_state.leave_data.loc[
                        st.session_state.leave_data["Name"] == edit_name, "Sick Leave"] = edited_sleave
                    st.session_state.leave_data.loc[
                        st.session_state.leave_data["Name"] == edit_name, "Personal Leave"] = edited_pleave
                    st.success(f"Employee {edit_name} updated successfully!")
                    st.table(st.session_state.leave_data)

    elif option == "Geofencing-Based Tracking":
        st.subheader("Geofencing-Based Tracking")
        st.info("It is just a prototype. Please contact the maker (Anand Soni) for geofencing integration information.")


def show_payroll_information():
    st.subheader("Payroll Processing")

    # Ensure employee data is initialized in session state
    if "employee_data" not in st.session_state:
        st.error("No employee data found. Please ensure the Employee Information section is correctly set up.")
        return

    # Password input for secure access
    password = st.text_input("Enter Admin Password to Access Payroll Processing(password is in ptt)", type="password")

    # Dropdown for selecting an employee


    # Check for password validity
    if password == "Anand":
        st.success("Access Granted!")
        employee_name = st.selectbox("Select Employee", st.session_state.employee_data["Name"])

        # Show radio buttons for salary calculations or tax deductions
        option = st.radio("Select an option:", ["Salary Calculations", "Tax Deductions"])

        # Default values for salary calculation
        hourly_rate = st.session_state.get("hourly_rate", 10)
        fixed_salary = st.session_state.get("fixed_salary", 50000)
        commission = st.session_state.get("commission", 0)

        # Handle Salary Calculations
        if option == "Salary Calculations":
            st.subheader("Salary Calculations")
            st.write(f"Default hourly rate: ₹{hourly_rate}")
            st.write(f"Default fixed salary: ₹{fixed_salary}")
            st.write(f"Default commission: ₹{commission}")

            # Allow admin to change the values
            new_hourly_rate = st.number_input("Hourly Rate", min_value=0, value=hourly_rate)
            new_fixed_salary = st.number_input("Fixed Salary", min_value=0, value=fixed_salary)
            new_commission = st.number_input("Commission", min_value=0, value=commission)

            # Update session state with new values
            st.session_state.hourly_rate = new_hourly_rate
            st.session_state.fixed_salary = new_fixed_salary
            st.session_state.commission = new_commission

            st.success("Salary details updated successfully!")

        # Handle Tax Deductions
        elif option == "Tax Deductions":
            st.subheader("Tax Deductions")
            st.write("Following are the standard tax deductions as per Indian laws:")
            st.write("""
                - Provident Fund (PF): 12% of Basic Salary
                - Professional Tax: ₹200 per month (if salary exceeds ₹10,000)
                - Income Tax: As per Income Tax Slab
                """)

            # Provide a rough example of tax calculation for simplicity
            basic_salary = st.session_state.fixed_salary
            pf = 0.12 * basic_salary
            professional_tax = 200 if basic_salary > 10000 else 0
            income_tax = 0.1 * (basic_salary - 250000) if basic_salary > 250000 else 0  # Basic example of a slab

            st.write(f"Provident Fund: ₹{pf}")
            st.write(f"Professional Tax: ₹{professional_tax}")
            st.write(f"Estimated Income Tax: ₹{income_tax}")
        if employee_name:
            if st.button("Generate Payslip"):
                # Retrieve details of the selected employee
                employee = st.session_state.employee_data[st.session_state.employee_data["Name"] == employee_name].iloc[
                    0]
                name = employee["Name"]
                contact = employee["Contact Details"]
                role = employee["Job Role"]
                salary = st.session_state.fixed_salary
                commission = st.session_state.commission

                # Sample calculation for gross salary and total deductions
                gross_salary = salary + commission
                pf = 0.12 * salary
                professional_tax = 200 if salary > 10000 else 0
                income_tax = 0.1 * (salary - 250000) if salary > 250000 else 0
                total_deductions = pf + professional_tax + income_tax
                net_salary = gross_salary - total_deductions

                # Display the payslip in tabular format
                payslip_data = {
                    "Field": ["Name", "Contact Details", "Job Role", "Fixed Salary", "Commission", "Gross Salary",
                              "Provident Fund", "Professional Tax", "Income Tax", "Total Deductions", "Net Salary"],
                    "Details": [name, contact, role, f"₹{salary}", f"₹{commission}", f"₹{gross_salary}",
                                f"₹{pf}", f"₹{professional_tax}", f"₹{income_tax}", f"₹{total_deductions}",
                                f"₹{net_salary}"]
                }
                payslip_df = pd.DataFrame(payslip_data)
                st.table(payslip_df)

    elif password:
        st.error("Password is incorrect!")


def performance_management():
    st.subheader("Performance Management")

    # Radio buttons for selecting a category
    option = st.radio("Select an option for Performance Management:",
                      ["Goal Setting and Tracking", "Performance Reviews and Evaluations",
                       "Employee Development Plans"])

    if option == "Goal Setting and Tracking":
        st.subheader("Goal Setting and Tracking")

        # Dropdown to select an employee
        employee_name = st.selectbox("Select Employee", st.session_state.employee_data["Name"])

        # Simulated goal data (could be stored in session state)
        goal_data = {
            "Employee": ["Anand", "Abhishek", "Anshul"],
            "Goals": [
                "Increase sales by 20%",
                "Complete 5 training courses",
                "Improve customer satisfaction score by 15%"
            ],
            "Status": ["On Track", "At Risk", "Completed"]
        }
        goals_df = pd.DataFrame(goal_data)

        # Show goals in a table format
        st.table(goals_df)

        # Add functionality to update goals
        if st.button("Update Goals for " + employee_name):
            new_goal = st.text_input("Enter new goal for " + employee_name)
            if new_goal:
                st.success(f"Goal for {employee_name} updated to: {new_goal}")

    elif option == "Performance Reviews and Evaluations":
        st.subheader("Performance Reviews and Evaluations")

        # Dropdown to select an employee
        employee_name = st.selectbox("Select Employee", st.session_state.employee_data["Name"])

        # Simulated review data (could be stored in session state)
        review_data = {
            "Employee": ["Anand", "Abhishek", "Anshul"],
            "Review Date": ["2024-01-10", "2024-01-15", "2024-01-20"],
            "Rating": [4.5, 4.0, 5.0],
            "Comments": [
                "Excellent performance!",
                "Needs improvement in time management.",
                "Outstanding contributions to the team."
            ]
        }
        reviews_df = pd.DataFrame(review_data)

        # Show reviews in a table format
        st.table(reviews_df)

        # Functionality to submit a new review
        if st.button("Add Review for " + employee_name):
            rating = st.number_input("Enter Rating (1-5)", min_value=1.0, max_value=5.0, step=0.1)
            comments = st.text_area("Enter Comments")
            if st.button("Submit Review"):
                st.success(f"Review submitted for {employee_name}: Rating {rating}, Comments: {comments}")

    elif option == "Employee Development Plans":
        st.subheader("Employee Development Plans")

        # Dropdown to select an employee
        employee_name = st.selectbox("Select Employee", st.session_state.employee_data["Name"])

        # Simulated development plan data (could be stored in session state)
        development_data = {
            "Employee": ["Anand", "Abhishek", "Anshul"],
            "Skill to Develop": ["Sales Techniques", "Time Management", "Leadership Skills"],
            "Action Plan": [
                "Enroll in advanced sales training.",
                "Attend time management workshop.",
                "Participate in leadership seminars."
            ],
            "Target Completion Date": ["2024-06-30", "2024-03-31", "2024-05-15"]
        }
        dev_plan_df = pd.DataFrame(development_data)

        # Show development plans in a table format
        st.table(dev_plan_df)

        # Functionality to add a new development plan
        if st.button("Add Development Plan for " + employee_name):
            skill = st.text_input("Skill to Develop")
            action_plan = st.text_input("Action Plan")
            target_date = st.date_input("Target Completion Date")
            if st.button("Submit Development Plan"):
                st.success(
                    f"Development plan added for {employee_name}: Skill - {skill}, Action - {action_plan}, Target Date - {target_date}")


def benefits_management():
    st.subheader("Benefits Administration")

    # Radio buttons for selecting a category
    option = st.radio("Select an option for Benefits Administration:",
                      ["Management of Employee Benefits", "Benefit Enrollment and Changes",
                       "Tracking of Benefit Usage and Cost"])

    if option == "Management of Employee Benefits":
        st.subheader("Management of Employee Benefits")

        # Simulated benefits data (could be stored in session state)
        benefits_data = {
            "Employee": ["Anand", "Abhishek", "Anshul"],
            "Health Insurance": ["Premium Plan", "Basic Plan", "Premium Plan"],
            "Retirement Plan": ["401(k)", "Pension Plan", "401(k)"]
        }
        benefits_df = pd.DataFrame(benefits_data)

        # Show benefits in a table format
        st.table(benefits_df)

        # Functionality to update benefits
        employee_name = st.selectbox("Select Employee to Update Benefits", benefits_df["Employee"])
        health_insurance = st.selectbox("Select Health Insurance Plan", ["Premium Plan", "Basic Plan"])
        retirement_plan = st.selectbox("Select Retirement Plan", ["401(k)", "Pension Plan"])

        if st.button("Update Benefits for " + employee_name):
            st.success(
                f"Benefits updated for {employee_name}: Health Insurance - {health_insurance}, Retirement Plan - {retirement_plan}")

    elif option == "Benefit Enrollment and Changes":
        st.subheader("Benefit Enrollment and Changes")

        # Dropdown to select an employee
        employee_name = st.selectbox("Select Employee", ["Anand", "Abhishek", "Anshul"])

        # Enrollment form for new benefits
        st.write(f"Enroll {employee_name} in benefits:")
        health_insurance = st.selectbox("Select Health Insurance Plan", ["Premium Plan", "Basic Plan"])
        retirement_plan = st.selectbox("Select Retirement Plan", ["401(k)", "Pension Plan"])

        if st.button("Enroll Benefits"):
            st.success(
                f"{employee_name} has been enrolled in: Health Insurance - {health_insurance}, Retirement Plan - {retirement_plan}")

    elif option == "Tracking of Benefit Usage and Cost":
        st.subheader("Tracking of Benefit Usage and Cost")

        # Simulated usage data (could be stored in session state)
        usage_data = {
            "Employee": ["Anand", "Abhishek", "Anshul"],
            "Health Insurance Claims": [1200, 800, 1500],
            "Retirement Contributions": [5000, 3000, 7000]
        }
        usage_df = pd.DataFrame(usage_data)

        # Show usage data in a table format
        st.table(usage_df)

        # Functionality to add new usage entry
        employee_name = st.selectbox("Select Employee for Usage Entry", usage_df["Employee"])
        claims = st.number_input("Enter Health Insurance Claims Amount", min_value=0)
        contributions = st.number_input("Enter Retirement Contributions Amount", min_value=0)

        if st.button("Add Usage Entry"):
            st.success(f"Usage entry added for {employee_name}: Claims - {claims}, Contributions - {contributions}")


# Display the appropriate section based on the selected option
if menu == "Employee Information":
    show_employee_information()
elif menu == "Time and Attendance":
    show_time_and_attendance()
elif menu == "Payroll Processing":
    show_payroll_information()
elif menu == "Performance Management":
    performance_management()
elif menu == "Benefits Administration":
    benefits_management()
