(function initPwa() {
  const installBtn = document.getElementById('install-app-btn');
  let deferredInstallPrompt = null;

  function hideInstallButton() {
    if (installBtn) {
      installBtn.classList.add('hidden');
    }
  }

  function showInstallButton() {
    if (installBtn) {
      installBtn.classList.remove('hidden');
    }
  }

  function isInstalled() {
    return (
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true
    );
  }

  if (isInstalled()) {
    hideInstallButton();
  }

  window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    deferredInstallPrompt = event;
    if (!isInstalled()) {
      showInstallButton();
    }
  });

  if (installBtn) {
    installBtn.addEventListener('click', async () => {
      if (!deferredInstallPrompt) return;

      deferredInstallPrompt.prompt();
      const { outcome } = await deferredInstallPrompt.userChoice;
      deferredInstallPrompt = null;

      if (outcome === 'accepted') {
        hideInstallButton();
      }
    });
  }

  window.addEventListener('appinstalled', () => {
    deferredInstallPrompt = null;
    hideInstallButton();
  });

})();
