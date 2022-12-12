/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,ts}"],
  theme: {
    extend: {
      colors: {
        primary: "#36805B",
        secondary: "#5CAC96",
        tertiary: "#56A38C",
        quarternary: "#D7EFE9",
        neutral: "#FDF4F7",
        primary_button: "#FA5454",
        primary_button_disabled: "#fb8383",
      },
    },
  },
  plugins: [],
};
