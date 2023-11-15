function editPost(postId) {
  // Hide the post content and edit button
  document.getElementById("post-content-" + postId).style.display = "none";
  this.style.display = "none"; // 'this' refers to the Edit button

  // Show the textarea and save button
  var content = document.getElementById("post-content-" + postId).innerText;
  var editTextArea = document.getElementById("edit-content-" + postId);
  var saveButton = document.getElementById("save-button-" + postId);
  editTextArea.style.display = "block";
  saveButton.style.display = "block";
  editTextArea.value = content;
}

function savePost(postId) {
  var updatedContent = document.getElementById("edit-content-" + postId).value;

  // Make an AJAX call to update the post
  fetch("/update_post/" + postId, {
    method: "POST",
    body: JSON.stringify({
      content: updatedContent,
    }),
    headers: {
      "X-CSRFToken": getCookie("csrftoken"), // Function to get CSRF token
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
  fetch(`/like/${postId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.log(data.error);
      } else {
        // Update the like button text with the new count
        document.querySelector(
          `#like-btn-${postId}`
        ).innerText = `${data.likes} Likes`;
      }
    })
    .catch((error) => console.log(error));
}
