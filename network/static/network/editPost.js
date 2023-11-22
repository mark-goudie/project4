function editPost(postId, editButton) {
  var postContent = document.getElementById("post-content-" + postId);
  if (postContent) {
    postContent.style.display = "none";
  }
  editButton.style.display = "none";

  var editTextArea = document.getElementById("edit-content-" + postId);
  var saveButton = document.getElementById("save-button-" + postId);
  if (editTextArea && saveButton) {
    editTextArea.style.display = "block";
    saveButton.style.display = "block";
    editTextArea.value = postContent.innerText;
  }
}

function savePost(postId) {
  var updatedContent = document.getElementById("edit-content-" + postId).value;

  fetch("/update_post/" + postId, {
    method: "POST",
    body: JSON.stringify({
      content: updatedContent,
    }),
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((result) => {
      // Update the post content on the page
      document.getElementById("post-content-" + postId).innerText =
        updatedContent;
      document.getElementById("post-content-" + postId).style.display = "block";
      document.getElementById("edit-content-" + postId).style.display = "none";
      document.getElementById("save-button-" + postId).style.display = "none";
      document.getElementById(`edit-button-${postId}`).style.display =
        "inline-block";
    })
    .catch((error) => {
      console.log(error);
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function toggleLike(postId) {
  const likeButton = document.getElementById(`like-btn-${postId}`);
  const isLiked = likeButton.getAttribute("data-liked") === "true";

  fetch(`/like/${postId}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      like: !isLiked,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.liked) {
        likeButton.classList.add("liked", "btn-primary");
        likeButton.classList.remove("unliked", "btn-secondary");
        likeButton.setAttribute("data-liked", "true");
      } else {
        likeButton.classList.add("unliked", "btn-secondary");
        likeButton.classList.remove("liked", "btn-primary");
        likeButton.setAttribute("data-liked", "false");
      }
      likeButton.innerHTML = `Like <span class="badge bg-secondary">${data.likes}</span>`;
    })
    .catch((error) => console.log(error));
}
