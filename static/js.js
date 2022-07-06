


//pull the pathname from window location
const activePage = window.location.pathname;
console.log(window);
console.log(window.location);
console.log(activePage);

/*create an arey of the links in nav,
compare each to pathname and mark the one that is active
*/
const navLinks = document.querySelectorAll('nav a').forEach(link => {
  if(link.href.includes(`${activePage}`)){
    link.classList.add('active');
  }
});

function openNav() { /* open the menu when we click on the menu symbol*/
  document.getElementById("navigation").style.display = "block";
  document.getElementById("open").style.display = "none";
  document.getElementById("open_deails_page").style.display = "none";
}
function closeNav() { /* close the menu when we click on X*/
  document.getElementById("navigation").style.display = "none";
  document.getElementById("open").style.display = "block";
}

function showVideo(){
    document.getElementById("Australia_video").style.display="block";

}