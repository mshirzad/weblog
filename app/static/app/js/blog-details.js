const DOMAIN = "http://127.0.0.1:8000";

const commentsUrl = `${DOMAIN}/api/comments/`;

const blogID = document.getElementById("blog-uid").value;
const replyForm = document.getElementById("reply-comment-form");
const replyBtn = document.getElementById("send-comment-btn");

if (replyBtn) {
  replyBtn.addEventListener("click", sendComment);
}

function sendComment() {
  const rawData = Object.fromEntries(new FormData(replyForm).entries());
  const formData = new FormData();

  formData.append("name", rawData["name"]);
  formData.append("email", rawData["email"]);
  formData.append("comment_body", rawData["comment_body"]);
  formData.append("blog", String(blogID));
  console.log(formData);

  fetch(commentsUrl, {
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
    },
    body: formData,
    method: "POST",
  })
    .then((response) =>
      response.json().then((data) => {
        if (response.ok) {
          console.log(data);
        } else {
          console.log(data);
          // console.log(data);
        }
      })
    )
    .catch((error) => console.log(error));
}
