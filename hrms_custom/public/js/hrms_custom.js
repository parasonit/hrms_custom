setTimeout(() => {
    const helpdeskLink = document.querySelector('.item-anchor[href="/app/helpdesk"]');    
    // Check if the link exists and update the href attribute
    if (helpdeskLink) {
        // Update the href to the new URL
        helpdeskLink.href = '/helpdesk'; 
    
        // Ensure it redirects when clicked
        helpdeskLink.addEventListener('click', function(event) {
            console.log("working121")
            // Optional: You can add logic here to track the click or perform any other action
            window.location.href = '/helpdesk'; // Redirect to the new URL
        });
    }
}, 1000);