import tkinter as tk
from tkinter import messagebox
from auth import authenticate, get_user_details, add_user, delete_user, get_student_grades, get_student_eca, update_student_profile


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Authenticate the user
    role = authenticate(username, password)
    if role:
        user = get_user_details(username)
        if user:
            messagebox.showinfo("Login Successful",
                                f"Welcome, {user.full_name} ({user.role})!")
            if role == "admin":
                admin_dashboard(user)
            elif role == "student":
                student_dashboard(user)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def admin_dashboard(user):
    """
    Admin dashboard functionality.
    """
    def add_user_ui():
        """
        UI for adding a new user.
        """
        def submit():
            new_username = username_entry.get()
            new_full_name = full_name_entry.get()
            new_password = password_entry.get()
            new_role = role_var.get()

            if add_user(new_username, new_full_name, new_password, new_role):
                messagebox.showinfo("Success", "User added successfully!")
                add_user_window.destroy()
            else:
                messagebox.showerror(
                    "Error", "Failed to add user. Username might already exist.")

        add_user_window = tk.Toplevel()
        add_user_window.title("Add User")
        add_user_window.geometry("400x300")

        tk.Label(add_user_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(add_user_window)
        username_entry.pack(pady=5)

        tk.Label(add_user_window, text="Full Name:").pack(pady=5)
        full_name_entry = tk.Entry(add_user_window)
        full_name_entry.pack(pady=5)

        tk.Label(add_user_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(add_user_window, show="*")
        password_entry.pack(pady=5)

        tk.Label(add_user_window, text="Role:").pack(pady=5)
        role_var = tk.StringVar(value="student")
        tk.OptionMenu(add_user_window, role_var,
                      "admin", "student").pack(pady=5)

        tk.Button(add_user_window, text="Submit", command=submit).pack(pady=10)

    def delete_user_ui():
        """
        UI for deleting a user.
        """
        def submit():
            username_to_delete = username_entry.get()
            if delete_user(username_to_delete):
                messagebox.showinfo("Success", "User deleted successfully!")
                delete_user_window.destroy()
            else:
                messagebox.showerror(
                    "Error", "Failed to delete user. Username might not exist.")

        delete_user_window = tk.Toplevel()
        delete_user_window.title("Delete User")
        delete_user_window.geometry("300x200")

        tk.Label(delete_user_window, text="Username to delete:").pack(pady=5)
        username_entry = tk.Entry(delete_user_window)
        username_entry.pack(pady=5)

        tk.Button(delete_user_window, text="Submit",
                  command=submit).pack(pady=10)

    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("400x300")

    tk.Label(admin_window, text=f"Welcome, {user.full_name}!", font=(
        "Arial", 16)).pack(pady=10)

    tk.Button(admin_window, text="Add User", command=add_user_ui).pack(pady=10)
    tk.Button(admin_window, text="Delete User",
              command=delete_user_ui).pack(pady=10)


def student_dashboard(user):
    """
    Student dashboard functionality.
    """
    def view_details():
        """
        View personal details, grades, and extracurricular activities.
        """
        grades = get_student_grades(user.username)
        eca = get_student_eca(user.username)

        details_window = tk.Toplevel()
        details_window.title("View Details")
        details_window.geometry("400x400")

        tk.Label(details_window, text=f"Full Name: {user.full_name}", font=(
            "Arial", 12)).pack(pady=5)
        tk.Label(details_window, text=f"Role: {user.role}", font=(
            "Arial", 12)).pack(pady=5)

        tk.Label(details_window, text="Grades:",
                 font=("Arial", 12, "bold")).pack(pady=5)
        if grades:
            for i, grade in enumerate(grades, 1):
                tk.Label(details_window, text=f"Subject {i}: {grade}").pack()
        else:
            tk.Label(details_window, text="No grades found.").pack()

        tk.Label(details_window, text="ECA Activities:",
                 font=("Arial", 12, "bold")).pack(pady=5)
        if eca:
            for activity in eca:
                tk.Label(details_window, text=f"- {activity}").pack()
        else:
            tk.Label(details_window,
                     text="No extracurricular activities found.").pack()

    def update_profile():
        """
        Update the student's profile information.
        """
        def submit():
            new_full_name = full_name_entry.get()
            if update_student_profile(user.username, new_full_name):
                messagebox.showinfo("Success", "Profile updated successfully!")
                update_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to update profile.")

        update_window = tk.Toplevel()
        update_window.title("Update Profile")
        update_window.geometry("300x200")

        tk.Label(update_window, text="New Full Name:").pack(pady=5)
        full_name_entry = tk.Entry(update_window)
        full_name_entry.insert(0, user.full_name)  # Pre-fill with current name
        full_name_entry.pack(pady=5)

        tk.Button(update_window, text="Submit", command=submit).pack(pady=10)

    student_window = tk.Toplevel()
    student_window.title("Student Dashboard")
    student_window.geometry("400x300")

    tk.Label(student_window, text=f"Welcome, {user.full_name}!", font=(
        "Arial", 16)).pack(pady=10)

    tk.Button(student_window, text="View Details",
              command=view_details).pack(pady=10)
    tk.Button(student_window, text="Update Profile",
              command=update_profile).pack(pady=10)


def main():
    root = tk.Tk()
    root.title("Login System")
    root.geometry("900x700")

    # Create a frame to center the elements
    frame = tk.Frame(root)
    frame.pack(expand=True)

    # Username label and entry
    tk.Label(frame, text="Username:").pack(pady=5)
    global username_entry
    username_entry = tk.Entry(frame)
    username_entry.pack(pady=5)

    # Password label and entry
    tk.Label(frame, text="Password:").pack(pady=5)
    global password_entry
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(pady=5)

    # Login button
    tk.Button(frame, text="Login", command=login).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()