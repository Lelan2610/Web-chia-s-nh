import streamlit as st
import os
from PIL import Image
import json

# Tạo thư mục lưu ảnh nếu chưa có
if not os.path.exists("images"):
    os.makedirs("images")

COMMENTS_FILE = "comments.json"

# Tạo file comments.json nếu chưa có
if not os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE, "w") as f:
        json.dump({}, f)

# Load dữ liệu bình luận
with open(COMMENTS_FILE, "r") as f:
    comments = json.load(f)

def save_comment(image_name, user_comment):
    if image_name not in comments:
        comments[image_name] = []
    comments[image_name].append(user_comment)
    with open(COMMENTS_FILE, "w") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

def show_comments(image_name):
    if image_name in comments:
        st.markdown("**Bình luận:**")
        for cmt in comments[image_name]:
            st.write(f"- {cmt}")

st.title("Cộng đồng chia sẻ ảnh")

# Upload ảnh
uploaded_file = st.file_uploader("Tải ảnh lên", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image_path = os.path.join("images", uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("Tải lên thành công!")

# Hiển thị tất cả ảnh
image_files = os.listdir("images")
for img_file in image_files:
    img_path = os.path.join("images", img_file)
    st.image(Image.open(img_path), caption=img_file, use_column_width=True)

    # Hiển thị bình luận
    show_comments(img_file)

    # Nhập bình luận
    with st.form(key=img_file):
        user_cmt = st.text_input("Bình luận về ảnh này:", key=f"cmt_{img_file}")
        submit = st.form_submit_button("Gửi bình luận")
        if submit and user_cmt:
            save_comment(img_file, user_cmt)
            st.success("Đã gửi bình luận!")
