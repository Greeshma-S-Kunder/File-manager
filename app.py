import os
import shutil
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from datetime import datetime

st.markdown(
"""
<style>
.custom-title {
    font-size: 39px;
    color: #0066cc;
    text-align: center;
    margin: 10px auto;
    padding: 52px;
}
.nav-button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
}
.nav-button:hover {
    background-color: #45a049;
    transform: scale(1.05);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
}
.dem {
    background-color: blue;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    border-radius: 4px;
    transition: background-color 0.3s;
    cursor: pointer;
}
.dem:hover {
    background-color: #45a049;
}
</style>
""",
    unsafe_allow_html=True,
)

def load_lottieus(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def organize_files(source_folder, destination_folder):
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        files = os.listdir(source_folder)
        recent_files = []
        for file in files:
            file_path = os.path.join(source_folder, file)
            if os.path.isfile(file_path):
                _, extension = os.path.splitext(file)
                extension = extension.lower()
                extension_folder = os.path.join(destination_folder, extension[1:])
                if not os.path.exists(extension_folder):
                    os.makedirs(extension_folder)
                shutil.move(file_path, os.path.join(extension_folder, file))
                recent_files.append(file)
        success_message = "Files organized successfully!"
        st.success(success_message)
        if recent_files:
            st.write("### Recently Accessed or Modified Files")
            st.write(recent_files)
    except FileNotFoundError:
        folder_not_found_message = f"Source folder or destination folder does not exist."
        st.error(folder_not_found_message)
        st.error("Please enter a valid folder path")
    except Exception as e:
        error_message = f"An error occurred: {e}"
        st.error(error_message)

def display_file_information(file_path):
    try:
        file_info = {
            "File Name": os.path.basename(file_path),
            "File Size (bytes)": os.path.getsize(file_path),
            "Creation Time": os.path.getctime(file_path),
            "Modification Time": os.path.getmtime(file_path),
        }
        st.write("### File Information")
        st.table(file_info)
    except Exception as e:
        st.error(f"Error getting file information: {e}")

def delete_file(file_path):
    try:
        if st.button("Delete File", key="delete_file"):
            confirmation = st.checkbox("I confirm that I want to delete this file.")
            if confirmation:
                os.remove(file_path)
                st.success("File deleted successfully!")
            else:
                st.warning("Please confirm the deletion.")
    except Exception as e:
        st.error(f"Error deleting file: {e}")

def rename_file(file_path):
    try:
        new_name = st.text_input("Enter new file name:", key="new_file_name")
        if st.button("Rename File", key="rename_file"):
            if new_name:
                new_path = os.path.join(os.path.dirname(file_path), new_name)
                os.rename(file_path, new_path)
                st.success("File renamed successfully!")
            else:
                st.warning("Please enter a new file name.")
    except Exception as e:
        st.error(f"Error renaming file: {e}")

with st.container():
    right, left = st.columns(2)
    with right:
        st.markdown('<h1 class="custom-title">File Manager</h1>', unsafe_allow_html=True)
    with left:
        lottie_coding = load_lottieus("https://lottie.host/55ecb3cd-41fe-4bc7-98e5-3db5905491f1/AQ7owZekPd.json")
        st_lottie(lottie_coding, height=200, key="coding")

st.write("---")

source_folder = st.text_input("Enter source folder path:")
destination_folder = st.text_input("Enter destination folder path:")

if st.button("Organize Files"):
    organize_files(source_folder, destination_folder)

st.write("#")
st.write("#")

selected_file = st.file_uploader("Choose a file for delete, rename, or display of file information", type=["txt", "png", "jpg", "jpeg"])

if selected_file:
    temp_file_path = f"temp.{selected_file.name.split('.')[-1]}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(selected_file.read())
    display_file_information(temp_file_path)
    delete_file(temp_file_path)
    rename_file(temp_file_path)

def page1():
    st.sidebar.markdown(
    """
    Welcome to File Manager!
    Here you can find information about the File Manager application and its features.
    - **File Organization**: Enter source and destination folders and click "Organize Files" to organize your files.
    - **File Operations**: Upload a file and perform operations like delete, rename, and view file information.
    Explore the features and enjoy using the File Manager!
    """
    )

def page2():
    st.sidebar.markdown(
    """
    ## Welcome to the Tips and Tricks section!
    **Tip 1: Efficient File Organization**
    - When organizing files, use meaningful folder names to make it easier to locate your files later.
    - Utilize subfolders for better categorization.
    **Tip 2: Quick File Information**
    - Click on a file to view its information, including file size, creation time, and modification time.
    - This can be helpful for managing disk space and tracking changes.
    **Tip 3: Batch Rename Files**
    - If you need to rename multiple files, organize them in a separate folder and use the "Organize Files" feature.
    - After organization, use the "Rename File" option to batch rename files efficiently.
    **Tip 4: Undo Deletions**
    - Be cautious when deleting files. Once deleted, files cannot be recovered directly from the File Manager.
    - Consider using backup solutions to prevent accidental data loss.
    """
    )

def page3():
    st.sidebar.markdown(
    """
    ## About Us
    Welcome to the File Manager! This application was developed by Greeshma Kunder, a student at St Joseph Engineering College Mangalore.
    **Contact Information**
    - Email: [greeshmakunder7@gmail.com](mailto:greeshmakunder7@gmail.com)
    - Phone: 8867253188
    **Purpose**
    The File Manager is designed to simplify file organization and management tasks. We aim to provide users with an intuitive interface and useful features to enhance their file management experience.
    **Contact Us**
    If you have any questions, suggestions, or feedback, feel free to reach out to us.
    Thank you for using the File Manager!
    """
    )

def page5():
    st.sidebar.markdown(
    """
    ## User Feedback
    We value your feedback! Please share your thoughts, suggestions, or report any issues you encounter while using the File Manager.
    **Feedback Form**
    Use the input box below to enter your feedback.
    """
    )
    with st.container():
        feedback_text = st.text_area("Enter your feedback here:", key="feedback_text", height=100)
        submit_feedback = st.button("Submit Feedback", key="submit_feedback")
        if submit_feedback:
            if feedback_text:
                st.success("Thank you for your feedback! We appreciate your input.")
                with open("user_feedback.txt", "a") as feedback_file:
                    feedback_file.write(f"\nFeedback ({datetime.now()}):\n{feedback_text}\n")
            else:
                st.warning("Please enter your feedback before submitting.")
        print("Feedback Text:", feedback_text)
        print("Submit Feedback:", submit_feedback)

def main():
    st.sidebar.title("Navigation Bar")
    page1_button = st.sidebar.button("Introduction", key="page1")
    page2_button = st.sidebar.button("Tips and Tricks", key="page2")
    page3_button = st.sidebar.button("About Us", key="page3")
    page5_button = st.sidebar.button("Feedback", key="page5")

    if page1_button:
        page1()
    elif page2_button:
        page2()
    elif page3_button:
        page3()
    elif page5_button:
        page5()

if __name__ == "__main__":
    main()
