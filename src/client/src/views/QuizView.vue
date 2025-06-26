<template>
    <div class = "quiz-overview-card">
        <h2>Quizname
            <span class="quiz-progress">
                ( {{ currentIndex + 1 }} / {{ questions.length }})
            </span>
        </h2>
          <div class="quiz-card-penguin">
          <Penguin style="width: 80px; height: 80px;" />
        </div>
   </div>
   <div class = "question-card">
            <h3>{{ currentQuestion.question }}</h3>
            <div v-for="(answer,index) in currentQuestion.answers" :key="index">
                <label>
                    <input type="radio" :value="answer" v-model="selectedAnswer" name="answer" > 
                    {{ answer }}
                </label> 
            </div>
            <button class = "btn-primary" v-if="!answered" @click="checkAnswer" :disabled="selectedAnswer === null" >Anwort abgeben</button>
            <div v-if="answered">
                <span v-if="result">Richtig!</span>
                <span v-else>Leider falsch. Die richtige Antwort ist: {{ currentQuestion.correctAnswer }}</span>
                <button class = "btn-secondary" @click="nextQuestion">Weiter</button>
            </div>
    
   </div>
</template>

<script>
import { useRouter } from 'vue-router'
const router = useRouter()

export default {
    data() {
        return {
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
        currentIndex:0,
        selectedAnswer: null,
        result: null,
        answered: false,
        correctCount: 0,
        totalCount: 0,
        userAnswers: []
        };     
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
        // Antwort speichern
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
            // Daten an quiz-result übergeben
            localStorage.setItem('quizResults', JSON.stringify(this.userAnswers)),
            // Weiterleitung zur Ergebnis-Seite
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
};
</script>

<style scoped>
    .quiz-overview-card {
      max-width: 800px;
      margin: 20px auto;
      padding: 20px;
      background: #f9f9f9;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .question-card {
      flex: 1;
      max-width: 800px;
      margin: 20px auto;
      padding: 20px;
      background: #fff;
      font-size: 1.2rem;
      line-height: 1.5;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .quiz-progress {
      font-size: 0.9rem;
      color: #888;
      margin-left: 10px;
      color: var(--color-muted);
      display: inline-block;
    }

    .btn-primary {
      padding: 12px 20px;
      font-size: 1.1rem;
      background: var(--color-primary);
      color: #fff;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 12px;
      transition: background 0.2s;
    }

    .btn-secondary {
      padding: 12px 20px;
      font-size: 1.1rem;
      background: var(--color-primary);
      color: #fff;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 12px;
      transition: background 0.2s;
    }
    </style>
