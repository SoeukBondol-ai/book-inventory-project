function goBack() {
    const lastVisited = sessionStorage.getItem('lastVisited');
    if (lastVisited) {
        window.location.href = lastVisited; // Redirect to last visited page
    } else {
        window.history.back(); // Fallback to history.back() if no stored URL
    }
}