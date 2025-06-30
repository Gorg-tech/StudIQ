<template>
  <div class="quiz-overview-container">
    <div class="card quiz-card">
      <div class="quiz-header">
        <div>
          <h2>
            {{ quiz.title }}
            <span class="quiz-progress">
              (Frage {{ currentIndex + 1 }} von {{ questions.length }})
            </span>
          </h2>
          <p class="quiz-description">{{ quiz.description }}</p>
        </div>
        <div class="quiz-card-penguin">
          <Penguin style="width: 80px; height: 80px;" />
        </div>
      </div>
      <div class="quiz-content">
        <div class="question-block">
          <h3>{{ currentQuestion.question }}</h3>
          <div v-for="(answer, index) in currentQuestion.answers" :key="index" class="answer-row">
            <label>
              <input type="radio" :value="answer" v-model="selectedAnswer" name="answer">
              {{ answer }}
            </label>
          </div>
          <div class="button-row">
            <button class="btn btn-primary" v-if="!answered" @click="checkAnswer" :disabled="selectedAnswer === null">
              Antwort abgeben
            </button>
            <button class="btn btn-secondary" v-if="answered" @click="nextQuestion">
              Weiter
            </button>
          </div>
          <div v-if="answered" class="result-message">
            <span v-if="result" class="user-answer correct">Richtig!</span>
            <span v-else class="user-answer incorrect">
              Leider falsch. Die richtige Antwort ist: {{ currentQuestion.correctAnswer }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Penguin from '@/components/Penguin.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

export default {
  components: { Penguin },
  data() {
    return {
    quiz: {
        title: "Demo-Quiz",
        description: "Teste dein Wissen über Hauptstädte in Europa!"
      },
      questions: [
        {
          question: "Was ist die Hauptstadt von Deutschland?",
          answers: ["Berlin", "München", "Hamburg", "Köln"],
          correctAnswer: "Berlin"
        },
        {
          question: "Was ist die Hauptstadt von Frankreich?",
          answers: ["Paris", "Lyon", "Marseille", "Nizza"],
          correctAnswer: "Paris"
        },
      ],
      currentIndex: 0,
      selectedAnswer: null,
      result: null,
      answered: false,
      correctCount: 0,
      totalCount: 0,
      userAnswers: []
    }
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex];
    }
  },
  methods: {
    checkAnswer() {
      this.totalCount++;
      const isCorrect = this.selectedAnswer === this.currentQuestion.correctAnswer;
      this.result = isCorrect;
      if (isCorrect) this.correctCount++;
      this.userAnswers[this.currentIndex] = {
        question: this.currentQuestion.question,
        selected: this.selectedAnswer,
        correct: this.currentQuestion.correctAnswer,
        isCorrect
      };
      this.answered = true;
    },
    nextQuestion() {
      this.currentIndex++;
      this.selectedAnswer = null;
      this.answered = false;
      if (this.currentIndex >= this.questions.length) {
        localStorage.setItem('quizResults', JSON.stringify(this.userAnswers));
        this.$router.push({
          name: "quiz-result",
          query: {
            correct: this.correctCount,
            total: this.totalCount,
          }
        });
      }
    }
  }
}
</script>

<style scoped>
.quiz-overview-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px;
}

.card {
  background-color: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(34, 34, 34, 0.08);
  width: 100%;
}

.quiz-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.quiz-header h2 {
  color: var(--color-accent);
  margin: 0;
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  gap: 16px;
}

.quiz-description {
  font-size: 1rem;
  color: var(--color-text);
  margin-top: 4px;
}

.quiz-progress {
  font-size: 1rem;
  color: var(--color-muted);
  margin-left: 16px;
}

.quiz-card-penguin {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  min-width: 100px;
  height: 100%;
}

.quiz-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.question-block {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.answer-row {
  width: 100%;
  margin-bottom: 12px;
}

.button-row {
  display: flex;
  gap: 12px;
  margin-top: 18px;
}

.btn {
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-size: 1rem;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:disabled {
  background-color: #b0bec5;
  cursor: not-allowed;
}

.btn-primary:hover:enabled {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: #f0f0f0;
  color: var(--color-text);
}

.btn-secondary:hover {
  background-color: #e0e0e0;
  transform: translateY(-2px);
}

.result-message {
  margin-top: 18px;
  font-size: 1.1rem;
}

.user-answer.correct {
  color: #4caf50;
  font-weight: 600;
}

.user-answer.incorrect {
  color: #f44336;
  font-weight: 600;
}
</style>
