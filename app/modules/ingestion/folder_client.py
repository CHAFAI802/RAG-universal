FOLDER_CLIENT_HTML = """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Importer un dossier - RAG Universal</title>
  <style>
    :root {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #172033;
      background: #f3f6fb;
    }
    * { box-sizing: border-box; }
    body { max-width: 76rem; margin: 0 auto; padding: 2rem 1.25rem 4rem; }
    h1 { margin-bottom: .4rem; font-size: clamp(1.8rem, 4vw, 2.4rem); }
    h2 { font-size: 1.15rem; }
    p { line-height: 1.55; }
    .intro { color: #596579; max-width: 58rem; }
    .panel {
      margin-top: 1.25rem; padding: 1.35rem; background: white;
      border: 1px solid #dfe5ef; border-radius: 14px;
      box-shadow: 0 5px 20px rgb(25 45 80 / 5%);
    }
    .panel-header {
      display: flex; align-items: center; justify-content: space-between;
      gap: 1rem; flex-wrap: wrap; margin-bottom: .8rem;
    }
    label { display: block; margin: .8rem 0; }
    input, button { font: inherit; }
    input:not([type="checkbox"]) {
      display: block; width: min(100%, 28rem); margin-top: .35rem;
      padding: .7rem .8rem; border: 1px solid #cbd4e2; border-radius: 8px;
    }
    button {
      border: 0; border-radius: 8px; padding: .7rem 1rem;
      background: #183153; color: white; font-weight: 600; cursor: pointer;
    }
    button:hover:not(:disabled) { background: #24466f; }
    button:disabled { opacity: .48; cursor: not-allowed; }
    button.secondary { background: #e8edf5; color: #24344d; }
    button.secondary:hover:not(:disabled) { background: #dce4ef; }
    .actions { display: flex; gap: .65rem; flex-wrap: wrap; align-items: center; }
    .muted { color: #647187; }
    #folder-name { margin: .8rem 0; color: #35445d; overflow-wrap: anywhere; }
    #status { min-height: 1.5rem; margin: 1rem 0; font-weight: 600; }
    .progress-track {
      height: 9px; background: #e7ecf4; border-radius: 99px;
      overflow: hidden; margin-top: 1rem;
    }
    #progress-bar {
      width: 0; height: 100%; background: #16835d;
      transition: width .2s ease;
    }
    .stats {
      display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: .75rem; margin-top: 1rem;
    }
    .stat { padding: .85rem; background: #f5f7fb; border-radius: 10px; }
    .stat strong { display: block; font-size: 1.5rem; }
    .stat span { color: #647187; font-size: .9rem; }
    .table-wrap { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; min-width: 44rem; }
    th, td { padding: .8rem .65rem; text-align: left; border-bottom: 1px solid #e8edf4; }
    th { color: #596579; font-size: .82rem; text-transform: uppercase; letter-spacing: .04em; }
    td { font-size: .92rem; vertical-align: top; }
    td.path { max-width: 22rem; overflow-wrap: anywhere; }
    .badge {
      display: inline-block; padding: .25rem .55rem; border-radius: 99px;
      font-size: .78rem; font-weight: 700;
    }
    .badge.RECEIVED { background: #dff5e9; color: #17613e; }
    .badge.FAILED { background: #fde7e7; color: #9b2929; }
    .badge.PENDING, .badge.RECEIVING { background: #fff1cf; color: #805a08; }
    .empty { padding: 1.5rem; text-align: center; color: #647187; }
    #results { white-space: pre-wrap; overflow-wrap: anywhere; margin-bottom: 0; }
    @media (max-width: 600px) {
      body { padding: 1.25rem .8rem 3rem; }
      .panel { padding: 1rem; }
      .stats { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <h1>Importer un dossier</h1>
  <p class="intro">
    Sélectionnez un dossier sur votre ordinateur. Le navigateur ne peut
    parcourir que le dossier explicitement choisi. Aucun fichier n'est lu
    ni transmis avant votre confirmation.
  </p>

  <form id="login" class="panel">
    <h2>Authentification</h2>
    <label>Username
      <input name="username" autocomplete="username" required>
    </label>
    <label>Mot de passe
      <input name="password" type="password" autocomplete="current-password" required>
    </label>
    <button type="submit">Se connecter</button>
  </form>

  <section id="folder-controls" class="panel" hidden>
    <div class="panel-header">
      <h2>Nouvel import</h2>
      <span class="muted">Import local sécurisé</span>
    </div>
    <div class="actions">
      <button id="choose" type="button">Choisir un dossier</button>
      <input id="folder-input" type="file" webkitdirectory directory multiple hidden>
      <button id="choose-file" type="button">Choisir un fichier</button>
      <input id="file-input" type="file" hidden>
    </div>
    <p id="folder-name" aria-live="polite"></p>
    <label>
      <input id="consent" type="checkbox">
      Je confirme l'envoi des fichiers du dossier sélectionné.
    </label>
    <div class="actions">
      <button id="upload" type="button" disabled>Parcourir et envoyer</button>
    </div>
    <div class="progress-track" aria-label="Progression de l'import">
      <div id="progress-bar"></div>
    </div>
    <p id="progress-label" class="muted" aria-live="polite">
      En attente d'un dossier.
    </p>
    <div class="stats" aria-label="Résultats du dernier import">
      <div class="stat"><strong id="success-count">0</strong><span>Reçus</span></div>
      <div class="stat"><strong id="failure-count">0</strong><span>En erreur</span></div>
      <div class="stat"><strong id="rejected-count">0</strong><span>Refusés localement</span></div>
    </div>
  </section>

  <p id="status" role="status" aria-live="polite"></p>

  <section id="results-panel" class="panel" hidden>
    <h2>Résultats du dernier import</h2>
    <pre id="results" aria-live="polite"></pre>
  </section>

  <section id="history-panel" class="panel" hidden>
    <div class="panel-header">
      <div>
        <h2>Historique des ingestions</h2>
        <p class="muted">Documents enregistrés pour votre compte.</p>
      </div>
      <button id="refresh-history" class="secondary" type="button">Actualiser</button>
    </div>
    <p id="history-status" class="muted" role="status" aria-live="polite"></p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Document</th>
            <th>Chemin source</th>
            <th>Taille</th>
            <th>Date de réception</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody id="history-body"></tbody>
      </table>
    </div>
    <div id="history-empty" class="empty" hidden>
      Aucune ingestion enregistrée.
    </div>
    <div class="actions">
      <button id="history-more" class="secondary" type="button" hidden>
        Charger la suite
      </button>
    </div>
  </section>

  <script>
    let accessToken = null;
    let selectedDirectory = null;
    let firefoxFiles = [];
    let firefoxRejected = [];
    let selectionMode = null;
    let busy = false;
    const supportsDirectoryPicker =
      typeof window.showDirectoryPicker === "function";

    const status = document.querySelector("#status");
    const results = document.querySelector("#results");
    const consent = document.querySelector("#consent");
    const uploadButton = document.querySelector("#upload");
    const folderInput = document.querySelector("#folder-input");
    const fileInput = document.querySelector("#file-input");
    const folderName = document.querySelector("#folder-name");
    const progressBar = document.querySelector("#progress-bar");
    const progressLabel = document.querySelector("#progress-label");
    const successCount = document.querySelector("#success-count");
    const failureCount = document.querySelector("#failure-count");
    const rejectedCount = document.querySelector("#rejected-count");
    const resultsPanel = document.querySelector("#results-panel");
    const historyPanel = document.querySelector("#history-panel");
    const historyBody = document.querySelector("#history-body");
    const historyStatus = document.querySelector("#history-status");
    const historyEmpty = document.querySelector("#history-empty");
    const historyMore = document.querySelector("#history-more");
    const historyLimit = 50;
    let historyOffset = 0;
    let historyHasMore = false;

    async function readJson(response) {
      try {
        return await response.json();
      } catch {
        return {};
      }
    }

    document.querySelector("#login").addEventListener("submit", async event => {
      event.preventDefault();
      const form = new FormData(event.currentTarget);
      const password = form.get("password");
      event.currentTarget.elements.password.value = "";
      status.textContent = "Connexion en cours…";
      try {
        const response = await fetch("/api/v1/auth/login", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            username: form.get("username"),
            password
          })
        });
        const data = await readJson(response);
        if (!response.ok || !data.access_token) {
          status.textContent = "Connexion refusée. Vérifiez vos identifiants.";
          return;
        }
        accessToken = data.access_token;
        document.querySelector("#folder-controls").hidden = false;
        historyPanel.hidden = false;
        status.textContent = "Connecté. Choisissez un dossier.";
        await loadHistory(true);
      } catch {
        status.textContent = "Connexion impossible. Vérifiez votre connexion.";
      }
    });

    function resetSelection() {
      selectedDirectory = null;
      firefoxFiles = [];
      firefoxRejected = [];
      selectionMode = null;
      folderInput.value = "";
      fileInput.value = "";
      consent.checked = false;
      folderName.textContent = "";
      uploadButton.disabled = true;
    }

    function hasSelection() {
      return selectionMode !== null && (
        selectedDirectory !== null ||
        firefoxFiles.length + firefoxRejected.length > 0
      );
    }

    function updateUploadButton() {
      uploadButton.disabled = !consent.checked || !hasSelection() || busy;
    }

    function validateRelativePath(rawPath) {
      if (typeof rawPath !== "string" || rawPath.length === 0) return null;
      if (rawPath.startsWith("/") || rawPath.endsWith("/")) return null;
      if (rawPath.startsWith("\\\\")) return null;
      if (/^[A-Za-z]:/.test(rawPath)) return null;
      if (rawPath.includes("\\\\") || rawPath.includes("//")) return null;
      if (rawPath.includes(String.fromCharCode(0))) return null;
      const segments = rawPath.split("/");
      for (const segment of segments) {
        if (segment === "" || segment === "." || segment === "..") return null;
      }
      return segments.join("/");
    }

    function isHiddenPath(relativePath) {
      return relativePath.split("/").some(
        segment => segment.startsWith(".")
      );
    }

    document.querySelector("#choose").addEventListener("click", async () => {
      if (busy) return;
      if (supportsDirectoryPicker) {
        try {
          const directory = await window.showDirectoryPicker({mode: "read"});
          resetSelection();
          selectedDirectory = directory;
          selectionMode = "chromium";
          folderName.textContent = "Dossier sélectionné : " + directory.name;
          status.textContent =
            "Confirmez l'envoi avant tout parcours du dossier.";
          updateUploadButton();
        } catch (error) {
          if (error.name !== "AbortError") {
            status.textContent = "Le dossier n'a pas pu être sélectionné.";
          }
        }
        return;
      }
      folderInput.value = "";
      folderInput.click();
    });

    document.querySelector("#choose-file").addEventListener("click", () => {
      if (busy) return;
      fileInput.value = "";
      fileInput.click();
    });

    fileInput.addEventListener("change", () => {
      const file = fileInput.files && fileInput.files[0];
      if (!file) return;

      const checkedName = validateRelativePath(file.name);
      resetSelection();
      selectionMode = "files";

      if (
        checkedName === null ||
        checkedName.includes("/") ||
        isHiddenPath(checkedName)
      ) {
        firefoxRejected = [
          file.name + " : nom ou chemin de fichier non autorisé"
        ];
        folderName.textContent = "Fichier refusé : " + file.name;
      } else {
        firefoxFiles = [{file, relativePath: checkedName}];
        folderName.textContent = "Fichier sélectionné : " + file.name;
      }

      status.textContent =
        "Confirmez l'envoi avant toute lecture du fichier.";
      results.textContent = "";
      for (const item of firefoxRejected) {
        results.textContent += "REFUSÉ — " + item + "\\n";
      }
      updateUploadButton();
    });

    folderInput.addEventListener("change", () => {
      const selection = collectFirefoxSelection(folderInput.files);
      resetSelection();
      firefoxFiles = selection.files;
      firefoxRejected = selection.rejected;
      selectionMode = "firefox";
      const total = firefoxFiles.length + firefoxRejected.length;
      if (total === 0) {
        status.textContent =
          "Aucun fichier exploitable dans le dossier sélectionné.";
        return;
      }
      folderName.textContent = "Dossier sélectionné : " + total + " fichier(s)";
      status.textContent =
        "Confirmez l'envoi avant toute lecture des fichiers.";
      results.textContent = "";
      for (const item of firefoxRejected) {
        results.textContent += "REFUSÉ — " + item + "\\n";
      }
      updateUploadButton();
    });

    consent.addEventListener("change", updateUploadButton);

    function collectFirefoxSelection(fileList) {
      const files = [];
      const rejected = [];
      let rootName = null;
      for (const file of fileList) {
        const rawPath = file.webkitRelativePath || "";
        const checkedPath = validateRelativePath(rawPath);
        if (checkedPath === null) {
          rejected.push(
            (rawPath || file.name) + " : chemin hors du dossier autorisé"
          );
          continue;
        }
        const segments = checkedPath.split("/");
        if (segments.length < 2) {
          rejected.push(checkedPath + " : fichier hors d'un dossier racine");
          continue;
        }
        if (rootName === null) {
          rootName = segments[0];
        } else if (segments[0] !== rootName) {
          rejected.push(
            checkedPath + " : dossier racine différent de " + rootName
          );
          continue;
        }
        const relativePath = segments.slice(1).join("/");
        if (isHiddenPath(relativePath)) {
          rejected.push(relativePath + " : fichier ou dossier caché refusé");
          continue;
        }
        files.push({file, relativePath});
      }
      return {files, rejected, rootName};
    }

    async function collectFiles(directory, root, path, files, rejected) {
      for await (const [name, entry] of directory.entries()) {
        const relativePath = path ? path + "/" + name : name;
        try {
          const resolvedPath = await root.resolve(entry);
          if (resolvedPath === null) {
            rejected.push(relativePath + " : chemin hors du dossier autorisé");
            continue;
          }
          const checkedPath = validateRelativePath(relativePath);
          if (checkedPath === null) {
            rejected.push(relativePath + " : chemin relatif invalide");
            continue;
          }
          if (entry.kind === "directory") {
            if (isHiddenPath(checkedPath)) {
              rejected.push(checkedPath + " : dossier caché refusé");
              continue;
            }
            await collectFiles(entry, root, checkedPath, files, rejected);
          } else if (isHiddenPath(checkedPath)) {
            rejected.push(checkedPath + " : fichier ou dossier caché refusé");
          } else {
            files.push({file: await entry.getFile(), relativePath: checkedPath});
          }
        } catch {
          rejected.push(relativePath + " : accès ou lecture refusé");
        }
      }
    }

    function formatBytes(value) {
      const bytes = Number(value) || 0;
      if (bytes < 1024) return bytes + " o";
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " Ko";
      if (bytes < 1024 * 1024 * 1024) {
        return (bytes / (1024 * 1024)).toFixed(1) + " Mo";
      }
      return (bytes / (1024 * 1024 * 1024)).toFixed(2) + " Go";
    }

    function formatDate(value) {
      if (!value) return "—";
      const date = new Date(value);
      return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString("fr-FR");
    }

    function appendCell(row, value, className) {
      const cell = document.createElement("td");
      if (className) cell.className = className;
      cell.textContent = value == null || value === "" ? "—" : String(value);
      row.appendChild(cell);
      return cell;
    }

    function renderHistory(items, append) {
      if (!append) historyBody.replaceChildren();
      for (const item of items) {
        const row = document.createElement("tr");
        appendCell(row, item.document_name);
        appendCell(row, item.source_identifier || item.source_type, "path");
        appendCell(row, formatBytes(item.size_bytes));
        appendCell(row, formatDate(item.received_at || item.created_at));
        const statusCell = appendCell(row, "");
        const badge = document.createElement("span");
        const allowedStatuses = new Set([
          "PENDING",
          "RECEIVING",
          "RECEIVED",
          "FAILED"
        ]);
        const isKnownStatus = allowedStatuses.has(item.status);
        badge.className = isKnownStatus ? "badge " + item.status : "badge";
        badge.textContent = isKnownStatus ? item.status : "INCONNU";
        statusCell.appendChild(badge);
        historyBody.appendChild(row);
      }
      historyEmpty.hidden = historyBody.children.length !== 0;
      historyMore.hidden = !historyHasMore;
    }

    async function loadHistory(reset) {
      if (!accessToken) return;
      if (reset) historyOffset = 0;
      historyStatus.textContent = "Chargement de l'historique…";
      try {
        const response = await fetch(
          "/api/v1/ingestions?limit=" + historyLimit + "&offset=" + historyOffset,
          {headers: {"Authorization": "Bearer " + accessToken}}
        );
        if (response.status === 401) {
          accessToken = null;
          historyStatus.textContent = "Session expirée. Reconnectez-vous.";
          document.querySelector("#folder-controls").hidden = true;
          historyPanel.hidden = true;
          return;
        }
        if (!response.ok) throw new Error("HTTP " + response.status);
        const items = await readJson(response);
        if (!Array.isArray(items)) throw new Error("Réponse invalide");
        historyHasMore = items.length === historyLimit;
        renderHistory(items, !reset);
        if (reset) historyOffset = items.length;
        else historyOffset += items.length;
        historyStatus.textContent =
          historyBody.children.length + " ingestion(s) affichée(s).";
      } catch {
        historyStatus.textContent =
          "Impossible de charger l'historique. Réessayez.";
      }
    }

    document.querySelector("#refresh-history").addEventListener(
      "click", () => loadHistory(true)
    );
    historyMore.addEventListener("click", () => loadHistory(false));

    uploadButton.addEventListener("click", async () => {
      if (!accessToken || !consent.checked || busy) return;
      if (!hasSelection()) return;

      busy = true;
      uploadButton.disabled = true;
      results.textContent = "";
      resultsPanel.hidden = false;
      successCount.textContent = "0";
      failureCount.textContent = "0";
      rejectedCount.textContent = "0";
      progressBar.style.width = "0%";
      progressLabel.textContent = "Préparation du parcours…";

      const files = [];
      const rejected = [];
      let succeeded = 0;
      let failed = 0;

      try {
        if (selectionMode === "chromium" && selectedDirectory !== null) {
          await collectFiles(
            selectedDirectory,
            selectedDirectory,
            "",
            files,
            rejected
          );
        } else if (
          selectionMode === "firefox" ||
          selectionMode === "files"
        ) {
          files.push(...firefoxFiles);
          rejected.push(...firefoxRejected);
        }

        for (const item of rejected) {
          results.textContent += "REFUSÉ — " + item + "\\n";
        }
        rejectedCount.textContent = String(rejected.length);

        const total = files.length;
        if (total === 0) {
          progressLabel.textContent = "Aucun fichier à transmettre.";
        }

        for (let index = 0; index < total; index++) {
          const item = files[index];
          status.textContent = "Envoi de " + item.relativePath;
          progressLabel.textContent =
            "Fichier " + (index + 1) + " sur " + total +
            " — " + item.relativePath;

          try {
            const metadataResponse = await fetch("/api/v1/ingestions", {
              method: "POST",
              headers: {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                document_name: item.file.name,
                source_type: "LOCAL_FOLDER",
                source_identifier: item.relativePath
              })
            });
            const metadata = await readJson(metadataResponse);

            if (!metadataResponse.ok || !metadata.ingestion_id) {
              failed++;
              results.textContent += "ERREUR — " + item.relativePath +
                " : " + (metadata.detail || "création de l'ingestion refusée") + "\\n";
            } else {
              const response = await fetch(
                "/api/v1/ingestions/" + metadata.ingestion_id + "/source",
                {
                  method: "PUT",
                  headers: {
                    "Authorization": "Bearer " + accessToken,
                    "Content-Type": "application/octet-stream"
                  },
                  body: item.file
                }
              );
              const result = await readJson(response);

              if (response.ok && result.status === "RECEIVED") {
                succeeded++;
                results.textContent += "REÇU — " + item.relativePath +
                  " — " + result.ingestion_id + "\\n";
              } else {
                failed++;
                results.textContent += "ERREUR — " + item.relativePath +
                  " — " + (result.detail || result.error_message ||
                    "transfert refusé") + "\\n";
              }
            }
          } catch {
            failed++;
            results.textContent += "ERREUR — " + item.relativePath +
              " — transfert interrompu\\n";
          }

          successCount.textContent = String(succeeded);
          failureCount.textContent = String(failed);
          progressBar.style.width =
            Math.round(((index + 1) / total) * 100) + "%";
        }

        status.textContent =
          "Parcours terminé : " + succeeded + " reçu(s), " +
          failed + " en erreur, " + rejected.length +
          " refusé(s) localement.";
        progressLabel.textContent = total
          ? "Parcours terminé : " + total + " fichier(s) traité(s)."
          : "Aucun fichier transmis.";

        await loadHistory(true);
      } catch {
        status.textContent =
          "Le dossier autorisé n'a pas pu être parcouru.";
        progressLabel.textContent = "Parcours interrompu.";
      } finally {
        busy = false;
        resetSelection();
      }
    });
  </script>
</body>
</html>
"""
