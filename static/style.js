window.onload=function(){

    const hamburger = document.querySelector(".menu-icon");
    const navMenu = document.querySelector(".menu");
    
    hamburger.addEventListener("click", () => {
      hamburger.classList.toggle("activeMenu");
      navMenu.classList.toggle("activeMenu");
    })
    
  }