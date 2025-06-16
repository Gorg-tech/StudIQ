<template>
      <div class="result-card card">
        <h2>Dein Quiz-Ergebnis</h2>
        <div class="result-summary">
          <div class="result-score">
            <span class="score">{{ correctAnswers }}</span> / {{ totalQuestions }} richtig
          </div>
          <div class="result-percentage">
            <span>{{ percentage }}%</span> korrekt beantwortet
          </div>
        </div>
        <div class ="rating">
          <span v-if="percentage >= 80" class="badge badge-success">Super!</span>
          <span v-else-if="percentage >= 50" class="badge badge-warning">Gut gemacht!</span>
          <span v-else class="badge badge-danger">Versuche es nochmal!</span>
        </div>
        <ul class="result-list">
          <li v-for="(result, idx) in results" :key="idx" class="result-item">
            <div class="question">{{ result.question }}</div>
            <div class="answers">
              <span :class="['user-answer', result.isCorrect ? 'correct' : 'incorrect']">
                Deine Antwort: {{ result.userAnswer }}
              </span>
              <span v-if="!result.isCorrect" class="correct-answer">
                Richtige Antwort: {{ result.correctAnswer }}
              </span>
            </div>
          </li>
        </ul>
        <div class="button-row">
            <button class="btn btn-primary" @click="restartQuiz">Quiz erneut starten</button>
            <button class="btn btn-secondary" @click="$router.push('/quizOverview')">Zur Quizübersicht</button>
        </div>
      </div>
    </template>
    
    <script setup>
    import { ref, computed } from 'vue'
    import { useRouter } from 'vue-router'
    
    const router = useRouter()

    const results = ref([
      { question: 'Was ist 2 + 2?', userAnswer: '4', correctAnswer: '4', isCorrect: true },
      { question: 'Hauptstadt von Frankreich?', userAnswer: 'Berlin', correctAnswer: 'Paris', isCorrect: false }
    ])
    
    const correctAnswers = computed(() => results.value.filter(r => r.isCorrect).length)
    const totalQuestions = computed(() => results.value.length)
    const percentage = computed(() =>
      totalQuestions.value > 0
        ? Math.round((correctAnswers.value / totalQuestions.value) * 100)
        : 0
    )
    
    function restartQuiz() {
      // Hier Quiz-Logik einfügen
      alert('Quiz wird neu gestartet!')
    }

    function goToOverview() {
      router.push('/quiz')
    }
    </script>
    
    <style scoped>
    .result-card {
      background-color: #fff;
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
      margin: 0 auto;
      max-width: 600px;
      text-align: center;
    }
    
    .result-card h2 {
      color: var(--color-accent);
      margin-bottom: 16px;
    }
    
    .result-summary {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 18px;
    }
    
    .result-score {
      font-size: 2rem;
      font-weight: 700;
      color: var(--color-primary);
    }
    
    .result-percentage {
      font-size: 1.1rem;
      color: var(--color-muted);
    }
    
    .result-list {
      list-style: none;
      padding: 0;
      margin: 24px 0;
      text-align: left;
    }
    
    .result-item {
      background: #f9f9f9;
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 12px;
      box-shadow: 0 1px 4px rgba(34, 34, 34, 0.04);
    }
    
    .question {
      font-weight: 600;
      margin-bottom: 6px;
      color: var(--color-text);
    }
    
    .answers {
      font-size: 0.98rem;
    }
    
    .user-answer.correct {
      color: #4caf50;
      font-weight: 600;
    }
    
    .user-answer.incorrect {
      color: #f44336;
      font-weight: 600;
    }
    
    .correct-answer {
      color: #2196f3;
      margin-left: 12px;
    }

    .button-row {
      display: flex;
      gap: 16px;
      justify-content: center;
      margin-top: 24px;
    }
    
    .btn-primary {
      padding: 12px 20px;
      font-size: 1.1rem;
      background: var(--color-accent);
      color: #fff;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 12px;
      transition: background 0.2s;
    }
    
    .btn-primary:hover {
      background: var(--color-primary);
    }

    .btn-secondary {
      padding: 12px 20px;
      font-size: 1.1rem;
      background: var(--color-accent);
      color: #fff;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 12px;
      transition: background 0.2s;
    }

    .btn-secondary:hover {
      background: var(--color-primary);
    }
    </style>
