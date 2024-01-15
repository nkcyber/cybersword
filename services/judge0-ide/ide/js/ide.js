const API_KEY = ""; // Get yours for free at https://judge0.com/ce and https://judge0.com/extra-ce

const AUTH_HEADERS = API_KEY ? {
    "X-RapidAPI-Key": API_KEY
} : {};

const defaultUrl = window.location.hostname === "localhost" ?
    "http://localhost/judge0-wrapper" // assume the judge0 wrapper is running locally (with docker compose up)
    : `${window.location.origin}/judge0-wrapper`;

var extraApiUrl = "";

var apiUrl = defaultUrl;
var wait = ((localStorageGetItem("wait") || "false") === "true");
const INITIAL_WAIT_TIME_MS = 500;
const WAIT_TIME_FUNCTION = i => 100 * i;
const MAX_PROBE_REQUESTS = 50;

var blinkStatusLine = ((localStorageGetItem("blink") || "true") === "true");

var fontSize = 17;

var layout;

var sourceEditor;
var stdinEditor;
var stdoutEditor;
var answerEditor;

var isEditorDirty = false;
var currentLanguageId;

var $selectLanguage;
var $insertTemplateBtn;
var $runBtn;
var $navigationMessage;
var $updates;
var $statusLine;

var timeStart;
var timeEnd;

var messagesData;

var challengeId;

var layoutConfig = {
    settings: {
        showPopoutIcon: false,
        reorderEnabled: true
    },
    dimensions: {
        borderWidth: 3,
        headerHeight: 22
    },
    content: [{
        type: "column",
        content: [{
            type: "component",
            height: 70,
            componentName: "source",
            id: "source",
            title: "SOURCE",
            isClosable: false,
            componentState: {
                readOnly: false
            }
        }, {
            type: "stack",
            content: [{
                type: "component",
                componentName: "stdin",
                id: "stdin",
                title: "Input",
                isClosable: false,
                componentState: {
                    readOnly: false
                }
            }, {
                type: "component",
                componentName: "stdout",
                id: "stdout",
                title: "Output",
                isClosable: false,
                componentState: {
                    readOnly: true
                }
            }, {
                type: "component",
                componentName: "answer",
                id: "answer",
                title: "Expected Output",
                isClosable: false,
                componentState: {
                    readOnly: true
                }
            }]
        }]
    }]
};

function encode(str) {
    return btoa(unescape(encodeURIComponent(str || "")));
}

function decode(bytes) {
    var escaped = escape(atob(bytes || ""));
    try {
        return decodeURIComponent(escaped);
    } catch {
        return unescape(escaped);
    }
}

function localStorageSetItem(key, value) {
    try {
        localStorage.setItem(key, value);
    } catch (ignorable) {
    }
}

function localStorageGetItem(key) {
    try {
        return localStorage.getItem(key);
    } catch (ignorable) {
        return null;
    }
}

function showError(title, content) {
    $("#site-modal #title").html(title);
    $("#site-modal .content").html(content);
    $("#site-modal").modal("show");
}

function handleError(jqXHR, _textStatus, _errorThrown) {
    showError(`${jqXHR.statusText} (${jqXHR.status})`, `<pre>${JSON.stringify(jqXHR, null, 4)}</pre>`);
}

function handleRunError(jqXHR, textStatus, errorThrown) {
    handleError(jqXHR, textStatus, errorThrown);
    $runBtn.removeClass("loading");
}

/**
 * show a modal to the user with the flag
 * @param {string} flag 
 */
function handleFlag(flag) {
    $("#flag-modal #title").html("Congrats! You got the flag!");
    $("#flag-modal .content").html(`<pre>${flag}</pre><p>You can close this tab after copying your flag.</p>`);
    $("#flag-modal").modal("show");
}

function handleResult(data) {
    if (data.flag !== "") {
        handleFlag(data.flag);
    }
    const tat = Math.round(performance.now() - timeStart);
    console.log(`It took ${tat}ms to get submission result.`);

    const status = data.status;
    const stdout = decode(data.stdout);
    const compile_output = decode(data.compile_output);
    const time = (data.time === null ? "-" : data.time + "s");
    const memory = (data.memory === null ? "-" : data.memory + "KB");

    $statusLine.html(`${status.description}, ${time}, ${memory} (TAT: ${tat}ms)`);

    if (blinkStatusLine) {
        $statusLine.addClass("blink");
        setTimeout(function () {
            blinkStatusLine = false;
            localStorageSetItem("blink", "false");
            $statusLine.removeClass("blink");
        }, 3000);
    }

    const output = [compile_output, stdout].join("\n").trim();

    stdoutEditor.setValue(output);

    if (output !== "") {
        let dot = document.getElementById("stdout-dot");
        if (!dot.parentElement.classList.contains("lm_active")) {
            dot.hidden = false;
        }
    }

    $runBtn.removeClass("loading");
}

