/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        'ra-orange': '#F4B384',
        'ra-blue': '#85BBEA',
        'ra-green': '#9ACC99',
        'ra-yellow': '#F4D075',
        'ra-red': '#F29C9C',
        'ra-purple': '#A4A6D5',
        'ra-bg': '#E6EEED',
      },
      fontFamily: {
        'sans': ['"Century Gothic"', '"VAG Rounded"', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
