const DOMAIN = "http://127.0.0.1:8000";

const servicesUrl = `${DOMAIN}/api/services/`;
const testimonialsUrl = `${DOMAIN}/api/testimonials/`;
const faqsUrl = `${DOMAIN}/api/faqs/`;
const blogsUrl = `${DOMAIN}/api/blogs/`;
const sendMsgURL = `${DOMAIN}/api/contact/`;

const servicesDiv = document.getElementById("services-div");
const testimonialsDiv = document.getElementById("testimonials-div");
const faqListDiv = document.getElementById("faq-list");
const blogsDiv = document.getElementById("blogs-div");
const contactForm = document.getElementById("contact-form");
const sendBtn = document.getElementById("send-message-btn");

if (sendBtn) {
  sendBtn.addEventListener("click", sendMessage);
}

function getCookie(name) {
  let cookieValue = null;
  // console.log(document.cookie);
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function getAPIData(url, callback) {
  fetch(url, {
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
    },
    method: "GET",
  })
    .then((jresp) => jresp.json())
    .then((resp) => {
      callback(resp);
    })
    .catch((error) => {
      console.log(error);
    });
}

function sendMessage(e) {
  const rawData = Object.fromEntries(new FormData(contactForm).entries());
  const formData = new FormData();

  formData.append("name", rawData["name"]);
  formData.append("email", rawData["email"]);
  formData.append("subject", rawData["subject"]);
  formData.append("message", rawData["message"]);

  fetch(sendMsgURL, {
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
    },
    body: formData,
    method: "POST",
  }).then((response) =>
    response
      .json()
      .then((data) => {
        console.log(data);
        // contactForm.querySelector(".loading").classList.remove("d-block");
        if (response.ok) {
          e.preventDefault();
          contactForm.querySelector(".sent-message").classList.add("d-block");
        } else {
          console.log("inside else ");
          throw new Error(
            data
              ? data
              : "Form submission failed and no error message returned from: " +
                action
          );
        }
      })
      .catch((error) => {
        displayError(contactForm, error);
      })
  );
  return false;
}

function renderServicesDiv(resp) {
  if (resp.length != 0) {
    for (const el of resp) {
      servicesDiv.appendChild(createServiceDiv(el));
    }
  } else {
    servicesDiv.innerText = "No Services Found";
  }
}

function renderTestimonialDiv(resp) {
  if (resp.length != 0) {
    for (const el of resp) {
      testimonialsDiv.appendChild(createTestimonialDiv(el));
    }
  } else {
    testimonialsDiv.innerText = "No Testimonial Found";
  }
}

function renderFaqListDiv(resp) {
  if (resp.length != 0) {
    for (const el of resp) {
      faqListDiv.appendChild(createFaqsDiv(el));
    }
  } else {
    faqListDiv.innerText = "No Faqs Found";
  }
}

function renderBlogsDiv(resp) {
  if (resp.length != 0) {
    for (const el of resp) {
      blogsDiv.appendChild(createBlogDiv(el));
    }
  } else {
    blogsDiv.innerText = "No blog Found";
  }
}

function createServiceDiv(el) {
  let div = document.createElement("div");

  div.innerHTML = `
        
            <div class="service-item">
              <div class="img">
                <img src="${el.image}" class="img-fluid" alt="">
              </div>
              <div class="details position-relative">
                <i class="${el.icon}"></i>
                <a href="#" class="stretched-link">
                  <h3>${el.title}</h3>
                </a>
                <p>${el.desc}</p>
              </div>
            </div>
         
    `;
  div.setAttribute("class", "col-xl-4 col-md-6");
  div.setAttribute("data-aos", "zoom-in");
  div.setAttribute("data-aos-delay", "200");

  return div;
}

function createTestimonialDiv(el) {
  let div = document.createElement("div");

  div.innerHTML = `
  
  <div class="testimonial-item">
    <img src="${el.image}" class="testimonial-img" alt="">
    <h3>${el.name}</h3>
    <h4>${el.position}</h4>
    <div class="stars">
      <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
    </div>
    <p>
      <i class="bi bi-quote quote-icon-left"></i>
      ${el.quote}
      <i class="bi bi-quote quote-icon-right"></i>
    </p>
  </div>
    `;

  div.setAttribute("class", "swiper-slide");

  return div;
}

function createFaqsDiv(el) {
  let div = document.createElement("div");

  div.innerHTML = `
  
  <h3 class="accordion-header">
    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq-content-1">
      <i class="bi bi-question-circle question-icon"></i>
      ${el.question}
    </button>
  </h3>
  <div id="faq-content-1" class="accordion-collapse collapse" data-bs-parent="#faqlist">
    <div class="accordion-body">
    ${el.answer}
    </div>
  </div>
    `;

  div.setAttribute("class", "accordion-item");
  div.setAttribute("data-aos-", "fade-up");
  div.setAttribute("data-aos-delay", "200");

  return div;
}

function createBlogDiv(el) {
  let div = document.createElement("div");

  div.innerHTML = `
  
  <div class="post-box">
    <div class="post-img"><img src="${
      el.image
    }" style="width: auto; height: 195px;" alt=""></div>
    <div class="meta">
      <span class="post-date">${el.publish_date.substr(0, 10)}</span>
      <span class="post-author"> / ${el.publisher.first_name} ${
    el.publisher.last_name
  }</span>
    </div>
    <h3 class="post-title">${el.title}</h3>
    <p>${el.desc.substr(0, 50)}...</p>
    <a href="blog-details/?pk=${
      el.uid
    }" class="readmore stretched-link"><span>Read More</span><i class="bi bi-arrow-right"></i></a>
  </div>
    `;
  div.setAttribute("class", "col-lg-4");
  div.setAttribute("data-aos", "fade-up");
  div.setAttribute("data-aos-delay", "200");

  return div;
}

function displayError(thisForm, error) {
  thisForm.querySelector(".loading").classList.remove("d-block");
  thisForm.querySelector(".error-message").innerHTML = error;
  thisForm.querySelector(".error-message").classList.add("d-block");
}

getAPIData(servicesUrl, renderServicesDiv);
getAPIData(testimonialsUrl, renderTestimonialDiv);
getAPIData(faqsUrl, renderFaqListDiv);
getAPIData(blogsUrl, renderBlogsDiv);
