const continueLearningSection = document.querySelector("[data-continue-learning]");
const continueLearningLink = document.querySelector("[data-continue-link]");
const completedLessonsKey = "skillsnacks:completedLessons";
const dailyCompletedLessonsKey = "skillsnacks:dailyCompletedLessons";
const voicePreferenceKey = "skillsnacks:voicePreference";
const streakDateKey = "skillsnacks:lastActiveDate";
const streakCountKey = "skillsnacks:streakCount";

function getCompletedLessons() {
  try {
    const parsed = JSON.parse(window.localStorage.getItem(completedLessonsKey) ?? "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch (_error) {
    return [];
  }
}

function saveCompletedLessons(slugs) {
  window.localStorage.setItem(completedLessonsKey, JSON.stringify([...new Set(slugs)]));
}

function getDailyProgress(today) {
  try {
    const parsed = JSON.parse(window.localStorage.getItem(dailyCompletedLessonsKey) ?? "{}");
    if (!parsed || typeof parsed !== "object" || parsed.date !== today) {
      return { date: today, slugs: [] };
    }
    return {
      date: parsed.date,
      slugs: Array.isArray(parsed.slugs) ? parsed.slugs : [],
    };
  } catch (_error) {
    return { date: today, slugs: [] };
  }
}

function saveDailyProgress(today, slugs) {
  window.localStorage.setItem(
    dailyCompletedLessonsKey,
    JSON.stringify({ date: today, slugs: [...new Set(slugs)] })
  );
}

function updateStreak(today) {
  const lastActiveDate = window.localStorage.getItem(streakDateKey);
  const currentCount = Number.parseInt(window.localStorage.getItem(streakCountKey) ?? "0", 10) || 0;

  if (!lastActiveDate) {
    window.localStorage.setItem(streakDateKey, today);
    window.localStorage.setItem(streakCountKey, "1");
    return 1;
  }

  if (lastActiveDate === today) {
    return currentCount || 1;
  }

  const previousDate = new Date(`${lastActiveDate}T00:00:00`);
  const currentDate = new Date(`${today}T00:00:00`);
  const daysBetween = Math.round((currentDate - previousDate) / 86400000);
  const nextCount = daysBetween === 1 ? currentCount + 1 : 1;

  window.localStorage.setItem(streakDateKey, today);
  window.localStorage.setItem(streakCountKey, String(nextCount));
  return nextCount;
}

function renderStreak() {
  const streakCountNodes = document.querySelectorAll("[data-streak-count]");
  if (!streakCountNodes.length) {
    return;
  }

  const lastActiveDate = window.localStorage.getItem(streakDateKey);
  const lessonArticle = document.querySelector("[data-lesson-slug]");
  const streakPanel = document.querySelector("[data-streak-panel]");
  const navStreak = document.querySelector("[data-streak-count][data-today]");
  const today = lessonArticle?.dataset.today ?? streakPanel?.dataset.today ?? navStreak?.dataset.today;
  let count = Number.parseInt(window.localStorage.getItem(streakCountKey) ?? "0", 10) || 0;

  if (lastActiveDate && today) {
    const previousDate = new Date(`${lastActiveDate}T00:00:00`);
    const currentDate = new Date(`${today}T00:00:00`);
    const daysBetween = Math.round((currentDate - previousDate) / 86400000);
    if (daysBetween > 1) {
      count = 0;
      window.localStorage.setItem(streakCountKey, "0");
    }
  }

  streakCountNodes.forEach((node) => {
    node.textContent = `🔥 ${count} Day Curiosity Streak`;
  });
}

function renderDailyGoal() {
  const goalNodes = document.querySelectorAll("[data-daily-goal]");
  if (!goalNodes.length) {
    return;
  }

  const lessonArticle = document.querySelector("[data-lesson-slug]");
  const goalPanel = document.querySelector("[data-daily-goal-panel]");
  const navStreak = document.querySelector("[data-streak-count][data-today]");
  const today = lessonArticle?.dataset.today ?? goalPanel?.dataset.today ?? navStreak?.dataset.today;
  const progress = getDailyProgress(today);

  goalNodes.forEach((node) => {
    node.textContent = `${progress.slugs.length} / 3 lessons`;
  });
}

function renderTopicProgress() {
  const completedLessons = new Set(getCompletedLessons());
  const topicBlocks = document.querySelectorAll("[data-topic-progress]");

  topicBlocks.forEach((block) => {
    const lessonSlugs = (block.dataset.topicLessons ?? "")
      .split(",")
      .map((slug) => slug.trim())
      .filter(Boolean);
    const total = Number.parseInt(block.dataset.topicTotal ?? String(lessonSlugs.length), 10) || lessonSlugs.length;
    const completed = lessonSlugs.filter((slug) => completedLessons.has(slug)).length;
    const percent = total > 0 ? (completed / total) * 100 : 0;

    const text = block.querySelector("[data-topic-progress-text]");
    const fill = block.querySelector("[data-topic-progress-fill]");

    if (text) {
      text.textContent = `${completed} / ${total} lessons completed`;
    }

    if (fill) {
      fill.style.width = `${percent}%`;
    }
  });
}

if (continueLearningSection && continueLearningLink) {
  const savedSlug = window.localStorage.getItem("skillsnacks:lastLessonSlug");
  const savedTitle = window.localStorage.getItem("skillsnacks:lastLessonTitle");

  if (savedSlug && savedTitle) {
    continueLearningLink.href = `/lesson/${savedSlug}`;
    continueLearningLink.querySelector("[data-continue-title]").textContent = savedTitle;
    continueLearningLink.querySelector("[data-continue-meta]").textContent = "Continue your last lesson";
    continueLearningSection.classList.remove("is-hidden");
  }
}

const lessonArticle = document.querySelector("[data-lesson-slug]");

if (lessonArticle) {
  const lessonSlug = lessonArticle.dataset.lessonSlug;
  const lessonTitle = lessonArticle.dataset.lessonTitle;
  const today = lessonArticle.dataset.today;

  window.localStorage.setItem("skillsnacks:lastLessonSlug", lessonSlug);
  window.localStorage.setItem("skillsnacks:lastLessonTitle", lessonTitle);
  if (today) {
    updateStreak(today);
  }

  const controls = lessonArticle.querySelector("[data-speech-controls]");
  const voiceSelect = lessonArticle.querySelector("[data-voice-select]");
  const completionBadge = lessonArticle.querySelector("[data-completion-badge]");
  const endMarker = lessonArticle.querySelector("[data-lesson-end]");
  const ideas = Array.from(lessonArticle.querySelectorAll("[data-lesson-speech] li")).map((item) => item.textContent.trim());
  const intro = lessonArticle.querySelector("h1")?.textContent.trim() ?? "";
  const storySections = Array.from(lessonArticle.querySelectorAll("[data-lesson-speech-part]")).map((item) => item.textContent.trim());
  const speechText = lessonArticle.dataset.lessonNarration || [intro, ...storySections, ...ideas].filter(Boolean).join(". ");
  let availableVoices = [];
  let selectedVoicePreference = window.localStorage.getItem(voicePreferenceKey) ?? "female";

  if (voiceSelect) {
    voiceSelect.value = selectedVoicePreference;
    voiceSelect.addEventListener("change", () => {
      selectedVoicePreference = voiceSelect.value;
      window.localStorage.setItem(voicePreferenceKey, selectedVoicePreference);
    });
  }

  function matchVoice(preference) {
    const femaleHints = ["female", "woman", "zira", "samantha", "victoria", "karen", "susan"];
    const maleHints = ["male", "man", "david", "daniel", "alex", "fred", "thomas"];
    const hints = preference === "male" ? maleHints : femaleHints;

    const exactMatch = availableVoices.find((voice) =>
      hints.some((hint) => voice.name.toLowerCase().includes(hint))
    );

    return exactMatch ?? availableVoices[0] ?? null;
  }

  function loadVoices() {
    availableVoices = window.speechSynthesis.getVoices();
  }

  if ("speechSynthesis" in window) {
    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;
  }

  function setCompletionState() {
    if (!completionBadge) {
      return;
    }

    const completedLessons = new Set(getCompletedLessons());
    completionBadge.textContent = completedLessons.has(lessonSlug) ? "Completed" : "In progress";
  }

  function markLessonCompleted() {
    const completedLessons = getCompletedLessons();
    completedLessons.push(lessonSlug);
    saveCompletedLessons(completedLessons);

    if (today) {
      const dailyProgress = getDailyProgress(today);
      dailyProgress.slugs.push(lessonSlug);
      saveDailyProgress(today, dailyProgress.slugs);
    }

    setCompletionState();
    renderTopicProgress();
    renderDailyGoal();
  }

  setCompletionState();

  if (endMarker && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            markLessonCompleted();
            observer.disconnect();
          }
        });
      },
      { threshold: 0.9 }
    );

    observer.observe(endMarker);
  }

  if (controls && "speechSynthesis" in window) {
    controls.addEventListener("click", (event) => {
      const button = event.target.closest("[data-speech-action]");
      if (!button) {
        return;
      }

      const action = button.dataset.speechAction;

      if (action === "read") {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(speechText);
        utterance.rate = 1;
        utterance.pitch = 1;
        const matchedVoice = matchVoice(selectedVoicePreference);
        if (matchedVoice) {
          utterance.voice = matchedVoice;
        }
        window.speechSynthesis.speak(utterance);
      }

      if (action === "pause") {
        if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
          window.speechSynthesis.pause();
        } else if (window.speechSynthesis.paused) {
          window.speechSynthesis.resume();
        }
      }

      if (action === "stop") {
        window.speechSynthesis.cancel();
      }
    });
  } else if (controls) {
    controls.innerHTML = "<p>Your browser does not support speech synthesis.</p>";
  }

  const audioControls = lessonArticle.querySelector("[data-audio-controls]");
  const audioPlayer = lessonArticle.querySelector("[data-audio-player]");
  if (audioControls && audioPlayer) {
    audioControls.addEventListener("click", (event) => {
      const button = event.target.closest("[data-audio-action]");
      if (!button) {
        return;
      }

      const action = button.dataset.audioAction;
      if (action === "play") {
        audioPlayer.play();
      }
      if (action === "pause") {
        audioPlayer.pause();
      }
      if (action === "stop") {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
      }
    });
  }
}

renderStreak();
renderTopicProgress();
renderDailyGoal();
