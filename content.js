// Runs inside the page
console.log("The page URL is:", window.location.href);

// Makes it so that script should run when there is a physical
// change to the screen
document.body.style.border = "5px solid red";

// Example: display it on the page
let banner = document.createElement("div");
banner.textContent = "URL: " + window.location.href;
banner.style.cssText = "position:fixed;top:0;left:0;background:yellow;padding:5px;z-index:9999;";
document.body.appendChild(banner);



