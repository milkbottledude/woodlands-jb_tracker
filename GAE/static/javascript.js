document.addEventListener("DOMContentLoaded", function() {
    const needle = document.getElementById("needle");
    const angle = parseFloat(needle.getAttribute('data-angle'));
    
    // Update the angle
    needle.style.background = `
        conic-gradient(
            from ${angle}deg at 50% 50%, /* Dynamically set from angle */
            skyblue 2deg,
            white 3deg 8deg,
            skyblue 8deg 10deg,
            transparent 10deg
        )
    `;
});
