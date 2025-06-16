<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="120"
    height="128"
    viewBox="-20 -20 449 479"
    fill="none"
  >
    <ellipse cx="207" cy="374.5" rx="161" ry="64.5" fill="black" fill-opacity="0.09" />
    
    <g class="penguin-body">
      <!-- Body -->
      <path
        d="M358.075 205C365.074 324.515 355.572 408.015 208.574 408.015C36.5557 408.015 50.0739 313.015 58.075 205C66.4387 92.091 85.0751 -0.0109179 208.075 9.70735e-07C307.075 0.0087893 351.456 91.9753 358.075 205Z"
        fill="#231F20"
      />
      
      <!-- Arms -->
      <g class="penguin-arm-right">
        <path
          d="M379.5 215C390.099 255.119 407.589 277.891 392.876 284.217C378.162 290.544 352.974 264.833 336.617 226.791C320.26 188.749 318.927 152.781 333.641 146.455C348.355 140.128 368.922 174.964 379.5 215Z"
          fill="#231F20"
        />
      </g>
      <g class="penguin-arm-left">
        <path
          d="M32.0181 213.32C21.9816 256.475 1.8181 279.955 20.8943 288.211C39.9706 296.466 69.5957 270.438 87.0638 230.075C104.532 189.712 103.228 150.299 84.1521 142.043C65.0759 133.787 42.0338 170.254 32.0181 213.32Z"
          fill="#231F20"
        />
      </g>
      
      <!-- Belly -->
      <path
        d="M142.5 85.4998C147.499 104.5 158.692 147.504 158.692 147.504C172 185 199.192 165.504 202.192 162.504C212.632 152.063 225.232 93.6482 230 76.0034C235 57.5 280.5 39.5005 292.692 96.0037C292.692 96.0037 319.216 211.817 323.192 241.002C330.343 293.502 310.192 339.502 310.192 339.502C302.869 354.44 290.692 384.002 211.692 387.004C180.155 388.202 159.497 388.327 132.192 372.504C109.005 359.067 98.4636 345.785 85.1916 322.504C59.1565 276.834 79.6916 188.004 79.6916 188.004C79.6916 188.004 85.4163 107.059 98.1916 76.0037C104.844 59.832 132.105 45.9965 142.5 85.4998Z"
        fill="white"
      />
      
      <!-- Eyes & Beak -->
      <ellipse class="penguin-eye-left" cx="120" cy="112" rx="12" ry="12" fill="#231F20" />
      <ellipse class="penguin-eye-right" cx="258" cy="112" rx="12" ry="12" fill="#231F20" />
      <path
        d="M185.5 149C181.5 148.977 167 136.149 167 132.709C167 132.14 185.315 127.136 188.896 126.164C189.292 126.056 189.703 126.074 190.088 126.215C192.816 127.213 204.082 131.379 203.999 132.079C203.508 136.222 189.499 149.023 185.5 149Z"
        fill="#D15E48"
      />
      <path
        d="M185.5 106.999C189.499 107.034 204 127.113 204 132.499C204 133.367 186.593 140.832 182.4 142.617C181.829 142.861 181.189 142.824 180.651 142.515C177.536 140.726 166.919 134.549 167 133.486C167.491 126.999 181.5 106.964 185.5 106.999Z"
        fill="#FC7960"
      />
      
      <!-- Feet -->
      <g class="penguin-foot-right">
        <ellipse
          cx="292.496"
          cy="377.866"
          rx="13.8962"
          ry="35.0184"
          transform="rotate(-170.247 292.496 377.866)"
          fill="#FC7960"
        />
        <ellipse
          cx="279.981"
          cy="377.651"
          rx="16.6754"
          ry="35.0184"
          transform="rotate(173.638 279.981 377.651)"
          fill="#FC7960"
        />
        <ellipse
          cx="271.95"
          cy="381.956"
          rx="16.6754"
          ry="35.0184"
          transform="rotate(150 271.95 381.956)"
          fill="#FC7960"
        />
      </g>
      <g class="penguin-foot-left">
        <ellipse
          cx="13.0646"
          cy="35.3274"
          rx="13.0646"
          ry="35.3274"
          transform="matrix(-0.672812 -0.739814 0.657096 -0.753807 115.151 417.621)"
          fill="#FC7960"
        />
        <ellipse
          cx="15.2655"
          cy="36.1143"
          rx="15.2655"
          ry="36.1143"
          transform="matrix(-0.903396 -0.428807 0.369076 -0.929399 119.581 415.221)"
          fill="#FC7960"
        />
        <ellipse
          cx="15.1225"
          cy="36.3787"
          rx="15.1225"
          ry="36.3787"
          transform="matrix(-0.999902 0.014029 -0.0106906 -0.999943 123.019 408.868)"
          fill="#FC7960"
        />
      </g>
    </g>
  </svg>