function downloadSource() {
    var value = parseInt($selectLanguage.val());
    download(sourceEditor.getValue(), fileNames[value], "text/plain");
}

function run() {
    if (sourceEditor.getValue().trim() === "") {
        showError("Error", "Source code can't be empty!");
        return;
    } else {
        $runBtn.addClass("loading");
    }

    document.getElementById("stdout-dot").hidden = true;

    stdoutEditor.setValue("");

    var x = layout.root.getItemsById("stdout")[0];
    x.parent.header.parent.setActiveContentItem(x);

    var sourceValue = encode(sourceEditor.getValue());
    var stdinValue = encode(stdinEditor.getValue());
    var languageId = resolveLanguageId($selectLanguage.val());

    if (parseInt(languageId) === 44) {
        sourceValue = sourceEditor.getValue();
    }

    var data = {
        source_code: sourceValue,
        language_id: languageId,
        stdin: stdinValue,
        compiler_options: "",
        command_line_arguments: "",
        redirect_stderr_to_stdout: true,
    };

    var sendRequest = function (data) {
        timeStart = performance.now();
        $.ajax({
            url: apiUrl + `/submissions?base64_encoded=true&wait=${wait}&challenge_id=${challengeId}`,
            type: "POST",
            async: true,
            contentType: "application/json",
            data: JSON.stringify(data),
            headers: AUTH_HEADERS,
            success: function (data, _textStatus, _jqXHR) {
                console.log(`Your submission token is: ${data.token}`);
                if (wait) {
                    handleResult(data);
                } else {
                    setTimeout(fetchSubmission.bind(null, data.token, 1), INITIAL_WAIT_TIME_MS);
                }
            },
            error: handleRunError
        });
    }

    // TODO: update this to new structure
    var fetchAdditionalFiles = false;
    if (parseInt(languageId) === 82) {
        if (sqliteAdditionalFiles === "") {
            fetchAdditionalFiles = true;
            $.ajax({
                url: `./data/additional_files_zip_base64.txt`,
                type: "GET",
                async: true,
                contentType: "text/plain",
                success: function (responseData, _textStatus, _jqXHR) {
                    sqliteAdditionalFiles = responseData;
                    data["additional_files"] = sqliteAdditionalFiles;
                    sendRequest(data);
                },
                error: handleRunError
            });
        }
        else {
            data["additional_files"] = sqliteAdditionalFiles;
        }
    }

    if (!fetchAdditionalFiles) {
        sendRequest(data);
    }
}

function fetchSubmission(submission_token, iteration) {
    if (iteration >= MAX_PROBE_REQUESTS) {
        handleRunError({
            statusText: "Maximum number of probe requests reached",
            status: 504
        }, null, null);
        return;
    }

    $.ajax({
        url: apiUrl + "/submissions/" + submission_token + "?base64_encoded=true&challenge_id=" + challengeId,
        type: "GET",
        async: true,
        accept: "application/json",
        headers: AUTH_HEADERS,
        success: function (data, _textStatus, _jqXHR) {
            if (data.status.id <= 2) { // In Queue or Processing
                $statusLine.html(data.status.description);
                setTimeout(fetchSubmission.bind(null, submission_token, iteration + 1), WAIT_TIME_FUNCTION(iteration));
                return;
            }
            handleResult(data);
        },
        error: handleRunError
    });
}

function changeEditorLanguage() {
    monaco.editor.setModelLanguage(sourceEditor.getModel(), $selectLanguage.find(":selected").attr("mode"));
    currentLanguageId = parseInt($selectLanguage.val());
    $(".lm_title")[0].innerText = fileNames[currentLanguageId];
    apiUrl = resolveApiUrl($selectLanguage.val());
}


const noChallengePromptFound = "# It looks like you haven't selected a challenge yet.\n# Try clicking the link in the challenge description, and opening it in a new tab.";
/**
 * interacts with our custom Judge0 wrapper service,
 * and sets the associated prompt for the challenge
 * specified by the page fragment.
 */
