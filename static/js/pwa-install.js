let deferredInstallPrompt = null;

function isStandaloneMode() {
  return window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
}

function createInstallPrompt() {
  if (isStandaloneMode()) {
    return null;
  }

  if (document.querySelector("[data-pwa-install]")) {
    return null;
  }

  const container = document.createElement("div");
  container.className = "pwa-install is-hidden";
  container.setAttribute("data-pwa-install", "");

  const copy = document.createElement("p");
  copy.className = "pwa-install__copy";
  copy.textContent = "Install SkillSnacks";

  const actions = document.createElement("div");
  actions.className = "pwa-install__actions";

  const installButton = document.createElement("button");
  installButton.type = "button";
  installButton.className = "action-button";
  installButton.textContent = "Install";
  installButton.setAttribute("data-pwa-install-action", "install");

  const dismissButton = document.createElement("button");
  dismissButton.type = "button";
  dismissButton.className = "pwa-install__dismiss";
  dismissButton.textContent = "Not now";
  dismissButton.setAttribute("data-pwa-install-action", "dismiss");

  actions.append(installButton, dismissButton);
  container.append(copy, actions);
  document.body.append(container);

  container.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-pwa-install-action]");
    if (!button) {
      return;
    }

    const action = button.dataset.pwaInstallAction;
    if (action === "dismiss") {
      container.classList.add("is-hidden");
      return;
    }

    if (action === "install" && deferredInstallPrompt) {
      deferredInstallPrompt.prompt();
      const outcome = await deferredInstallPrompt.userChoice;
      if (outcome.outcome === "accepted") {
        container.classList.add("is-hidden");
      }
      deferredInstallPrompt = null;
    }
  });

  return container;
}

const installPrompt = createInstallPrompt();

window.addEventListener("beforeinstallprompt", (event) => {
  if (isStandaloneMode()) {
    return;
  }

  event.preventDefault();
  deferredInstallPrompt = event;
  if (installPrompt) {
    installPrompt.classList.remove("is-hidden");
  }
});

window.addEventListener("appinstalled", () => {
  deferredInstallPrompt = null;
  if (installPrompt) {
    installPrompt.classList.add("is-hidden");
  }
});
