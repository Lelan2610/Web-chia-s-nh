import streamlit as st
import json
import os
from datetime import datetime
import uuid

USER_DATA_FILE = "data/user_data.json"
COMMENTS_FILE = "data/comments.json"

# Tải dữ liệu
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    st.title("Web ảnh nhóm bạn thân")

    st.sidebar.header("Chọn thành viên trong nhóm")
    user_data = load_json(USER_DATA_FILE)
    comments = load_json(COMMENTS_FILE)

    usernames = list(user_data.keys())
    selected_user = st.sidebar.selectbox("Thành viên", usernames)

    st.header(f"Ảnh đặc biệt của {selected_user}")
    
    # Giao diện tải ảnh
    uploaded_image = st.file_uploader("Tải ảnh lên", type=["png", "jpg", "jpeg"])
    if st.button("Đăng ảnh") and uploaded_image:
        image_id = str(uuid.uuid4())
        file_path = f"data/{image_id}.jpg"
        with open(file_path, "wb") as f:
            f.write(uploaded_image.read())
        new_entry = {
            "image_id": image_id,
            "file_path": file_path,
            "time": datetime.now().isoformat()
        }
        user_data.setdefault(selected_user, []).append(new_entry)
        save_json(user_data, USER_DATA_FILE)
        st.success("Ảnh đã được đăng!")

    # Hiển thị ảnh + phần bình luận
    if selected_user in user_data:
        for photo in reversed(user_data[selected_user]):
            st.image(photo["file_path"], width=400, caption=f"Đăng lúc: {photo['time'][:19].replace('T', ' ')}")

            # Hiển thị bình luận
            st.subheader("Bình luận")
            photo_comments = comments.get(photo["image_id"], [])
            for c in photo_comments:
                st.markdown(f"**{c['name']}** ({c['time'][:19].replace('T', ' ')}): {c['comment']}")

            # Gửi bình luận mới
            st.markdown("---")
            with st.form(f"comment_form_{photo['image_id']}"):
                name = st.text_input("Tên", key=f"name_{photo['image_id']}")
                comment_text = st.text_area("Viết bình luận", key=f"comment_{photo['image_id']}")
                submitted = st.form_submit_button("Gửi bình luận")
                if submitted and name and comment_text:
                    new_comment = {
                        "name": name,
                        "comment": comment_text,
                        "time": datetime.now().isoformat()
                    }
                    comments.setdefault(photo["image_id"], []).append(new_comment)
                    save_json(comments, COMMENTS_FILE)
                    st.success("Đã gửi bình luận!")
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