function setChallengeInfo() {
    challengeId = URIHash.get('challenge');
    if (!challengeId) {
        sourceEditor.setValue(noChallengePromptFound)
        return;
    }
    challengeId = parseInt(challengeId);
    if (isNaN(challengeId)) {
        sourceEditor.setValue(noChallengePromptFound)
        return;
    }

    $.ajax({
        url: apiUrl + `/challenge_info/${challengeId}`,
        type: "GET",
        async: true,
        headers: AUTH_HEADERS,
        success: function (data, _textStatus, _jqXHR) {
            sourceEditor.setValue(data.prompt);
            answerEditor.setValue(data.answer.trim());
            currentLanguageId = data.language_id;
            $selectLanguage.dropdown("set selected", currentLanguageId);
        },
        error: handleRunError
    });
}

function insertTemplate() {
    currentLanguageId = parseInt($selectLanguage.val());
    setChallengeInfo();
    stdinEditor.setValue(inputs[currentLanguageId] || "");
    changeEditorLanguage();
}

// TODO: load language based on challenge fragment id
function loadLanguage() {
    var values = [];
    for (var i = 0; i < $selectLanguage[0].options.length; ++i) {
        values.push($selectLanguage[0].options[i].value);
    }
    $selectLanguage.dropdown("set selected", values[0]);
    apiUrl = resolveApiUrl($selectLanguage.val())
    insertTemplate();
}

function resolveLanguageId(id) {
    id = parseInt(id);
    return languageIdTable[id] || id;
}

function resolveApiUrl(id) {
    id = parseInt(id);
    return languageApiUrlTable[id] || defaultUrl;
}

function editorsUpdateFontSize(fontSize) {
    sourceEditor.updateOptions({ fontSize: fontSize });
    stdinEditor.updateOptions({ fontSize: fontSize });
    stdoutEditor.updateOptions({ fontSize: fontSize });
    answerEditor.updateOptions({ fontSize: fontSize });
}

function updateScreenElements() {
    var display = window.innerWidth <= 1200 ? "none" : "";
    $(".wide.screen.only").each(function (_index) {
        $(this).css("display", display);
    });
}

$(window).resize(function () {
    layout.updateSize();
    updateScreenElements();
});

$(document).ready(function () {
    updateScreenElements();

    $selectLanguage = $("#select-language");
    $selectLanguage.change(function (_e) {
        if (!isEditorDirty) {
            insertTemplate();
        } else {
            changeEditorLanguage();
        }
    });

    $insertTemplateBtn = $("#insert-template-btn");
    $insertTemplateBtn.click(function (_e) {
        if (isEditorDirty && confirm("Are you sure? Your current changes will be lost.")) {
            insertTemplate();
        }
    });

    if (!/(Mac|iPhone|iPod|iPad)/i.test(navigator.platform)) {
        $("#run-btn-label").html("Run (Ctrl + ↵)");
    }

    $runBtn = $("#run-btn");
    $runBtn.click(function (_e) {
        run();
    });

    $navigationMessage = $("#navigation-message span");
    $updates = $("#judge0-more");

    $statusLine = $("#status-line");

    $(document).on("keydown", "body", function (e) {
        var keyCode = e.keyCode || e.which;
        if ((e.metaKey || e.ctrlKey) && keyCode === 13) { // Ctrl + Enter, CMD + Enter
            e.preventDefault();
            run();
        } else if (keyCode == 119) { // F8
            e.preventDefault();
            var url = prompt("Enter base URL:", apiUrl);
            if (url != null) {
                url = url.trim();
            }
            if (url != null && url != "") {
                apiUrl = url;
                localStorageSetItem("api-url", apiUrl);
            }
        } else if (keyCode == 118) { // F7
            e.preventDefault();
            wait = !wait;
            localStorageSetItem("wait", wait);
            alert(`Submission wait is ${wait ? "ON. Enjoy" : "OFF"}.`);
        } else if (event.ctrlKey && keyCode == 107) { // Ctrl++
            e.preventDefault();
            fontSize += 1;
            editorsUpdateFontSize(fontSize);
        } else if (event.ctrlKey && keyCode == 109) { // Ctrl+-
            e.preventDefault();
            fontSize -= 1;
            editorsUpdateFontSize(fontSize);
        }
    });

    $("select.dropdown").dropdown();
    $(".ui.dropdown").dropdown();
    $(".ui.dropdown.site-links").dropdown({ action: "hide", on: "hover" });
    $(".ui.checkbox").checkbox();
    $(".message .close").on("click", function () {
        $(this).closest(".message").transition("fade");
    });

    // $("#copy-and-close").on("click", function () {
    //     // TODO: Consider navigator browser API
    //     // https://stackoverflow.com/a/30905277
    //     function copyToClipboard(element) {
    //         var $temp = $("<input>");
    //         $("body").append($temp);
    //         $temp.val($(element).text()).select();
    //         document.execCommand("copy");
    //         $temp.remove();
    //     }
    //     const flag = $("flag-content").text();
    //     copyToClipboard(flag);
    // });

    require(["vs/editor/editor.main"], function (_ignorable) {
        layout = new GoldenLayout(layoutConfig, $("#site-content"));

        layout.registerComponent("source", function (container, state) {
            sourceEditor = monaco.editor.create(container.getElement()[0], {
                automaticLayout: true,
                theme: "vs-dark",
                scrollBeyondLastLine: true,
                readOnly: state.readOnly,
                language: "cpp",
                minimap: {
                    enabled: false
                }
            });

            sourceEditor.getModel().onDidChangeContent(function (_e) {
                currentLanguageId = parseInt($selectLanguage.val());
                isEditorDirty = sourceEditor.getValue() != sources[currentLanguageId];
            });

            sourceEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, run);
        });

        layout.registerComponent("answer", function (container, state) {
            answerEditor = monaco.editor.create(container.getElement()[0], {
                automaticLayout: true,
                theme: "vs-dark",
                scrollBeyondLastLine: false,
                readOnly: state.readOnly,
                language: "plaintext",
                minimap: {
                    enabled: false
                }
            });
        });

        layout.registerComponent("stdin", function (container, state) {
            stdinEditor = monaco.editor.create(container.getElement()[0], {
                automaticLayout: true,
                theme: "vs-dark",
                scrollBeyondLastLine: false,
                readOnly: state.readOnly,
                language: "plaintext",
                minimap: {
                    enabled: false
                }
            });
        });

        layout.registerComponent("stdout", function (container, state) {
            stdoutEditor = monaco.editor.create(container.getElement()[0], {
                automaticLayout: true,
                theme: "vs-dark",
                scrollBeyondLastLine: false,
                readOnly: state.readOnly,
                language: "plaintext",
                minimap: {
                    enabled: false
                }
            });

            container.on("tab", function (tab) {
                tab.element.append("<span id=\"stdout-dot\" class=\"dot\" hidden></span>");
                tab.element.on("mousedown", function (e) {
                    e.target.closest(".lm_tab").children[3].hidden = true;
                });
            });
        });


        layout.on("initialised", function () {
            loadLanguage();
            $("#site-navigation").css("border-bottom", "1px solid black");
            sourceEditor.focus();
            editorsUpdateFontSize(fontSize);
        });

        layout.init();
    });
});


