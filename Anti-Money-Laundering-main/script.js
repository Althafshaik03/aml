document.addEventListener('DOMContentLoaded', function() {
    // Create an audio element and preload it
    const audio = new Audio('click-sound.mp3'); // Replace with the correct path to your click sound file
    audio.preload = 'auto';  // Make sure the sound is preloaded when the page loads

    // Ensure the audio is fully loaded before any clicks
    audio.addEventListener('canplaythrough', function() {
        // Now the sound is ready to be played without delay
        console.log('Audio ready to play');
    });

    // Add click sound effect to all 'a' elements (links)
    const buttons = document.querySelectorAll('a');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            audio.currentTime = 0;  // Rewind to the start, in case it's already playing
            audio.play(); // Play the sound immediately
        });
    });
});