</template><style scoped>
.penguin-arm-left {
  transform-box: fill-box;
  transform-origin: 35% 35%;
  animation: penguin-arm-left-wiggle 5.0s infinite ease-in-out;
}
.penguin-arm-right {
  transform-box: fill-box;
  transform-origin: 65% 35%;
  animation: penguin-arm-right-wiggle 5.0s infinite ease-in-out;
}
.penguin-body {
  transform-box: fill-box;
  transform-origin: 50% 60%;
  animation: penguin-body-wiggle 9.0s infinite ease-in-out;
}
.penguin-foot-left {
  transform-box: fill-box;
  transform-origin: 30% 100%;
  animation: penguin-foot-left-wiggle 5.0s infinite ease-in-out;
}
.penguin-foot-right {
  transform-box: fill-box;
  transform-origin: 70% 100%;
  animation: penguin-foot-right-wiggle 5.0s infinite ease-in-out;
}
.penguin-eye-left,
.penguin-eye-right {
  transform-box: fill-box;
  transform-origin: 50% 50%;
  animation: penguin-eye-blink 10s infinite;
}
@keyframes penguin-arm-left-wiggle {
  0%,
  100% {
    transform: rotate(-2deg);
  }
  20% {
    transform: rotate(-6deg);
  }
  50% {
    transform: rotate(0deg);
  }
  80% {
    transform: rotate(-6deg);
  }
}
@keyframes penguin-arm-right-wiggle {
  0%,
  100% {
    transform: rotate(2deg);
  }
  20% {
    transform: rotate(6deg);
  }
  50% {
    transform: rotate(0deg);
  }
  80% {
    transform: rotate(6deg);
  }
}
@keyframes penguin-body-wiggle {
  0%,
  100% {
    transform: rotate(0deg) scale(1);
  }
  20% {
    transform: rotate(-2deg) scale(1.01, 0.99);
  }
  50% {
    transform: rotate(2deg) scale(0.99, 1.01);
  }
  80% {
    transform: rotate(-2deg) scale(1.01, 0.99);
  }
}
@keyframes penguin-foot-left-wiggle {
  0%,
  100% {
    transform: rotate(-2deg);
  }
  30% {
    transform: rotate(-12deg);
  }
  60% {
    transform: rotate(4deg);
  }
}
@keyframes penguin-foot-right-wiggle {
  0%,
  100% {
    transform: rotate(2deg);
  }
  30% {
    transform: rotate(12deg);
  }
  60% {
    transform: rotate(-4deg);
  }
}
@keyframes penguin-eye-blink {
  0%,
  100% {
    transform: scaleY(1);
  }
  9% {
    transform: scaleY(1);
  }
  10% {
    transform: scaleY(0.6);
  }
  11% {
    transform: scaleY(1);
  }
  60% {
    transform: scaleY(1);
  }
  64% {
    transform: scaleY(0.4);
  }
  66% {
    transform: scaleY(1);
  }
}
</style>