var sqliteSource = "\
-- On Judge0 IDE your SQL script is run on chinook database (https://www.sqlitetutorial.net/sqlite-sample-database).\n\
-- For more information about how to use SQL with Judge0 please\n\
-- watch this asciicast: https://asciinema.org/a/326975.\n\
SELECT\n\
    Name, COUNT(*) AS num_albums\n\
FROM artists JOIN albums\n\
ON albums.ArtistID = artists.ArtistID\n\
GROUP BY Name\n\
ORDER BY num_albums DESC\n\
LIMIT 4;\n\
";
var sqliteAdditionalFiles = "";

const pythonSource = "\
print('hello world')\
";

var sources = {
    71: pythonSource,
    82: sqliteSource,
};

var fileNames = {
    71: "script.py",
    82: "script.sql",
};

var languageIdTable = {
    1001: 1,
    1002: 2,
    1003: 3,
    1004: 4,
    1005: 5,
    1006: 6,
    1007: 7,
    1008: 8,
    1009: 9,
    1010: 10,
    1011: 11,
    1012: 12,
    1013: 13,
    1014: 14,
    1015: 15,
    1021: 21,
    1022: 22,
    1023: 23,
    1024: 24
}

var languageApiUrlTable = {
    1001: extraApiUrl,
    1002: extraApiUrl,
    1003: extraApiUrl,
    1004: extraApiUrl,
    1005: extraApiUrl,
    1006: extraApiUrl,
    1007: extraApiUrl,
    1008: extraApiUrl,
    1009: extraApiUrl,
    1010: extraApiUrl,
    1011: extraApiUrl,
    1012: extraApiUrl,
    1013: extraApiUrl,
    1014: extraApiUrl,
    1015: extraApiUrl,
    1021: extraApiUrl,
    1022: extraApiUrl,
    1023: extraApiUrl,
    1024: extraApiUrl
}

var competitiveProgrammingInput = "\
3\n\
3 2\n\
1 2 5\n\
2 3 7\n\
1 3\n\
3 3\n\
1 2 4\n\
1 3 7\n\
2 3 1\n\
1 3\n\
3 1\n\
1 2 4\n\
1 3\n\
";

var inputs = {
    54: competitiveProgrammingInput
}

