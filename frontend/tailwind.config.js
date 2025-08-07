/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0a0a0f",
      },
      animation: {
        gradientShift: "gradientShift 15s ease infinite",
      },
      backgroundSize: {
        400: "400% 400%",
      },
    },
  },
  plugins: [],
};
