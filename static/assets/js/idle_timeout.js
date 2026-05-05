(function () {
  const IDLE_TIMEOUT_MS = 4.5 * 60 * 1000; // 4 min 30 sec — fires before server session (5 min)
  const LOGIN_URL = window.IDLE_LOGIN_URL;   // injected by Django template
  const STORAGE_KEY = "rtdms_last_active";

  let timer;

  function redirectToLogin() {
    window.location.href = LOGIN_URL;
  }

  function resetTimer() {
    localStorage.setItem(STORAGE_KEY, Date.now().toString());
    clearTimeout(timer);
    timer = setTimeout(redirectToLogin, IDLE_TIMEOUT_MS);
  }

  // All meaningful user activity events
  ["mousemove", "mousedown", "keypress", "touchstart", "scroll", "click"].forEach(function (evt) {
    document.addEventListener(evt, resetTimer, { passive: true });
  });

  // Cross-tab sync: if the user is active in another tab, reset this tab's timer too
  window.addEventListener("storage", function (e) {
    if (e.key !== STORAGE_KEY) return;
    const lastActive = parseInt(e.newValue, 10);
    const remaining = IDLE_TIMEOUT_MS - (Date.now() - lastActive);
    clearTimeout(timer);
    if (remaining <= 0) {
      redirectToLogin();
    } else {
      timer = setTimeout(redirectToLogin, remaining);
    }
  });

  // Start the clock
  resetTimer();
})();